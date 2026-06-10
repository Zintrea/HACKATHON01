#!/usr/bin/env python3
"""CLI entrypoint for H1 Dorm code.

Example:
    python3 run_analysis.py ../../cart_web.log --output output
    python3 run_analysis.py ../../cart_web.log --output output_debug --max-lines 100000
"""
from __future__ import annotations

import argparse
from pathlib import Path

from h1_analyzer.runner import run_analysis


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze H1 cart_web.log and generate dashboard-ready outputs.")
    parser.add_argument("log_path", type=Path, help="Path to cart_web.log or a sample log file")
    parser.add_argument("--output", type=Path, default=Path("output"), help="Output directory for CSV/JSON/Markdown files")
    parser.add_argument("--max-lines", type=int, default=None, help="Debug mode: analyze only first N lines")
    args = parser.parse_args()

    summary = run_analysis(args.log_path, args.output, max_lines=args.max_lines)
    print("H1 analysis completed")
    print(f"parsed_lines={summary['parsed_lines']}")
    print(f"malformed_lines={summary['malformed_lines']}")
    print(f"unique_ips={summary['unique_ips']}")
    print(f"suspicious_ips={summary['suspicious_ips']}")
    print(f"output_dir={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
