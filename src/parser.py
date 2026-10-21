import re
from datetime import datetime


LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<endpoint>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d{3}) '
    r'(?P<size>\d+)'
)


def parse_log_line(line: str) -> dict | None:
    match = LOG_PATTERN.match(line.strip())

    if not match:
        return None

    data = match.groupdict()

    return {
        "ip": data["ip"],
        "timestamp": datetime.strptime(
            data["timestamp"],
            "%d/%b/%Y:%H:%M:%S %z"
        ),
        "method": data["method"],
        "endpoint": data["endpoint"],
        "protocol": data["protocol"],
        "status": int(data["status"]),
        "size": int(data["size"]),
    }


def parse_log_file(file_path: str) -> list[dict]:
    entries = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parsed = parse_log_line(line)

            if parsed:
                entries.append(parsed)

    return entries