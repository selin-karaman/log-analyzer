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

        peak_traffic = analysis["peak_traffic_hour"]

    if peak_traffic:
        hour, count = peak_traffic

        lines.append("")
        lines.append("Peak traffic hour:")
        lines.append(
            f"  {hour:02d}:00 - {(hour + 1) % 24:02d}:00 "
            f"({count} requests)"
        )

    peak_error = analysis["peak_error_hour"]

    if peak_error:
        hour, count = peak_error

        lines.append("")
        lines.append("Peak error hour:")
        lines.append(
            f"  {hour:02d}:00 - {(hour + 1) % 24:02d}:00 "
            f"({count} errors)"
        )

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