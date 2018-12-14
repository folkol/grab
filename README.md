# Grab — a unix filter for extracting parts of the line

Grabs specified tokens from lines on stdin.

`usage: grab.py [-h] command [tokens]`

Each character in `command` specifies a token, `grab` will scan the input line for each token, and output them tab-separated.

If `tokens` is specified, only these tokens are printed (1-indexed). Indices are numbers from 0–9.

## Examples

- grab first two numbers: `grab dd`
- grab quoted string and number: `grab qd`
- grab three numbers, print them in reverse order: `grab ddd 321`

## Known tokens

- *d* (integer)
- *i* (IPv4) address)
- *e* (email address)
- *q* (double-quoted string)
- *w* (word)
- *[* (square-bracketed expression)
