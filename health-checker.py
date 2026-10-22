
import socket
from urllib.request import urlopen
from time import perf_counter
from urllib.error import HTTPError, URLError
from datetime import datetime
import argparse


# define a reusable function for saving the log timestamp

def save_result(message):
    # Get the current local date and time, formatted as readable text
    checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Open the log file in append mode.
# Python creates the file if it does not exist

    with open("health-checks.log", "a", encoding="utf-8") as log_file:
            # Write one line containing the hostname, status, and response time.
        log_file.write(
            f"{checked_at} | {message} \n"
        )


# Ask for a hostname, such as ngugi-portfolio.duckdns.org.
# input() returns what the user types as a string.
# strip() removes spaces from the beginning and end.
#
# hostname = input("Enter Your Website Hostname: ").strip()
#create a parser for reading the command-line arguements.

parser = argparse.ArgumentParser(
    description="Check's a website DNs, HTTP status and response time."
)

#Require a hostname when one runs the prograxm
parser.add_argument(
    "hostname",
    help="Website's hostname only, such as example.com"
)

#Read the arguments passed in the terminal.
args = parser.parse_args()

#Read the hostname passed and remove any whitespaces.
hostname = args.hostname.strip()

# An empty string is considered false in Python.
# This also catches input containing only spaces because of strip().
if not hostname:
    print("Please enter a website hostname")

    # Stop the program with exit code 1, indicating failure.
    raise SystemExit(1)


# Attempt to find an IPv4 address for the hostname.
try:
    ip_address = socket.gethostbyname(hostname)
    print("IP_Adress: ", ip_address)

# If the lookup fails, handle the error instead of showing a traceback.
# "as error" stores the exception so we can print its details.
except socket.gaierror as error:
    print("DNS lookup failed for: ", hostname)
    print("Reason: ", error)
    save_result(f"{hostname} | DNS FAILED | {error}")
    raise SystemExit(1)


# Build a complete URL by joining three strings.
# Example: "https://" + "example.com" + "/" becomes
# "https://example.com/"
url = "https://" + hostname + "/"
print("Requested url: ", url)


# Record the timer's value immediately before making the request.
# perf_counter() measures seconds; it does not provide a date or clock time.
start_time = perf_counter()

try:
    # Send a request to the URL.
    # timeout=10 sets a timeout for blocking network operations;
    # it is not a ten-second deadline for the entire program.
    # "as response" gives the returned response the name "response".
    # The with block closes the response automatically when we leave it.
    # raise TimeoutError("SIMULATED timeout for practice")
    with urlopen(url, timeout=10) as response:

        # Record the timer after urlopen() returns the response.
        end_time = perf_counter()

        # Read the HTTP status code, for example 200.
        status_code = response.status

# Handle HTTP error responses, such as 404 or 500.
# HTTPError must come before URLError because it is a type of URLError.
except HTTPError as error:
    print("HTTP request failed")
    print("HTTP status: ", error.code)
    print("Reason: ", error.reason)
    # Save the HTTP status and its explanation before stopping.
    save_result(f"{hostname} | HTTP {error.code} | {error.reason}")
    raise SystemExit(1)

# Handle connection problems, such as the refusal we tested.
# error.reason contains the underlying explanation.
except URLError as error:
    print("Web request failed: ", error.reason)
    # Save the underlying reason before stopping.
    save_result(f"{hostname} | Request Failed | {error.reason}")
    raise SystemExit(1)

except TimeoutError as error:
    print("Request timed out: ", error )

    # Record timeouts that are raised directly as TimeoutError.
    save_result(f"{hostname} | Request Timed Out | {error}")
    raise SystemExit(1)

# Subtract the timer readings to calculate elapsed seconds.
# Multiply by 1000 to convert seconds into milliseconds.
# This measures the request until the response headers are received;
# it does not measure downloading the full page or loading it in a browser.
response_time_ms = (end_time - start_time) * 1000

# These lines run only if the request reached this point successfully.
print("HTTPS Status: ", status_code)

# Round the result to two decimal places for easier reading.
print("Response time (ms): ", round(response_time_ms, 2))

# Call the function, passing this check's result as its message.
save_result(
    f"{hostname} | HTTP {status_code} | {response_time_ms:.2f} ms"
)





print("Result saved in the health-checks.log")