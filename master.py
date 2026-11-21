class Master:
    def __init__(self, storage_nodes=None):
        self.metadata = {}
        self.nodes = {}
        self.storage_nodes = storage_nodes if storage_nodes is not None else {}

    def add_file(self, filename, filesize):
        self.metadata[filename] = {
            "filesize": filesize,
            "chunks": []
        }

    def add_node(self, node_id):
        self.nodes[node_id] = {
            "chunks": []

        }


    def add_chunk(self, filename, node_id, chunk_id):
       if filename not in self.metadata:
           raise ValueError(f"File {filename} does not exist")
       if node_id not in self.nodes:
           raise ValueError(f"Node {node_id} does not exist")

        # Track the chunk and its storage location
       self.metadata[filename]["chunks"].append({
           "chunk_id": chunk_id,
           "node_id": node_id
       })

       self.nodes[node_id]["chunks"].append(chunk_id) 

    def lookup_file(self, filename):
        if filename not in self.metadata:
            raise ValueError(f"File {filename} does not exist")

        return self.metadata[filename]["chunks"]

    def select_nodes(self, replication_factor=2):
        healthy_nodes = []

        for node_id in self.nodes:
            if self.storage_nodes[node_id].is_alive:
                healthy_nodes.append(node_id)

        return healthy_nodes[:replication_factor]

    def recover_node(self, failed_node_id):
        if self.storage_nodes[failed_node_id].is_alive:
            print(f"{failed_node_id} is still online")
            return

        print(f"Recovering chunks from {failed_node_id}")

        lost_chunks = list(self.nodes[failed_node_id]["chunks"])

        for chunk_id in lost_chunks:
            print(f"Needs recovery: {chunk_id}")

            # Find which file this chunk belongs to
            filename = None

            for name, file_info in self.metadata.items():
                if any(entry["chunk_id"] == chunk_id for entry in file_info["chunks"]):
                    filename = name
                    break

            if filename is None:
                print(f"No metadata found for {chunk_id}")
                continue

            # Find a healthy surviving replica
            source_id = None

            for node_id in self.select_nodes():
                if chunk_id in self.nodes[node_id]["chunks"]:
                    source_id = node_id
                    break

            if source_id is None:
                print(f"No surviving replica found for {chunk_id}")
                continue

            data = self.storage_nodes[source_id].retrieve_data(chunk_id)

            # Find a healthy replacement destination
            target_id = None

            for node_id in self.select_nodes():
                if node_id == source_id:
                    continue

                target = self.storage_nodes[node_id]

                if chunk_id not in target.storage:
                    target.store_chunk(chunk_id, data)

                target_id = node_id
                break

            if target_id is None:
                print(f"No replacement destination available for {chunk_id}")
                continue

            # Register the recovered replica if not already recorded
            if chunk_id not in self.nodes[target_id]["chunks"]:
                self.add_chunk(filename, target_id, chunk_id)

            print(f"Recovered {chunk_id} onto {target_id}")

        # Remove failed node's replica locations from metadata
        for file_info in self.metadata.values():
            file_info["chunks"] = [
                entry for entry in file_info["chunks"]
                if entry["node_id"] != failed_node_id
            ]

        self.nodes[failed_node_id]["chunks"].clear()

        



if __name__ == "__main__":
    master = Master()
    master.add_file("hello.txt", 10246)

    master.add_node("node_A")
    master.add_node("node_B")
    master.add_node("node_C")


    master.add_chunk("hello.txt", "node_A", "chunk_0")
    master.add_chunk("hello.txt", "node_B", "chunk_1")
    master.add_chunk("hello.txt", "node_C", "chunk_2")

    print(master.metadata)
    print(master.nodes)
    # print(master.lookup_file("missing.txt"))

        