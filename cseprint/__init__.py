"""This file provides everything the script needs.  The main entry point for the program is main()
"""
import argparse
import getpass
import os
import re
import subprocess
import sys

def is_valid_printer(args):
    """Validates that the state of the arguments provide a valid printer."""
    pattern = re.compile(r'printer (%s) is (?P<status>[a-z]+)' % args.printer.lower())

    try:
        result = subprocess.check_output(
            ['ssh', args.user + '@' + args.domain + '.cse.ohio-state.edu', 'lpstat', '-p'])
    except subprocess.CalledProcessError as cpe:
        print >>sys.stderr, 'There was an error listing printers: %s' % str(cpe)
        raise cpe

    match = pattern.search(result)
    if match:
        if match.group('status') == 'disabled':
            print '%s is disabled.' % args.printer
            return False
        else:
            return True
    else:
        print >>sys.stderr, 'Could not find the printer "%s"' % args.printer

def setup_args():
    """Configures the command line arguments, parses and returns them."""
    parser = argparse.ArgumentParser(description='Print anything you want to any cse printer.')

    parser.add_argument('domain', choices=['faclinux', 'stdlinux'],
                        help='Subdomain you are printing to.')
    parser.add_argument('printer', help='Printer you would like to send to.')
    parser.add_argument('file', help='The file to send to the printer.')

    # Allow the user to override their username
    parser.add_argument('--user', required=False,
                        help='stdlinux/faclinux username if different from your local one.')

    # Allow verbose logging
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging.')

    # Special printing options
    parser.add_argument('--double-sided', action='store_true', help='Print double-sided sheets.')

    # Show a list of available printers
    parser.add_argument('--list', action='store_true', help='List the printers available to you.')

    # Version printing
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.2')

    return parser.parse_args()

def main():
    """The main entry point for the function."""
    # Configure the script from the command line arguments
    args = setup_args()
    args.user = args.user if args.user is not None else getpass.getuser()

    # Validate that the file exists
    if not os.path.isfile(os.path.expanduser(args.file)):
        sys.exit('%s is not a valid file.' % args.file)

    # Complain about non-pdf files.
    if args.file.split('.')[-1] != 'pdf':
        response = raw_input(
            'The file you provided is not a pdf, would you like to continue anyways (y/n) ')
        if response != 'Y' and response != 'y':
            sys.exit(0)

    # Validate that the file can be opened
    if args.verbose:
        print 'Validating the provided file.'
    try:
        handle = open(os.path.expanduser(args.file), 'rb')
    except (OSError, IOError):
        sys.exit('%s could not be opened.' % args.file)
    finally:
        handle.close()

    # Validate that the user exists
    if args.verbose:
        print 'Validating the username: %s' % args.user
    try:
        subprocess.check_call(
            ['ssh', args.user + '@' + args.domain + '.cse.ohio-state.edu', 'exit'])
    except subprocess.CalledProcessError:
        sys.exit('Failed to connect over ssh, is your username valid?')

    # Validate that the printer exists
    if args.verbose:
        print 'Validating the provided printer.'
    try:
        if not is_valid_printer(args):
            sys.exit(1)
    except subprocess.CalledProcessError:
        sys.exit(1)

    command = 'ssh {user}@{domain}.cse.ohio-state.edu lp -d {printer} '.format(
        user=args.user, domain=args.domain, printer=args.printer)
    if args.double_sided:
        command += '-o sides=two-sided-long-edge '
    command += '- < {file}'.format(file=args.file)

    if args.verbose:
        print 'Queuing up print job.'
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    main()
