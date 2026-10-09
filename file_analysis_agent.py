import os
from collections import defaultdict
from typing import Dict, List, Tuple

def scan_directory(root_path: str) -> dict:
    if not os.path.isdir(root_path):
        raise ValueError(f"Not a directory: {root_path}")
    ext_counts = defaultdict(int)
    file_sizes: List[Tuple[int, str]] = []
    total_files = 0
    for dirpath, _, filenames in os.walk(root_path, followlinks=False):
        for fname in filenames:
            total_files += 1
            full_path = os.path.join(dirpath, fname)
            try:
                size = os.path.getsize(full_path)
            except OSError:
                size = 0
            file_sizes.append((size, full_path))
            _, ext = os.path.splitext(fname)
            ext = ext.lower() if ext else "(no extension)"
            ext_counts[ext] += 1
    largest = sorted(file_sizes, key=lambda x: x[0], reverse=True)[:5]
    return {"total_files": total_files, "extensions": dict(ext_counts), "largest_files": largest}

def format_report(result: dict) -> str:
    lines = [f"Total files: {result['total_files']}", ""]
    lines.append("File counts by extension:")
    for ext, count in sorted(result["extensions"].items()):
        lines.append(f"  {ext}: {count}")
    lines.append("")
    lines.append("Largest files:")
    for size, path in result["largest_files"]:
        lines.append(f"  {size:8d} bytes: {path}")
    return "\n".join(lines)

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python file_analysis_agent.py <directory>")
        sys.exit(1)
    try:
        print(format_report(scan_directory(sys.argv[1])))
    except Exception as e:
        print(f"Error: {e}"); sys.exit(1)
if __name__ == "__main__":
    main()
