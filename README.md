# Website Health Checker

A beginner Python project that checks a website's DNS resolution,
HTTPS response status, and response time.

## Features

- Accepts a hostname as a command-line argument.
- Rejects empty input.
- Looks up an IPv4 address for the hostname.
- Sends an HTTPS request.
- Displays the HTTP status and request duration.
- Handles DNS failures, HTTP errors, connection problems, and direct timeouts.
- Saves successful checks and handled failures with timestamps.

## Requirements

- Python 3.13.5 — the version used for this project.
- Internet access for checking online websites.

The project uses Python's standard library, so no additional packages
need to be installed.

## How to run

Open a terminal in the project folder and provide a hostname:

```bash
py health-checker.py ngugi-portfolio.duckdns.org
```

Use a hostname without `https://` or a page path.

To display usage instructions:

```bash
py health-checker.py --help
```

## Saved results

Results are appended to `health-checks.log` in the folder where
you run the command.

Example entry:

```text
2026-10-22 14:16:46 | ngugi-portfolio.duckdns.org | HTTP 200 | 441.47 ms
```

Timestamps use the computer's local time.

## Current scope

The checker requests the website's HTTPS homepage. Its response time
measures the request until response headers arrive, rather than a full
page loading in a browser.