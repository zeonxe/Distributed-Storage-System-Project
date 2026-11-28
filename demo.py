
from master import Master
from storage_node import StorageNode
from client import Client
from concurrent.futures import ThreadPoolExecutor


# Initialize storage nodes
node_A = StorageNode("node_A")
node_B = StorageNode("node_B")
node_C = StorageNode("node_C")

storage_nodes = {
    "node_A": node_A,
    "node_B": node_B,
    "node_C": node_C
}

# Initialize Master and Client
master = Master(storage_nodes)
client = Client(master, storage_nodes)

# Register storage nodes
master.add_node("node_A")
master.add_node("node_B")
master.add_node("node_C")


# TEST 1: File upload and reconstruction
print("\n=== TEST 1: FILE UPLOAD AND DOWNLOAD ===")

client.upload_file("test.txt", "Hello World Python", 4)

reconstructed = client.download_file("test.txt")
assert reconstructed == "Hello World Python"

print("Reconstructed file:", reconstructed)
print("PASS: File uploaded and reconstructed successfully")


# TEST 2: Verify replication
print("\n=== TEST 2: CHUNK REPLICATION ===")

for i in range(5):
    chunk_id = f"test.txt_chunk_{i}"

    assert chunk_id in node_A.storage
    assert chunk_id in node_B.storage
    assert node_A.storage[chunk_id] == node_B.storage[chunk_id]

print("PASS: All five chunks replicated across Node A and Node B")


# TEST 3: Simulate node failure and replica fallback
print("\n=== TEST 3: NODE FAILURE AND FALLBACK ===")

node_A.is_alive = False

reconstructed = client.download_file("test.txt")
assert reconstructed == "Hello World Python"

print("PASS: File retrieved despite Node A being offline")


# TEST 4: Automatic recovery
print("\n=== TEST 4: AUTOMATIC RECOVERY ===")

master.recover_node("node_A")

for i in range(5):
    chunk_id = f"test.txt_chunk_{i}"

    assert chunk_id in node_C.storage
    assert node_C.storage[chunk_id] == node_B.storage[chunk_id]

print("PASS: Missing replicas restored onto Node C")


# TEST 5: Metadata consistency
print("\n=== TEST 5: METADATA CONSISTENCY ===")

for i in range(5):
    chunk_id = f"test.txt_chunk_{i}"

    locations = [
        entry["node_id"]
        for entry in master.lookup_file("test.txt")
        if entry["chunk_id"] == chunk_id
    ]

    assert sorted(locations) == ["node_B", "node_C"]

print("PASS: Metadata reflects two replicas per chunk")


# TEST 6: Concurrent uploads
print("\n=== TEST 6: CONCURRENT UPLOADS ===")

with ThreadPoolExecutor(max_workers=2) as executor:
    future_A = executor.submit(
        client.upload_file, "alpha.txt", "Hello from Alpha", 4
    )

    future_B = executor.submit(
        client.upload_file, "beta.txt", "Hello from Beta", 4
    )

    future_A.result()
    future_B.result()

assert client.download_file("alpha.txt") == "Hello from Alpha"
assert client.download_file("beta.txt") == "Hello from Beta"

print("PASS: Both concurrent uploads completed successfully")


# TEST 7: Insufficient healthy nodes
print("\n=== TEST 7: INSUFFICIENT HEALTHY NODES ===")

node_B.is_alive = False

try:
    master.select_nodes()
except ValueError as error:
    print("PASS: Expected error:", error)
else:
    raise AssertionError("Expected an error for insufficient healthy nodes")


print("\n=== ALL DEMONSTRATION TESTS PASSED ===")
