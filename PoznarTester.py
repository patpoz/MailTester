import argparse
import csv
import os
import requests

from collections import defaultdict, OrderedDict
from enum import Enum
from time import sleep
from lxml import html


class STATUS(Enum):
    OK = 0
    INVALID_DOMAIN = 1
    NOT_ALLOWED = 2
    DOES_NOT_EXIST = 3
    UNKNOWN = 100


STATUS_NAMES_MAP = OrderedDict([
    (STATUS.OK, "Valid"),
    (STATUS.INVALID_DOMAIN, "Invalid domain"),
    (STATUS.NOT_ALLOWED, "Validation not allowed"),
    (STATUS.DOES_NOT_EXIST, "Email does not exist"),
    (STATUS.UNKNOWN, "Unknown error status"),
])

STATUS_MESSAGE_MAP = {
    "E-mail address is valid": STATUS.OK,
    "Invalid mail domain.": STATUS.INVALID_DOMAIN,
    "The domain is invalid or no mail server was found for it.": STATUS.INVALID_DOMAIN,
    "Server doesn't allow e-mail address verification": STATUS.NOT_ALLOWED,
    "E-mail address does not exist on this server": STATUS.DOES_NOT_EXIST,
}


def email_candidates(first_name, last_name, domain):
    yield "{first_name}.{last_name}{domain}".format(
        first_name=first_name, last_name=last_name, domain=domain)
    yield "{first_name}{last_name}{domain}".format(
        first_name=first_name, last_name=last_name, domain=domain)
    yield "{first_name_letter}.{last_name}{domain}".format(
        first_name_letter=first_name[0], last_name=last_name, domain=domain)
    yield "{first_name_letter}{last_name}{domain}".format(
        first_name_letter=first_name[0], last_name=last_name, domain=domain)
    yield "kontakt{domain}".format(domain=domain)
    yield "contact{domain}".format(domain=domain)


def validate_email(email):
    ok_color_status = "#00DD00"
    payload = {'lang': 'en', 'email': email}
    response = requests.post("http://mailtester.com/testmail.php", data=payload)
    response.raise_for_status()
    tree = html.fromstring(response.content)
    statuses = tree.xpath('//div[@id="content"]//table/tr[position()>1]/td[last()][@bgcolor]')
    if all(status.get("@bgcolor") == ok_color_status for status in statuses):
        # If all cells have green background, we assume that email is valid
        return STATUS.OK
    for status in statuses:
        if status.get("@bgcolor") == ok_color_status:
            # We only look for the first error message
            pass
        if status.text in STATUS_MESSAGE_MAP:
            # Return known error status
            return STATUS_MESSAGE_MAP[status.text]
    # Unknown error status
    return STATUS.UNKNOWN


def main(csv_reader, log_output, max_retries=3):
    emails_by_statuses = defaultdict(set)
    checked_emails = set()
    for first_name, last_name, domain in csv_reader:
        for email_candidate in email_candidates(first_name, last_name, domain):
            # Check all possible formats
            if email_candidate in checked_emails:
                # Avoid checking the same email twice
                continue
            email_status = None
            retries = 0
            while retries < max_retries:
                try:
                    email_status = validate_email(email_candidate)
                except requests.HTTPError as http_error:
                    # Repeat for n times until valid response
                    print("Cooldown for 3 seconds: {}".format(http_error))
                    retries += 1
                    if retries == max_retries:
                        break
                    sleep(3)
                else:
                    break
            if retries == max_retries:
                print("Failure after {} retries, skipping".format(retries))
            else:
                emails_by_statuses[email_status].add(email_candidate)
                checked_emails.add(email_candidate)
                if email_status == STATUS.OK:
                    print("Valid email: {}".format(email_candidate))
    for status, status_name in STATUS_NAMES_MAP.items():
        # Print all checked emails by statuses (starting with OK)
        # TODO: Better output formatting
        if status in emails_by_statuses:
            for email in emails_by_statuses[status]:
                log_output.write("{}: {}\n".format(status_name, email))
            print("{}: {} emails".format(status_name, len(emails_by_statuses[status])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input csv file")
    parser.add_argument("-o", "--output", default="results.log", help="Output log file")
    parser.add_argument("-r", '--retries', type=int, default=3, help="Max number of email validation retries")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print("{} cannot be found, exiting.".format(args.input))
        exit(1)

    with open(args.input, 'r') as input:
        with open(args.output, 'w') as output:
            csv_reader = csv.reader(input, delimiter=',')
            main(csv_reader, output, max_retries=args.retries)

    #TODO: Dodać kombinacje maili
    #TODO: Zrobić zapisywanie wyników do pliku w formie gotowej do wysyłki
