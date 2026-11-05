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
