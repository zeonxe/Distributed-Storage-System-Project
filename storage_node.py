class StorageNode:
    def __init__(self, node_id):
        self.storage = {}
        self.node_id = node_id


    def store_chunk(self, chunk_id, data):
        self.storage[chunk_id] = data

    def retrieve_data(self, chunk_id):
        return self.storage[chunk_id]
            
         

node_A = StorageNode("node_A")
node_B = StorageNode("node_B")
node_C = StorageNode("node_C")

node_A.store_chunk("chunk_0", "Hello World")
node_B.store_chunk("chunk_0", "Hello World")

print(node_B.retrieve_data("chunk_0"))

    

print(node_A.node_id)
print(node_A.storage)

print(node_B.node_id)
print(node_B.storage)

print(node_C.node_id)
print(node_C.storage)

