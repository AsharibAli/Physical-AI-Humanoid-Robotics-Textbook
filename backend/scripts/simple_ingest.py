"""
Simple standalone script to ingest textbook chapters into Qdrant.
No external module dependencies - everything self-contained.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from backend.config.settings import settings


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 100):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())

    return chunks


def extract_metadata(file_path: Path):
    """Extract module and chapter info from file path."""
    parts = file_path.parts
    module_id = "unknown"
    chapter_id = file_path.stem

    for part in parts:
        if part.startswith('module-'):
            module_id = part
            break

    return module_id, chapter_id


def process_file(file_path: Path, openai_client, point_id):
    """Process a markdown file and create vector points."""
    print(f"  Processing: {file_path.name}")

    # Read content
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"    [ERROR] Could not read file: {e}")
        return []

    # Remove frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            title_line = [line for line in parts[1].split('\n') if 'title:' in line]
            title = title_line[0].split(':', 1)[1].strip() if title_line else file_path.stem
            content = parts[2].strip()
        else:
            title = file_path.stem
    else:
        title = file_path.stem

    # Get metadata
    module_id, chapter_id = extract_metadata(file_path)

    # Chunk content
    chunks = chunk_text(content)
    print(f"    Created {len(chunks)} chunks")

    # Generate embeddings and create points
    points = []
    for i, text_chunk in enumerate(chunks):
        try:
            # Generate embedding
            response = openai_client.embeddings.create(
                model=settings.openai_embedding_model,
                input=text_chunk
            )
            embedding = response.data[0].embedding

            # Create point
            point = PointStruct(
                id=point_id + i,
                vector=embedding,
                payload={
                    'module_id': module_id,
                    'chapter_id': chapter_id,
                    'chapter_title': title,
                    'section_type': 'general',
                    'chunk_text': text_chunk,
                    'file_path': str(file_path)
                }
            )
            points.append(point)

        except Exception as e:
            print(f"    [ERROR] Failed to create embedding for chunk {i}: {e}")

    print(f"    Generated {len(points)} vectors")
    return points


def main():
    """Main ingestion function."""
    print("=" * 60)
    print("SIMPLE CONTENT INGESTION")
    print("=" * 60)
    print()

    # Initialize clients
    print("1. Initializing clients...")
    openai_client = OpenAI(api_key=settings.openai_api_key)
    qdrant_client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )
    print("   [OK] Clients initialized")
    print()

    # Create/recreate collection
    collection_name = settings.qdrant_collection_name
    print(f"2. Setting up collection: {collection_name}")

    try:
        # Delete if exists
        try:
            qdrant_client.delete_collection(collection_name)
            print("   Deleted existing collection")
        except:
            pass

        # Create new
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1536,  # OpenAI ada-002 size
                distance=Distance.COSINE
            )
        )
        print("   [OK] Collection created")
    except Exception as e:
        print(f"   [ERROR] Collection setup failed: {e}")
        return

    print()

    # Find markdown files
    docs_dir = Path(__file__).parent.parent.parent / 'frontend' / 'docs'
    print(f"3. Scanning for content in: {docs_dir}")

    md_files = []

    # Add intro.md if exists
    intro_file = docs_dir / 'intro.md'
    if intro_file.exists():
        md_files.append(intro_file)

    # Add all markdown files from module directories
    for module_dir in sorted(docs_dir.glob('module-*')):
        if module_dir.is_dir():
            # Get all .md files (chapters and index)
            for md_file in sorted(module_dir.glob('*.md')):
                md_files.append(md_file)

    print(f"   Found {len(md_files)} markdown files")

    if not md_files:
        print("   [WARNING] No chapter files found!")
        print("   Make sure chapters exist in frontend/docs/module-*/chapter-*.md")
        return

    print()

    # Process files
    print("4. Processing files...")
    print()

    all_points = []
    point_id = 1

    for md_file in md_files:
        points = process_file(md_file, openai_client, point_id)
        all_points.extend(points)
        point_id += len(points)

    print()
    print(f"   Total vectors created: {len(all_points)}")
    print()

    # Upload to Qdrant
    if all_points:
        print("5. Uploading to Qdrant...")

        batch_size = 100
        total_batches = (len(all_points) + batch_size - 1) // batch_size

        for i in range(0, len(all_points), batch_size):
            batch = all_points[i:i + batch_size]
            try:
                qdrant_client.upsert(
                    collection_name=collection_name,
                    points=batch
                )
                batch_num = i // batch_size + 1
                print(f"   Batch {batch_num}/{total_batches} uploaded")
            except Exception as e:
                print(f"   [ERROR] Batch {i // batch_size + 1} failed: {e}")

        print("   [OK] Upload complete")
    else:
        print("5. [ERROR] No vectors to upload")
        return

    print()

    # Verify
    print("6. Verifying...")
    try:
        info = qdrant_client.get_collection(collection_name)
        print(f"   Vectors in collection: {info.points_count}")

        if info.points_count > 0:
            print("   [OK] Ingestion successful!")
        else:
            print("   [ERROR] Collection is empty")
    except Exception as e:
        print(f"   [ERROR] Verification failed: {e}")

    print()
    print("=" * 60)
    print("[OK] INGESTION COMPLETE")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Verify: uv run python scripts/check_qdrant.py")
    print("2. Test chatbot at: http://localhost:3000")
    print()


if __name__ == "__main__":
    main()
