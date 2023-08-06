# pyjama
A set of casual python utilities

## Mutable String Builder
```python
from pyjama.strutils import string_builder as sb
s = sb.StringBuilder()

s.append('Wow, ')
s.append('such a nice ').append('builder')
print(len(s))

s += ' :)'

s[:3] = 'whee'

s.remove(1)

for c in s:
    pass

print(str(s))
```
