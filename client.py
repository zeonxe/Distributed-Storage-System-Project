
class Client:
    def __init__(self, master, storage_nodes):
        self.master = master
        self.storage_nodes = storage_nodes

    def upload_chunk(self, filename, chunk_id, data):
        selected_nodes = self.master.select_nodes()

        for node_id in selected_nodes:
            self.storage_nodes[node_id].store_chunk(chunk_id, data)
            self.master.add_chunk(filename, node_id, chunk_id)

    def download_chunk(self, filename, chunk_id):
        chunk_locations = self.master.lookup_file(filename)

        for location in chunk_locations:
            if location["chunk_id"] == chunk_id:
                node_id = location["node_id"]

                try:
                    return self.storage_nodes[node_id].retrieve_data(chunk_id)
                except (KeyError, ConnectionError):
                    print(f"Could not retrieve {chunk_id} from {node_id}. Trying next replica...")

        raise ValueError(f"No available replica found for {chunk_id}")

    def split_file(self, data, chunk_size=6):
        chunks = []

        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            chunks.append(chunk)

        return chunks

    def upload_file(self, filename, data, chunk_size=6):
        self.master.add_file(filename, len(data))

        chunks = self.split_file(data, chunk_size)

        for index, chunk in enumerate(chunks):
            chunk_id = f"{filename}_chunk_{index}"
            self.upload_chunk(filename, chunk_id, chunk)

    def download_file(self, filename):
        chunk_locations = self.master.lookup_file(filename)
        chunk_ids = set()

        for location in chunk_locations:
            chunk_ids.add(location["chunk_id"])

        sorted_chunks = sorted(
            chunk_ids,
            key=lambda chunk_id: int(chunk_id.rsplit("_", 1)[1])
        )

        retrieved_chunks = []

        for chunk_id in sorted_chunks:
            data = self.download_chunk(filename, chunk_id)
            retrieved_chunks.append(data)

        return "".join(retrieved_chunks)
