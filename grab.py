import re
import sys

command = sys.argv[1]

patterns = {
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

# print(patterns['a'])
# print(patterns['e'])

if len(sys.argv) == 3:
    indices = [int(c) for c in sys.argv[2]]
else:
    indices = [i + 1 for i in range(len(command))]

with open('sample/access_log') as f:
    for line in sys.stdin:
        tokens = []
        prev = ''
        for c in command:
            if c == '\\':
                prev = c
                continue

            pattern = patterns[c]
            match = re.search(pattern, line)
            if match:
                begin, end = match.span()
                if prev != '\\':
                    tokens.append(line[begin: end])
                line = line[end:]
            prev = c

        output = []
        for i in indices:
            output.append(tokens[i - 1])

        # print(f'tokens={tokens}, output={output}')
        print('\t'.join(output))
