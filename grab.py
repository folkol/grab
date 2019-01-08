#! /usr/bin/env python3
import argparse
import re
import sys

from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

PATTERNS = {
    'd': r'[0-9]+',
    'i': r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',
    'a': r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:["
         r"a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]["
         r"0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\["
         r"\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
    'e': r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|" r'"(?:['
         r'\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:['
         r'a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){'
         r'3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:['
         r'\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])',
    'q': r'"(?:[^"\\]|\\.)*"',
    'w': r'\S+',
    '[': r'\[[^\]]*\]'
}

parser = argparse.ArgumentParser(description='grabs tokens from lines of text.')
parser.add_argument('command',
                    action='store',
                    help='specifies what tokens to grab')
parser.add_argument('tokens',
                    nargs='?',
                    help='Which tokens to output (1-based, defaults to all)')
parser.epilog = ("token types: d=integer number, i=IP address, a=IP or domain name, e=email address, q=double quoted "
                 "string, w=word, [=square bracketed text ")
args = parser.parse_args()

indices = [int(c) for c in args.tokens or range(1, len(args.command) + 1)]

for line in sys.stdin:
    tokens = []
    for c in args.command:
        pattern = PATTERNS[c]
        match = re.search(pattern, line)
        if match:
            begin, end = match.span()
            tokens.append(line[begin: end])
            line = line[end:]

    output = []
    for i in indices:
        try:
            output.append(tokens[i - 1])
        except IndexError:
            pass

    output = '\t'.join(output)
    if output:
        print(output)
