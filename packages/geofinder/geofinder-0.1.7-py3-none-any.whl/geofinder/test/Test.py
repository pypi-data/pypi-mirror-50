import re

reg = r'^\s*(ABT\s+)?([1-3]?[0-9]{1}\s+)?((JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+)?(\d{3,4})'

m = re.search(reg, '12 NOV 1986')
if m:
    print(m.group(1))
    print(m.group(2))
    print(m.group(3))
    print(m.group(5))
