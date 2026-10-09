class Master:
    def __init__(self):
        self.metadata = {}
        self.nodes = {}

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

        