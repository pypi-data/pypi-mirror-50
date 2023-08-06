# injectslib

Python APi for [https://injects.cert.pl](https://injects.cert.pl).
Compatible with python2 and python3.

## Info

**Contact email**: msm@cert.pl

## Example

```python
import sys
from injectslib import InjectsApi


if len(sys.argv) == 1:
    print("Usage: example.py api_token")
api = InjectsApi(sys.argv[1])

print("Attacks on {}:".format(api.organisation().name))
for attack in api.attacks():
    print(" - attack by {}, first observed at {}".format(
        attack.family,
        attack.first_seen_iso
    ))
    for inject in attack.injects:
        print("   - inject when url like {}".format(inject.url_pattern))
    for action in attack.actions:
        print("   - {} when url like {}".format(
            action.act_type, action.url_pattern
        ))
```
