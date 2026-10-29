from datetime import datetime

from src.analyzer import analyze_logs


def get_sample_entries():
    return [
        {
            "ip": "192.168.1.10",
            "timestamp": datetime(2026, 10, 19, 14, 1),
            "method": "GET",
            "endpoint": "/api/users",
            "protocol": "HTTP/1.1",
            "status": 200,
            "size": 1200,
        },
        {
            "ip": "192.168.1.11",
            "timestamp": datetime(2026, 10, 19, 14, 5),
            "method": "GET",
            "endpoint": "/api/payment",
            "protocol": "HTTP/1.1",
            "status": 500,
            "size": 900,
        },
        {
            "ip": "192.168.1.11",
            "timestamp": datetime(2026, 10, 19, 14, 10),
            "method": "GET",
            "endpoint": "/api/payment",
            "protocol": "HTTP/1.1",
            "status": 503,
            "size": 850,
        },
        {
            "ip": "192.168.1.12",
            "timestamp": datetime(2026, 10, 19, 15, 2),
            "method": "GET",
            "endpoint": "/missing-page",
            "protocol": "HTTP/1.1",
            "status": 404,
            "size": 300,
        },
    ]


def test_analyze_basic_counts():
    analysis = analyze_logs(get_sample_entries())

    assert analysis["total_requests"] == 4
    assert analysis["unique_ips"] == 3
    assert analysis["client_errors"] == 1
    assert analysis["server_errors"] == 2


def test_status_code_distribution():
    analysis = analyze_logs(get_sample_entries())

    assert analysis["status_counts"] == {
        200: 1,
        500: 1,
        503: 1,
        404: 1,
    }


def test_top_error_endpoint():
    analysis = analyze_logs(get_sample_entries())

    assert analysis["top_error_endpoints"][0] == (
        "/api/payment",
        2,
    )


def test_most_active_ip():
    analysis = analyze_logs(get_sample_entries())

    assert analysis["top_ips"][0] == (
        "192.168.1.11",
        2,
    )


def test_peak_traffic_hour():
    analysis = analyze_logs(get_sample_entries())

    assert analysis["peak_traffic_hour"] == (
        14,
        3,
    )


def test_peak_error_hour():
    analysis = analyze_logs(get_sample_entries())

    assert analysis["peak_error_hour"] == (
        14,
        2,
    )