import argparse

from src.parser import parse_log_file
from src.analyzer import analyze_logs
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

    args = parser.parse_args()

    entries = parse_log_file(args.log_file)

    if not entries:
        print("No valid log entries found.")
        return

    analysis = analyze_logs(entries, top_n=args.top)

    print(generate_text_report(analysis))

    save_reports(
        analysis,
        output_directory=args.output
    )

    print("\nReports created:")
    print(f"  {args.output}/summary.txt")
    print(f"  {args.output}/analysis.json")


if __name__ == "__main__":
    main()