class Master:
    def __init__(self):
        self.metadata = {}
        self.nodes = {}

    def add_file(self, filename, filesize):
        self.metadata[filename][filesize] = {
            "chunks": []
        }

    def add_node(self, node_id):
        self.nodes[node_id] = {
            "chunks": []

        }


    def add_chunk(self, filename, node_id, chunk_id):
        self.metadata[filename]["chunks"].append(chunk_id)
        self.nodes[node_id]["chunks"].append(chunk_id)
    

master = Master()
master.add_file("hello.txt", 10246)
print(master.metadata)

master.add_node("node_A")
master.add_node("node_B")
master.add_node("node_C")
print(master.nodes)

master.add_chunk("hello.txt", "node_A", "chunk_0")
master.add_chunk("hello.txt", "node_B", "chunk_1")
master.add_chunk("hello.txt", "node_C", "chunk_2")
print(master.metadata)

        