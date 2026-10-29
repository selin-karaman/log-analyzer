import argparse
from pathlib import Path

from src.analyzer import analyze_logs
from src.csv_parser import parse_csv_file
from src.parser import parse_log_file
from src.reporter import generate_text_report, save_reports


SUPPORTED_EXTENSIONS = {".log", ".txt", ".csv"}


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

    log_path = Path(args.log_file)

    if not log_path.exists():
        print(f"Error: file not found: {args.log_file}")
        return

    if not log_path.is_file():
        print(f"Error: path is not a file: {args.log_file}")
        return

    file_extension = log_path.suffix.lower()

    if file_extension not in SUPPORTED_EXTENSIONS:
        print(
            "Error: unsupported file format. "
            "Supported formats: .log, .txt, .csv"
        )
        return

    if args.top <= 0:
        print("Error: --top must be greater than 0.")
        return

    if log_path.stat().st_size == 0:
        print("Error: input file is empty.")
        return

    parsing_stats = None

    try:
        if file_extension == ".csv":
            entries, parsing_stats = parse_csv_file(str(log_path))
        else:
            entries = parse_log_file(str(log_path))

    except (OSError, UnicodeDecodeError) as error:
        print(f"Error: could not read log file: {error}")
        return

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

    try:
        save_reports(
            analysis,
            output_directory=args.output
        )

    except OSError as error:
        print(f"\nError: could not save reports: {error}")
        return

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