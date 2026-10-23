import csv
from datetime import datetime


def parse_url_field(url_field: str) -> tuple[str, str, str]:
    parts = url_field.strip().split()

    if len(parts) >= 3:
        method = parts[0]
        protocol = parts[-1]
        endpoint = " ".join(parts[1:-1])

    elif len(parts) == 2:
        method = parts[0]
        endpoint = parts[1]
        protocol = ""

    else:
        method = ""
        endpoint = url_field.strip()
        protocol = ""

    return method, endpoint, protocol


def parse_csv_file(file_path: str) -> tuple[list[dict], dict]:
    entries = []

    total_rows = 0
    skipped_rows = 0
    skipped_examples = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_rows += 1

            try:
                method, endpoint, protocol = parse_url_field(row["URL"])

                timestamp = datetime.strptime(
                    row["Time"].strip(),
                    "[%d/%b/%Y:%H:%M:%S"
                )

                entry = {
                    "ip": row["IP"].strip(),
                    "timestamp": timestamp,
                    "method": method,
                    "endpoint": endpoint,
                    "protocol": protocol,
                    "status": int(row["Staus"]),
                    "size": None,
                }

                entries.append(entry)

            except (ValueError, KeyError, TypeError) as error:
                skipped_rows += 1

                if len(skipped_examples) < 5:
                    skipped_examples.append(
                        {
                            "row": row,
                            "error": str(error),
                        }
                    )

    parsing_stats = {
        "total_rows": total_rows,
        "parsed_rows": len(entries),
        "skipped_rows": skipped_rows,
        "skipped_examples": skipped_examples,
    }

    return entries, parsing_stats