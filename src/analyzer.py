from collections import Counter


def analyze_logs(entries: list[dict], top_n: int = 5) -> dict:
    total_requests = len(entries)

    unique_ips = len({entry["ip"] for entry in entries})

    status_counts = Counter(entry["status"] for entry in entries)

    client_errors = sum(
        count
        for status, count in status_counts.items()
        if 400 <= status < 500
    )

    server_errors = sum(
        count
        for status, count in status_counts.items()
        if 500 <= status < 600
    )

    endpoint_counts = Counter(
        entry["endpoint"]
        for entry in entries
    )

    ip_counts = Counter(
        entry["ip"]
        for entry in entries
    )

    error_endpoint_counts = Counter(
        entry["endpoint"]
        for entry in entries
        if entry["status"] >= 400
    )

    return {
        "total_requests": total_requests,
        "unique_ips": unique_ips,
        "client_errors": client_errors,
        "server_errors": server_errors,
        "status_counts": dict(status_counts),
        "top_endpoints": endpoint_counts.most_common(top_n),
        "top_error_endpoints": error_endpoint_counts.most_common(top_n),
        "top_ips": ip_counts.most_common(top_n),
    }