"""
Content ingestion script.

This script orchestrates the full document ingestion pipeline:
1. Parse Markdown documents from frontend/docs/
2. Chunk documents into overlapping segments
3. Generate embeddings using OpenAI API
4. Store embeddings in Qdrant vector database
"""

import argparse
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

from backend.ingestion.chunker import TextChunker
from backend.ingestion.embedder import EmbeddingGenerator
from backend.ingestion.markdown_parser import MarkdownParser
from backend.ingestion.vector_store import VectorStore
from backend.models.embedding import DocumentChunk, EmbeddingMetadata


def main():
    """Run the document ingestion pipeline."""
    parser = argparse.ArgumentParser(description="Ingest documents into vector database")
    parser.add_argument(
        "--docs-path",
        type=str,
        default="../frontend/docs",
        help="Path to frontend docs directory",
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Recreate collection (deletes existing data)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Chunk size in words",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=100,
        help="Overlap size in words",
    )
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not openai_api_key:
        print("Error: OPENAI_API_KEY not set in environment")
        sys.exit(1)
    if not qdrant_url:
        print("Error: QDRANT_URL not set in environment")
        sys.exit(1)

    print("=" * 80)
    print("DOCUMENT INGESTION PIPELINE")
    print("=" * 80)

    # Resolve docs path
    docs_path = Path(__file__).parent.parent / args.docs_path
    if not docs_path.exists():
        print(f"Error: Docs path does not exist: {docs_path}")
        sys.exit(1)

    print(f"\nDocs path: {docs_path}")
    print(f"Chunk size: {args.chunk_size} words")
    print(f"Overlap: {args.overlap} words")
    print(f"Recreate collection: {args.recreate}")
    print()

    # Step 1: Parse documents
    print("Step 1: Parsing Markdown documents...")
    parser = MarkdownParser(docs_path)
    documents = parser.parse_all_documents()
    print(f"Found {len(documents)} documents")

    if not documents:
        print("Warning: No documents found. Make sure frontend/docs/ has .md files.")
        sys.exit(0)

    # Step 2: Chunk documents
    print("\nStep 2: Chunking documents...")
    chunker = TextChunker(
        chunk_size=args.chunk_size,
        overlap_size=args.overlap,
    )

    all_chunks = []
    for doc in documents:
        sections = doc.get_sections()

        # If no sections found, treat entire content as one section
        if not sections:
            sections = {"general": doc.content}

        section_chunks = chunker.chunk_document_sections(sections)

        for section_type, chunk_text, chunk_idx in section_chunks:
            # Create metadata
            metadata = EmbeddingMetadata(
                chapter_id=doc.chapter_id,
                chapter_title=doc.title,
                module_id=doc.module_id,
                section_type=section_type,
                chunk_index=chunk_idx,
                file_path=str(doc.file_path),
                topics=[],  # TODO: Extract topics using NLP or keywords
                chunk_text=chunk_text,
                word_count=chunker.get_word_count(chunk_text),
            )

            # Create document chunk
            chunk = DocumentChunk(
                chunk_id=f"{doc.chapter_id}_{section_type}_{chunk_idx}",
                text=chunk_text,
                embedding=None,  # Will be populated in next step
                metadata=metadata,
            )
            all_chunks.append(chunk)

    print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")

    # Step 3: Generate embeddings
    print("\nStep 3: Generating embeddings...")
    embedder = EmbeddingGenerator(api_key=openai_api_key)

    texts = [chunk.text for chunk in all_chunks]
    embeddings = embedder.generate_embeddings_sync(texts, show_progress=True)

    # Assign embeddings to chunks
    for chunk, embedding in zip(all_chunks, embeddings):
        chunk.embedding = embedding

    print(f"Generated {len(embeddings)} embeddings")

    # Step 4: Store in Qdrant
    print("\nStep 4: Storing embeddings in Qdrant...")
    vector_store = VectorStore(
        url=qdrant_url,
        api_key=qdrant_api_key,
    )

    # Create collection if needed
    if args.recreate or not vector_store.collection_exists():
        vector_store.create_collection(
            vector_size=embedder.get_embedding_dimension(),
            recreate=args.recreate,
        )

    # Upsert chunks
    vector_store.upsert_chunks(all_chunks, show_progress=True)

    # Get collection info
    info = vector_store.get_collection_info()
    print("\nCollection Info:")
    print(f"  Points count: {info.get('points_count', 'N/A')}")
    print(f"  Vectors count: {info.get('vectors_count', 'N/A')}")
    print(f"  Status: {info.get('status', 'N/A')}")

    print("\n" + "=" * 80)
    print("INGESTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
