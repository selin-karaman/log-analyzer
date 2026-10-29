from src.parser import parse_log_line


def test_parse_valid_log_line():
    line = (
        '192.168.1.10 - - [19/Oct/2026:14:01:12 +0300] '
        '"GET /api/users HTTP/1.1" 200 1240'
    )

    result = parse_log_line(line)

    assert result is not None
    assert result["ip"] == "192.168.1.10"
    assert result["method"] == "GET"
    assert result["endpoint"] == "/api/users"
    assert result["protocol"] == "HTTP/1.1"
    assert result["status"] == 200
    assert result["size"] == 1240


def test_parse_invalid_log_line():
    line = "this is not a valid access log"

    result = parse_log_line(line)

    assert result is None