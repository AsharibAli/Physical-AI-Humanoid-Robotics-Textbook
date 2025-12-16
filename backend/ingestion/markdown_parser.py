"""
Markdown parser for document ingestion.

This module reads and parses Markdown files from the frontend/docs/ directory.
"""

import re
from pathlib import Path
from typing import Optional

import frontmatter


class MarkdownDocument:
    """Represents a parsed Markdown document."""

    def __init__(
        self,
        file_path: Path,
        content: str,
        metadata: dict[str, any],
    ):
        self.file_path = file_path
        self.content = content
        self.metadata = metadata
        self.title = metadata.get("title", file_path.stem)
        self.module_id = self._extract_module_id()
        self.chapter_id = self._extract_chapter_id()

    def _extract_module_id(self) -> str:
        """Extract module ID from file path (e.g., 'module-01-ros2')."""
        parts = self.file_path.parts
        for part in parts:
            if part.startswith("module-"):
                return part
        return "unknown-module"

    def _extract_chapter_id(self) -> str:
        """Extract chapter ID from file path."""
        return self.file_path.stem

    def get_sections(self) -> dict[str, str]:
        """
        Extract sections from Markdown content.

        Returns a dict mapping section types to their content.
        Expected sections: concepts, architectures, algorithms, real-world
        """
        sections = {}

        # Split by H2 headers (##)
        pattern = r"^##\s+(.+?)$"
        matches = list(re.finditer(pattern, self.content, re.MULTILINE))

        for i, match in enumerate(matches):
            section_title = match.group(1).strip().lower()
            start_pos = match.end()

            # Find content until next H2 or end of document
            if i + 1 < len(matches):
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(self.content)

            section_content = self.content[start_pos:end_pos].strip()

            # Map section titles to standardized types
            section_type = self._normalize_section_type(section_title)
            if section_type:
                sections[section_type] = section_content

        return sections

    def _normalize_section_type(self, title: str) -> Optional[str]:
        """Normalize section title to one of the four standard types."""
        title_lower = title.lower()

        if "concept" in title_lower or "foundation" in title_lower or "introduction" in title_lower:
            return "concepts"
        elif "architecture" in title_lower or "design" in title_lower or "structure" in title_lower:
            return "architectures"
        elif "algorithm" in title_lower or "implementation" in title_lower or "technique" in title_lower:
            return "algorithms"
        elif "real-world" in title_lower or "practical" in title_lower or "application" in title_lower or "consideration" in title_lower:
            return "real-world"

        return None


class MarkdownParser:
    """Parser for reading Markdown documents from the docs directory."""

    def __init__(self, docs_root: Path):
        """
        Initialize parser.

        Args:
            docs_root: Root directory containing documentation (e.g., frontend/docs/)
        """
        self.docs_root = Path(docs_root)
        if not self.docs_root.exists():
            raise ValueError(f"Docs root does not exist: {self.docs_root}")

    def parse_all_documents(self) -> list[MarkdownDocument]:
        """
        Parse all Markdown documents in the docs directory.

        Returns:
            List of MarkdownDocument instances
        """
        documents = []

        # Find all .md files recursively
        for md_file in self.docs_root.rglob("*.md"):
            # Skip index files if they don't contain substantial content
            if md_file.name == "index.md":
                continue

            try:
                doc = self.parse_document(md_file)
                documents.append(doc)
            except Exception as e:
                print(f"Warning: Failed to parse {md_file}: {e}")

        return documents

    def parse_document(self, file_path: Path) -> MarkdownDocument:
        """
        Parse a single Markdown document.

        Args:
            file_path: Path to the Markdown file

        Returns:
            MarkdownDocument instance
        """
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        return MarkdownDocument(
            file_path=file_path.relative_to(self.docs_root),
            content=post.content,
            metadata=post.metadata,
        )

    def get_module_directories(self) -> list[Path]:
        """
        Get all module directories (e.g., module-01-ros2, module-02-simulation).

        Returns:
            List of module directory paths
        """
        modules = []
        for item in self.docs_root.iterdir():
            if item.is_dir() and item.name.startswith("module-"):
                modules.append(item)
        return sorted(modules)
