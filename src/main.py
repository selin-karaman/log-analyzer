from src.parser import parse_log_file


def main():
    log_file = "data/sample.log"

    entries = parse_log_file(log_file)

    print(f"Parsed {len(entries)} log entries.\n")

    for entry in entries:
        print(entry)


if __name__ == "__main__":
    main()