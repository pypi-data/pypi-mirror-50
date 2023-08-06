import sys
from .api import InjectsApi


def main():
    if len(sys.argv) == 1:
        print("Usage: example.py api_token [api_root]")
    token = sys.argv[1]
    if len(sys.argv) > 2:
        api_root = sys.argv[2]
    else:
        api_root = "https://injects.cert.pl"
    api = InjectsApi(token, api_root=api_root)

    org = api.organisation()
    print("This org: {} ({})".format(org.name, org.contact_email))
    print("Assigned url patterns:")
    for url in org.url_patterns:
        print(" - {}".format(url))
    print("")
    print("Attacks:")
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


if __name__ == '__main__':
    main()
