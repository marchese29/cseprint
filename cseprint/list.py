"""List all of the printers available on your subdomain."""
import argparse
import getpass
import re
import subprocess
import sys

def get_printers(args):
    """Retrieve a list of all printers returned by the lpstat command along with their status.
    Return format: [(name, status)].
    """
    printer_pattern = re.compile(r'printer (?P<printer>\w+) is (?P<status>[a-z]+)')
    result = []

    try:
        response = subprocess.check_output(
            ['ssh', args.user + '@' + args.domain + '.cse.ohio-state.edu', 'lpstat', '-p'])
    except subprocess.CalledProcessError as cpe:
        sys.exit('There was an error listing printers: %s' % str(cpe))

    for match in printer_pattern.finditer(response):
        result.append( (match.group('printer'), match.group('status')) )

    return result

def setup_args():
    """Configure the command line arguments."""
    parser = argparse.ArgumentParser(description='List the printers in your subdomain.')

    # Positional arguments
    parser.add_argument('domain', choices=['faclinux', 'stdlinux'],
                        help='The subdomain in question')

    # Optional arguments
    parser.add_argument('--user', required=False,
                        help='stdlinux/faclinux username if different from your local one')
    parser.add_argument('--version', action='version', version='%(prog)s 1.1')

    return parser.parse_args()

def main():
    """The main entry point for the program."""
    args = setup_args()
    args.user = args.user if args.user is not None else getpass.getuser()

    responses = get_printers(args)
    statuses = set(map(lambda x: x[1], responses))
    for status in statuses:
        print '%s printers:' % status
        for printer in [p for (p, s) in responses if s == status]:
            print '\t%s' % printer
        print ''

    return 0

if __name__ == '__main__':
    sys.exit(main())