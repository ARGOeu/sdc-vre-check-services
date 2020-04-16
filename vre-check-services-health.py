#!/usr/bin/python

import json
import sys
import requests
import argparse

# ##############################################################################
# VRE Check Services health#
# ##############################################################################


def ValidateValues(arguments):
    """ Validate values - input values """

    if arguments.timeout <= 0:
        print("\nInvalid timeout value: %s\n" % arguments.timeout)
        print_help()
        exit()
    if arguments.svre is None:
        print("\nNo service provided\n")
        print_help()
        exit()
    if arguments.hostname is None:
        print("\nNo hostname provided\n")
        print_help()
        exit()
    if not arguments.hostname.startswith("http"):
        print("\nNo schema supplied with hostname, did you mean https://%s?\n" % arguments.hostname)
        print_help()
        exit()


def print_help():
    """ Print help values."""

    print("usage: sdc-vre-check-services.py -H  -r")
    print("--- ---- ---- ---- ---- ---- ----\n")
    print("main arguments:")
    print("-H hostname")
    print("\n")
    print("optional arguments:")
    print(" -h, --help  show this help message and exit")
    print("-s vre service to check")
    print("-t timeout")
    print("-v verbose")


def debugValues(arguments):
    """ Print debug values.
        Args:
            arguments: the input arguments
    """
    if arguments.debug:
        print("[debugValues] - hostname: %s" % arguments.hostname)
    if arguments.svre != '':
        print("[debugValues] - svre: %s" % arguments.svre)
    if arguments.timeout != '':
        print("[debugValues] - timeout: %s" % arguments.timeout)


def checkHealth(URL, arguments):
    """ Check service status.
        Args:
           URL : service hostname
           timeout : how long should we wait for a response from the server
    """
    response = None
    u = URL + "healthcheck.json"

    if arguments.debug:
        print("[debugValues] - finalPath: %s" % u)
    timeout = arguments.timeout
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url=u, timeout=timeout, headers=headers)

    # ERROR handling
    except requests.exceptions.SSLError:
        description = "WARNING - Invalid SSL certificate"
        exit_code = 1
        return description, exit_code
    except requests.exceptions.ConnectionError:
        description = "CRITICAL - Service unreachable"
        exit_code = 2
        return description, exit_code
    except Exception as e:
        description = 'UNKNOWN - {0}'.format(str(e))
        exit_code = 3
        return description, exit_code

    if response is None:
        description = "UNKNOWN - Status unknown"
        exit_code = 3
        return description, exit_code

    if response.status_code == 404:
        description = "CRITICAL - Endpoint health check  not found"
        exit_code = 2
        return description, exit_code
    if response.status_code != 200:
        description = "WARNING - Unexpected status code %s" % response.status_code
        exit_code = 1
        return description, exit_code

    content = response.json()
    if arguments.debug:
        print content

    todos = json.loads(response.text)

    serviceToCheck = arguments.svre
    errors = 0
    servicesUnhealthy = ""
    if len(todos) < 2:
        description = "CRITICAL - Service " + serviceToCheck + " is not healthy and maybe all the services or docker are down"
        exit_code = 1
        return description, exit_code

    for key, value in todos.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if serviceToCheck in key:
            if "healthy" in value:
                description = "OK - Service reachable"
                exit_code = 0
            else:
                errors = errors + 1
                servicesUnhealthy = servicesUnhealthy + " , " + key

    if errors > 0:
        description = "CRITICAL - Service " + serviceToCheck + " is not healthy. Check " + servicesUnhealthy
        exit_code = 1
        return description, exit_code

    description = "OK - Service reachable"
    exit_code = 0
    return description, exit_code


def printResult(description, exit_code):
    """ Print the predefined values
        Args:
            description: the nagios description
            exit_code: the code that should be returned to nagios
    """

    print(description)
    sys.exit(exit_code)


def main():

    parser = argparse.ArgumentParser(description='Replication Manager probe '
                                                 'Supports healthcheck.')
    parser.add_argument("--hostname", "-H", help='The Hostname of Replication service')
    parser.add_argument("--svre", "-s")
    parser.add_argument("--timeout", "-t", metavar="seconds", help="Timeout in seconds. Must be greater than zero", type=int, default=30)
    parser.add_argument("--verbose", "-v", dest='debug', help='Set verbosity level', action='count', default=0)

    arguments = parser.parse_args()

    ValidateValues(arguments)

    if arguments.debug:
        debugValues(arguments)
    URL = arguments.hostname

    description, exit_code = checkHealth(URL, arguments)
    printResult(description, exit_code)

if __name__ == "__main__":
    main()
