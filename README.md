# Distributed-Storage-System-Project

Overview

This project is a miniature distributed storage system developed in Python as part of an independent study in computer science. Inspired by concepts from the Google File System (GFS), the system demonstrates how file chunking, replication, metadata management, and fault tolerance can be implemented across multiple storage nodes.

The primary objective is to explore how a distributed storage system can maintain data availability and recover from simulated storage node failures.

System Architecture

The system consists of three primary components:

Master (master.py): Manages file metadata, registers storage nodes, selects storage destinations, tracks chunk locations, and coordinates replica recovery.

Storage Nodes (storage_node.py): Store file chunks in memory, retrieve stored data, and simulate node availability through health-status flags.

Client (client.py): Splits file contents into chunks, uploads them to selected storage nodes, retrieves chunks using the Master's metadata, and reconstructs complete files.

The components interact through Python object references within a single process rather than through a physical network.

Features

File Chunking: Divides file contents into smaller, configurable chunks.

Chunk Replication: Stores two copies of each chunk on separate storage nodes.

Metadata Management: Tracks files, chunk identifiers, and replica locations.

File Reconstruction: Retrieves and reassembles chunks in their original order.

Replica Fallback: Retrieves data from another replica when the first is unavailable.

Simulated Node Failure: Marks storage nodes offline without immediately deleting their stored data.

Automatic Recovery: Copies surviving replicas to healthy nodes and updates metadata after a simulated failure.

Concurrency Demonstration: Uses Python threads to submit multiple file uploads concurrently, with locks protecting selected metadata updates.

Project Structure

Distributed-Storage-System-Project/
├── master.py
├── storage_node.py
├── client.py
├── demo.py
└── README.md

Running the Project

Requirements: Python 3.11 or a compatible Python 3 version. No third-party packages are required.

Clone or download the repository.

Open a terminal in the project directory.

Run the demonstration:

python demo.py

The demonstration executes seven tests covering file uploading, replication, simulated node failure, automatic recovery, metadata consistency, concurrent uploads, and insufficient healthy-node handling.

Successful execution ends with:

=== ALL DEMONSTRATION TESTS PASSED ===

Limitations

This project is an educational prototype rather than a production-ready distributed file system.

Storage nodes operate in memory rather than on independent physical servers.

File contents are represented as strings rather than actual disk files.

Node availability is simulated through Boolean health flags rather than network heartbeats.

Replica placement uses a simplified selection strategy.

Concurrency testing demonstrates overlapping upload operations but does not establish complete thread safety.

Recovery is designed for the demonstrated failure scenario and does not cover every possible failure condition.

Conclusion

This project demonstrates fundamental distributed storage concepts through a working Python prototype. It illustrates how replication and metadata coordination can preserve access to data during simulated node failures and how missing replicas can be restored using surviving storage nodes.
