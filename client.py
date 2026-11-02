from master import Master
from storage_node import StorageNode

class Client:
    def __init__(self, master, storage_nodes):
        self.master = master
        self.storage_nodes = storage_nodes



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

print(client.master.metadata)
print(client.storage_nodes["node_A"].node_id)
print(master.nodes)
print(master.select_nodes())
