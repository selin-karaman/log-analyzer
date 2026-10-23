import argparse
from pathlib import Path

from src.analyzer import analyze_logs
from src.csv_parser import parse_csv_file
from src.parser import parse_log_file
from src.reporter import generate_text_report, save_reports


def main():
    parser = argparse.ArgumentParser(
        description="Analyze server access log files."
    )

    parser.add_argument(
        "log_file",
        help="Path to the log file to analyze"
    )

    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of top results to display (default: 5)"
    )

    parser.add_argument(
        "--output",
        default="reports",
        help="Directory where reports will be saved (default: reports)"
    )

    parser.add_argument(
        "--show-skipped",
        action="store_true",
        help="Show examples of skipped malformed rows"
    )

    args = parser.parse_args()

    file_extension = Path(args.log_file).suffix.lower()

    parsing_stats = None

    if file_extension == ".csv":
        entries, parsing_stats = parse_csv_file(args.log_file)
    else:
        entries = parse_log_file(args.log_file)

    if not entries:
        print("No valid log entries found.")
        return

    analysis = analyze_logs(
        entries,
        top_n=args.top
    )

    if parsing_stats:
        print("Parsing Summary\n")
        print(
            f"Rows processed: "
            f"{parsing_stats['total_rows']}"
        )
        print(
            f"Successfully parsed: "
            f"{parsing_stats['parsed_rows']}"
        )
        print(
            f"Skipped malformed rows: "
            f"{parsing_stats['skipped_rows']}"
        )
        print()

    print(generate_text_report(analysis))

    save_reports(
        analysis,
        output_directory=args.output
    )

    print("\nReports created:")
    print(f"  {args.output}/summary.txt")
    print(f"  {args.output}/analysis.json")

    if (
        args.show_skipped
        and parsing_stats
        and parsing_stats.get("skipped_examples")
    ):
        print("\nSkipped row examples:")

        for example in parsing_stats["skipped_examples"]:
            print(f"  Row: {example['row']}")
            print(f"  Error: {example['error']}")


if __name__ == "__main__":
    main()