# Log Analyzer

A Python-based command-line tool for parsing and analyzing web server access logs.

The project supports both raw access log files and CSV-based web log datasets, and generates useful traffic and error statistics from the input data.

## Features

- Parse raw `.log` and `.txt` access log files
- Parse CSV-based web log datasets
- Count total requests and unique IP addresses
- Analyze HTTP status code distribution
- Analyze HTTP method distribution
- Calculate client-side and server-side error counts
- Calculate overall error rate
- Identify the most requested endpoints
- Identify the endpoints generating the most errors
- Identify the most active IP addresses
- Detect peak traffic hour
- Detect peak error hour
- Show the analyzed time range
- Skip malformed or non-log rows safely
- Optionally display examples of skipped rows
- Generate TXT and JSON reports
- Support configurable top result counts through the CLI
- Validate input paths and supported file formats

## Project Structure

```text
log-analyzer/
├── data/
│   ├── sample.log
│   └── weblog.csv
├── reports/
├── src/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── csv_parser.py
│   ├── main.py
│   ├── parser.py
│   └── reporter.py
├── tests/
│   ├── test_analyzer.py
│   ├── test_csv_parser.py
│   └── test_parser.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

Clone the repository and install the required dependency:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

Analyze a log file:

```bash
python3 -m src.main data/sample.log
```

Analyze a CSV dataset:

```bash
python3 -m src.main data/weblog.csv
```

Limit the number of top results:

```bash
python3 -m src.main data/weblog.csv --top 3
```

Save reports to a custom directory:

```bash
python3 -m src.main data/weblog.csv --output output
```

Display examples of malformed rows that were skipped during parsing:

```bash
python3 -m src.main data/weblog.csv --show-skipped
```

View all CLI options:

```bash
python3 -m src.main --help
```

## Example Output

```text
Parsing Summary

Rows processed: 16007
Successfully parsed: 15789
Skipped malformed rows: 218

Log Analysis Summary

Total requests: 15789
Unique IPs: 5
4xx responses: 251
5xx responses: 0
Error rate: 1.59%

HTTP method distribution:
  GET: 15098
  HEAD: 9
  POST: 682

Top endpoints:
  /login.php: 3298
  /home.php: 2653
  /js/vendor/modernizr-2.8.3.min.js: 1417

Peak traffic hour:
  20:00 - 21:00 (5458 requests)

Peak error hour:
  15:00 - 16:00 (32 errors)
```

## Reports

Each successful analysis generates:

```text
reports/
├── analysis.json
└── summary.txt
```

`summary.txt` contains a human-readable overview of the analysis.

`analysis.json` contains the same results in structured format for further processing or integration with other tools.

## Dataset

The project was tested using the **RUET OJ Web Log Dataset** from Kaggle.

The dataset contains web server activity including:

- client IP addresses
- request timestamps
- HTTP requests
- HTTP status codes

Some rows in the dataset contain malformed or non-web-log content. These rows are skipped during parsing and included in the parsing statistics.

## Testing

The project uses `pytest`.

Run all tests with:

```bash
python3 -m pytest -v
```

The test suite covers:

- raw access log parsing
- invalid log handling
- CSV request parsing
- HTTP status analysis
- error counting
- active IP detection
- top error endpoints
- peak traffic detection
- peak error detection

## Supported Formats

Currently supported input formats:

```text
.log
.txt
.csv
```

Raw `.log` and `.txt` files are expected to use an Apache/Nginx-style access log format.

CSV files are expected to follow the column structure used by the RUET OJ dataset.

## Limitations

- Raw log parsing currently targets a specific Apache/Nginx-style access log structure.
- CSV parsing currently expects the RUET OJ dataset column format.
- Malformed rows are skipped instead of being automatically repaired.
- The project currently focuses on access log analysis rather than application or system logs.

## Key Takeaways

This project demonstrates:

- parsing structured and semi-structured log data with Python
- working with real-world datasets containing malformed records
- extracting traffic and error metrics from server logs
- building a command-line interface with `argparse`
- generating machine-readable and human-readable reports
- implementing input validation and graceful error handling
- writing unit tests with `pytest`