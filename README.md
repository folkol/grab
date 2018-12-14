# Grab — a unix filter for extracting parts of the line

## Usecases

grab numbers from lines
grab dates from lines
grab quoted string from lines
grab urls from lines

## Roadmap

grab and destructure quoted string from line ('grab quoted string from access log, grab method and path from that string')

## Examples

grab dd  # grab first two numbers
grab qd 2  # grab quoted string, and then the next number after that, disbard the quoted string
grab -qd  # discard first quoted string, print nubmer after that
grab iDq(-SS)d  # grab ip, date, quoted string (Discard first word, grab second) and number.  
grab 3d  # grab three numbers
grab 3d 231  # grab first three number, print them in other order

full syntax of grab command:

grab [ -d '\t' ] ( MULTIPLIER PATTERN [ PARAMETERS ] )+ [ FORMAT_STRING ]

pattern definitions:
    - default/builtin
    - command line arguments?
    - env variables
    - .grab file

## PATTERNS

d   digits
f   floating point
n   number?

s   string? (whitespace?)
D   date
q   quoted string

(custom regex)
-(custom regex)  # discard this
