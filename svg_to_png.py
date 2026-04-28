#!/usr/bin/env python3
"""
Batch convert SVGs to PNGs using Inkscape CLI.
Usage: python svg_to_png.py <input_folder> [output_folder] [--dpi 96]
"""

import argparse
import subprocess
import sys
from pathlib import Path

import os
os.environ["PATH"] += r";C:\Program Files\Inkscape\bin"


def check_inkscape():
    """Verify Inkscape is installed and accessible."""
    try:
        result = subprocess.run(
            ["inkscape", "--version"],
            capture_output=True, text=True, check=True
        )
        print(f"Found: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("Error: Inkscape not found. Install it and ensure it's on your PATH.")
        print("  macOS:   brew install inkscape")
        print("  Ubuntu:  sudo apt install inkscape")
        print("  Windows: https://inkscape.org/release/")
        return False
    except subprocess.CalledProcessError:
        return False


def convert_svg(svg_path: Path, png_path: Path, dpi: int) -> bool:
    """Convert a single SVG to PNG using Inkscape."""
    cmd = [
        "inkscape",
        "--export-type=png",
        f"--export-filename={png_path}",
        f"--export-dpi={dpi}",
        str(svg_path),
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] {svg_path.name}: {e.stderr.strip() or 'unknown error'}")
        return False


def batch_convert(input_folder: str, output_folder: str | None, dpi: int):
    input_path = Path(input_folder).resolve()

    if not input_path.is_dir():
        print(f"Error: '{input_folder}' is not a valid directory.")
        sys.exit(1)

    svgs = sorted(input_path.glob("*.svg"))
    if not svgs:
        print(f"No SVG files found in '{input_path}'.")
        sys.exit(0)

    # Determine output directory
    out_path = Path(output_folder).resolve() if output_folder else input_path
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"\nInput  : {input_path}")
    print(f"Output : {out_path}")
    print(f"DPI    : {dpi}")
    print(f"Files  : {len(svgs)} SVG(s) found\n")

    success, failure = 0, 0

    for i, svg in enumerate(svgs, 1):
        png = out_path / (svg.stem + ".png")
        print(f"[{i}/{len(svgs)}] {svg.name} → {png.name} ... ", end="", flush=True)
        if convert_svg(svg, png, dpi):
            print("OK")
            success += 1
        else:
            failure += 1

    print(f"\nDone — {success} converted, {failure} failed.")


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert SVG files to PNG using Inkscape."
    )
    parser.add_argument("input_folder", help="Folder containing SVG files")
    parser.add_argument(
        "output_folder",
        nargs="?",
        default=None,
        help="Destination folder for PNGs (default: same as input)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=96,
        help="Export resolution in DPI (default: 96)",
    )
    args = parser.parse_args()

    if not check_inkscape():
        sys.exit(1)

    batch_convert(args.input_folder, args.output_folder, args.dpi)


if __name__ == "__main__":
    main()
