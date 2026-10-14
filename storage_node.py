class StorageNode:
    def __init__(self, node_id):
        self.storage = {}
        self.node_id = node_id


node_A = StorageNode("node_A")
node_B = StorageNode("node_B")
node_C = StorageNode("node_C")

print(node_A.node_id)
print(node_A.storage)

print(node_B.node_id)
print(node_B.storage)

print(node_C.node_id)
print(node_C.storage)

