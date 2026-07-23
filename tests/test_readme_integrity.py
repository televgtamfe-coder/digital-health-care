import hashlib
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPOSITORY_ROOT / "README.md"

# README content from commit 5db4de5, before the faulty layout commit.
EXPECTED_README_SHA256 = (
    "129e0445dbf7aaf3ff06a979e872b8265ecbd4dca53d389631d7012e0f8eae1a"
)


class ReadmeIntegrityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = README_PATH.read_bytes()
        cls.text = cls.raw.decode("utf-8")

    def test_readme_matches_restoration_target(self):
        self.assertEqual(
            hashlib.sha256(self.raw).hexdigest(),
            EXPECTED_README_SHA256,
            "README.md no longer matches the approved pre-layout version",
        )

    def test_heading_hierarchy_is_restored(self):
        expected_counts = {1: 1, 2: 5, 3: 28, 4: 15}
        for level, expected in expected_counts.items():
            pattern = rf"^{'#' * level} "
            self.assertEqual(
                len(re.findall(pattern, self.text, flags=re.MULTILINE)),
                expected,
                f"unexpected level-{level} heading count",
            )

        self.assertNotIn("<details", self.text)
        self.assertNotIn("<summary", self.text)
        self.assertNotIn("<h1", self.text)

    def test_mermaid_blocks_are_present_and_balanced(self):
        mermaid_blocks = re.findall(
            r"```mermaid\n(.*?)\n```", self.text, flags=re.DOTALL
        )
        self.assertEqual(len(mermaid_blocks), 6)
        self.assertEqual(self.text.count("```"), 12)

        expected_diagram_types = [
            "flowchart LR",
            "timeline",
            "mindmap",
            "flowchart TB",
            "sequenceDiagram",
            "flowchart LR",
        ]
        actual_diagram_types = [
            next(line.strip() for line in block.splitlines() if line.strip())
            for block in mermaid_blocks
        ]
        self.assertEqual(actual_diagram_types, expected_diagram_types)

    def test_local_markdown_links_resolve(self):
        destinations = re.findall(r"\[[^\]]+\]\(([^)]+)\)", self.text)
        self.assertEqual(len(destinations), 3)

        local_destinations = [
            destination
            for destination in destinations
            if not destination.startswith(("http://", "https://", "#"))
        ]
        self.assertEqual(len(local_destinations), 2)

        for destination in local_destinations:
            target = (REPOSITORY_ROOT / destination).resolve()
            self.assertTrue(target.is_file(), f"missing README link target: {destination}")


if __name__ == "__main__":
    unittest.main()
