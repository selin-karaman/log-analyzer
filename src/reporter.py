import json
from pathlib import Path


def generate_text_report(analysis: dict) -> str:
    lines = [
        "Log Analysis Summary",
        "",
        f"Total requests: {analysis['total_requests']}",
        f"Unique IPs: {analysis['unique_ips']}",
        f"4xx responses: {analysis['client_errors']}",
        f"5xx responses: {analysis['server_errors']}",
        "",
        "Status code distribution:",
    ]

    for status, count in sorted(analysis["status_counts"].items()):
        lines.append(f"  {status}: {count}")

    lines.append("")
    lines.append("Top endpoints:")

    for endpoint, count in analysis["top_endpoints"]:
        lines.append(f"  {endpoint}: {count}")

    lines.append("")
    lines.append("Top error endpoints:")

    for endpoint, count in analysis["top_error_endpoints"]:
        lines.append(f"  {endpoint}: {count}")

    lines.append("")
    lines.append("Most active IPs:")

    for ip, count in analysis["top_ips"]:
        lines.append(f"  {ip}: {count}")

    return "\n".join(lines)


def save_reports(
    analysis: dict,
    output_directory: str = "reports"
) -> None:
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)

    text_report = generate_text_report(analysis)

    with open(
        output_path / "summary.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(text_report)

    with open(
        output_path / "analysis.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(analysis, file, indent=4)