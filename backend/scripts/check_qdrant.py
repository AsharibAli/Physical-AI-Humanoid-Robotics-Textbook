"""
Script to check Qdrant collection data and status.

This script verifies:
1. Connection to Qdrant
2. Collection existence
3. Number of vectors stored
4. Sample data retrieval
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from qdrant_client import QdrantClient
from backend.config.settings import settings


async def check_qdrant():
    """Check Qdrant collection status and data."""

    print("=" * 60)
    print("QDRANT DATA CHECK")
    print("=" * 60)
    print()

    # 1. Initialize client
    print("1. Connecting to Qdrant...")
    print(f"   URL: {settings.qdrant_url}")

    try:
        client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        print("   [OK] Connected successfully")
    except Exception as e:
        print(f"   [ERROR] Connection failed: {str(e)}")
        return

    print()

    # 2. Check collection existence
    collection_name = settings.qdrant_collection_name
    print(f"2. Checking collection: '{collection_name}'...")

    try:
        collections = client.get_collections()
        collection_names = [c.name for c in collections.collections]

        if collection_name in collection_names:
            print(f"   [OK] Collection exists")
        else:
            print(f"   [ERROR] Collection does NOT exist")
            print(f"   Available collections: {collection_names}")
            return
    except Exception as e:
        print(f"   [ERROR] Failed to get collections: {str(e)}")
        return

    print()

    # 3. Get collection info
    print("3. Getting collection information...")

    try:
        collection_info = client.get_collection(collection_name)
        print(f"   Vector count: {collection_info.points_count}")
        print(f"   Vector size: {collection_info.config.params.vectors.size}")
        print(f"   Distance metric: {collection_info.config.params.vectors.distance}")

        if collection_info.points_count == 0:
            print()
            print("   [WARNING]  WARNING: Collection is empty!")
            print("   Run the ingestion script to add documents:")
            print("   > uv run python scripts/ingest_content.py")
            return

    except Exception as e:
        print(f"   [ERROR] Failed to get collection info: {str(e)}")
        return

    print()

    # 4. Sample some data
    print("4. Retrieving sample documents...")

    try:
        # Get first 5 points
        results = client.scroll(
            collection_name=collection_name,
            limit=5,
            with_payload=True,
            with_vectors=False
        )

        points = results[0]

        if points:
            print(f"   [OK] Retrieved {len(points)} sample documents")
            print()

            for i, point in enumerate(points, 1):
                payload = point.payload
                print(f"   Document {i}:")
                print(f"   - ID: {point.id}")
                print(f"   - Module: {payload.get('module_id', 'N/A')}")
                print(f"   - Chapter: {payload.get('chapter_id', 'N/A')}")
                print(f"   - Section: {payload.get('section_type', 'N/A')}")
                print(f"   - Text preview: {payload.get('chunk_text', '')[:100]}...")
                print()
        else:
            print("   [ERROR] No documents found")

    except Exception as e:
        print(f"   [ERROR] Failed to retrieve sample data: {str(e)}")
        return

    print()

    # 5. Test search
    print("5. Testing vector search...")

    try:
        from openai import OpenAI

        openai_client = OpenAI(api_key=settings.openai_api_key)

        # Create test embedding
        test_query = "What is ROS 2?"
        response = openai_client.embeddings.create(
            model=settings.openai_embedding_model,
            input=test_query
        )
        query_vector = response.data[0].embedding

        # Search
        search_response = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=3,
            with_payload=True
        )
        search_results = search_response.points

        print(f"   [OK] Search successful!")
        print(f"   Query: \"{test_query}\"")
        print(f"   Results found: {len(search_results)}")
        print()

        for i, result in enumerate(search_results, 1):
            print(f"   Result {i}:")
            print(f"   - Score: {result.score:.4f}")
            print(f"   - Source: {result.payload.get('module_id')}/{result.payload.get('chapter_id')}")
            print(f"   - Text: {result.payload.get('chunk_text', '')[:150]}...")
            print()

    except Exception as e:
        print(f"   [WARNING]  Search test failed: {str(e)}")
        print("   (This is optional - collection data is still accessible)")

    print()
    print("=" * 60)
    print("[OK] QDRANT CHECK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(check_qdrant())
