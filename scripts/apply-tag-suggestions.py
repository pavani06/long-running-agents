#!/usr/bin/env python3
"""
Apply tag suggestions from curriculum/tag-suggestions.yaml to markdown files.

Reads the YAML suggestions file, then for each entry:
1. Reads the target markdown file
2. Extracts the YAML frontmatter (between first and second ---)
3. Merges suggested_new_tags into the existing tags array (additive, no duplicates)
4. Writes back preserving all other frontmatter formatting
"""

import re
import sys
from pathlib import Path

import yaml


def load_suggestions(suggestions_path: str) -> list[dict]:
    """Load the tag-suggestions.yaml file."""
    with open(suggestions_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    entries = []
    for key, value in data.items():
        if key.startswith("/"):
            entries.append(
                {
                    "path": key,
                    "current_tags": value.get("current_tags", []),
                    "suggested_new_tags": value.get("suggested_new_tags", []),
                }
            )
    return entries


def update_frontmatter_tags(content: str, suggested_new_tags: list[str]) -> tuple[str, bool]:
    """
    Update the tags list in YAML frontmatter.

    Returns (updated_content, was_modified).
    """
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content, False

    frontmatter = parts[1]
    body = parts[2]

    # Parse existing tags
    tags_match = re.search(r"^tags:\s*\[(.*?)\]", frontmatter, re.MULTILINE)
    if not tags_match:
        # Try multi-line YAML array
        tags_match = re.search(r"^tags:\s*\n((?:\s+-\s+.+\n?)*)", frontmatter, re.MULTILINE)
        if not tags_match:
            print(f"  WARNING: Could not find tags: in frontmatter", file=sys.stderr)
            return content, False

        # Multi-line format
        existing_tags = [line.strip().lstrip("- ").strip() for line in tags_match.group(1).strip().split("\n") if line.strip().startswith("-")]
        all_tags = list(dict.fromkeys(existing_tags + [t for t in suggested_new_tags if t not in existing_tags]))

        # Rebuild tags in multi-line format
        new_tags_block = "tags:\n" + "\n".join(f"  - {tag}" for tag in all_tags)
        new_frontmatter = frontmatter[:tags_match.start()] + new_tags_block + frontmatter[tags_match.end():]
    else:
        # Single-line array format: tags: [tag1, tag2]
        inner = tags_match.group(1)
        existing_tags = [t.strip().strip("'\"") for t in inner.split(",") if t.strip()]
        all_tags = list(dict.fromkeys(existing_tags + [t for t in suggested_new_tags if t not in existing_tags]))

        new_tags_line = f"tags: [{', '.join(all_tags)}]"
        new_frontmatter = frontmatter[:tags_match.start()] + new_tags_line + frontmatter[tags_match.end():]

    if new_frontmatter == frontmatter:
        return content, False

    updated = f"---{new_frontmatter}---{body}"
    return updated, True


def main():
    repo_root = Path(__file__).resolve().parents[1]
    suggestions_path = repo_root / "curriculum" / "tag-suggestions.yaml"

    if not suggestions_path.exists():
        print(f"ERROR: {suggestions_path} not found", file=sys.stderr)
        sys.exit(1)

    entries = load_suggestions(str(suggestions_path))
    print(f"Loaded {len(entries)} entries from tag-suggestions.yaml\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for entry in entries:
        file_path = entry["path"]
        suggested = entry["suggested_new_tags"]

        if not Path(file_path).exists():
            print(f"SKIP (not found): {file_path}")
            skipped_count += 1
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()

        updated, modified = update_frontmatter_tags(original, suggested)

        if not modified:
            print(f"SKIP (no change): {file_path}")
            skipped_count += 1
            continue

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated)

        added = [t for t in suggested if t not in entry["current_tags"]]
        print(f"  OK {Path(file_path).name} (+{len(added)} tags)")
        updated_count += 1

    print(f"\n---")
    print(f"Updated: {updated_count} files")
    print(f"Skipped: {skipped_count} files")
    print(f"Errors:  {error_count} files")

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
