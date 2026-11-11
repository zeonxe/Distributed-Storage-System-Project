from master import Master
from storage_node import StorageNode

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
        
        sorted_chunks = sorted(chunk_ids, key=lambda chunk_id: int(chunk_id.rsplit("_", 1)[1]))
        retrieved_chunks = []

        for chunk_id in sorted_chunks:
            data = self.download_chunk(filename, chunk_id)
            retrieved_chunks.append(data)

        return "".join(retrieved_chunks)




    




master = Master()

node_A = StorageNode("node_A")
node_B = StorageNode("node_B")
node_C = StorageNode("node_C")

storage_nodes = {
    "node_A": node_A,
    "node_B": node_B,
    "node_C": node_C,
    
}

client = Client(master, storage_nodes)

master.add_node("node_A")
master.add_node("node_B")
master.add_node("node_C")

master.add_file("hello.txt", 11)

client.upload_chunk("hello.txt", "chunk_0", "Hello World")
print(node_A.storage)
print(node_B.storage)
print(node_C.storage)

print(client.master.metadata)
print(client.storage_nodes["node_A"].node_id)
print(master.nodes)
print(master.select_nodes())
print(client.download_chunk("hello.txt", "chunk_0"))


node_A.storage.pop("chunk_0")
print(client.download_chunk("hello.txt", "chunk_0"))

print(client.split_file("Hello World Python", 4))

client.upload_file("test.txt", "Hello World Python", 4)
print(master.lookup_file("test.txt"))

reconstructed_file = client.download_file("test.txt")
print("Reconstructed file:", reconstructed_file)

print(node_A.is_alive)
node_A.is_alive = False
print(client.download_file("test.txt"))



print(node_A.is_alive)
print(node_A.storage)