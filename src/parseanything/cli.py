"""Command Line Interface for ParseAnything engine."""

import argparse
import os
import json
from parseanything.pipeline import ParseAnythingEngine


def main():
    parser = argparse.ArgumentParser(description="ParseAnything Engine: Extract clean structured text & tables from PDFs and Images.")
    parser.add_argument("input", help="Path to input PDF, PNG, or JPG file")
    parser.add_argument("-o", "--output", help="Output file path (e.g., output.md or output.json)")
    parser.add_argument("-f", "--format", choices=["markdown", "json"], default="markdown", help="Output format (default: markdown)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    engine = ParseAnythingEngine()
    doc = engine.parse_file(args.input)

    if args.format == "json":
        result = json.dumps(doc.model_dump(), indent=2)
    else:
        result = engine.document_to_markdown(doc)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Successfully processed '{args.input}' -> Saved to '{args.output}'")
    else:
        print(result)


if __name__ == "__main__":
    main()