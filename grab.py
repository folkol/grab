#! /usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

TOKENS = {
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
    'Q': r"'(?:[^'\\]|\\.)*'",
    'w': r'\S+',
    '[': r'\[[^\]]*\]'
}

parser = argparse.ArgumentParser(description='grabs tokens from stdin (e.g. `grab qdd 13 <README`)',
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('command',
                    action='store',
                    help='specifies what tokens to grab')
parser.add_argument('tokens',
                    nargs='?',
                    help='Which tokens to output (1-based, defaults to all)')
parser.epilog = """
token types:
    d: integer number
    i: IP address
    a: IP or domain name
    e: email address
    q: single quoted string
    Q: double quoted string
    w: word
    [: square bracketed text

override or add token types:
    Add a json object with token name (single char) and corresponding regex to ~/.grab/tokens.json
"""
args = parser.parse_args()

additional_patterns = Path.home().joinpath('.grab').joinpath('tokens.json')
if additional_patterns.is_file():
    with open(str(additional_patterns)) as f:
        TOKENS = {**TOKENS, **json.load(f)}

indices = [int(c) for c in args.tokens or range(1, len(args.command) + 1)]

for line in sys.stdin:
    tokens = []
    for c in args.command:
        pattern = TOKENS[c]
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
        print(output, flush=True)
