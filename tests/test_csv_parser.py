from src.csv_parser import parse_url_field


def test_parse_url_field_with_full_request():
    method, endpoint, protocol = parse_url_field(
        "GET /login.php HTTP/1.1"
    )

    assert method == "GET"
    assert endpoint == "/login.php"
    assert protocol == "HTTP/1.1"


def test_parse_url_field_without_protocol():
    method, endpoint, protocol = parse_url_field(
        "GET /login.php"
    )

    assert method == "GET"
    assert endpoint == "/login.php"
    assert protocol == ""


def test_parse_url_field_with_single_value():
    method, endpoint, protocol = parse_url_field(
        "/login.php"
    )

    assert method == ""
    assert endpoint == "/login.php"
    assert protocol == ""