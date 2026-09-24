import re

with open('src/chroma_client.py', 'r') as f:
    content = f.read()

# Replace the connection logic
old_block = """    host = os.getenv("CHROMADB_HOST", "localhost")
    port = int(os.getenv("CHROMADB_PORT", "8100"))

    if not _port_open(host, port):
        raise RuntimeError(
            f"ChromaDB is not reachable at {host}:{port}. Start the ChromaDB "
            f"service (e.g. `docker compose up chromadb`) or set CHROMADB_HOST / "
            f"CHROMADB_PORT to point at a running instance."
        )

    client = chromadb.HttpClient(host=host, port=port)"""

new_block = """    # Using local persistent ChromaDB for native memory without a Docker container
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
    os.makedirs(db_path, exist_ok=True)
    client = chromadb.PersistentClient(path=db_path)"""

content = content.replace(old_block, new_block)

with open('src/chroma_client.py', 'w') as f:
    f.write(content)
print("Patched ChromaDB to use PersistentClient")
