import datetime
import sys
import json
import requests


def parse_iso(date):
    fmt = '%Y-%m-%dT%H:%M:%S%z'
    return datetime.datetime.strptime(date, fmt)


class TokenData:
    def __init__(self, token):
        if sys.version_info >= (3, 0):
            decoded = bytes.fromhex(token).decode('utf-8')
        else:
            decoded = token.decode('hex')
        data = decoded[:decoded.rfind('.')]
        raw = json.loads(data)
        self.organisation = raw['organisation']
        self.is_admin = raw['is_admin']


class Organisation:
    def __init__(self, raw):
        self.raw = raw

    @property
    def name(self):
        """ name of the organisation (shown in the address bar and in the UI)
        """
        return self.raw["name"]

    @property
    def contact_email(self):
        """ contact email of the organisation. May be null. """
        return self.raw["contact_email"]

    @property
    def url_patterns(self):
        """ List of url patterns assigned to the organisation. """
        return self.raw["url_patterns"]


class Action:
    def __init__(self, raw):
        self.raw = raw

    @property
    def url_pattern(self):
        """ Url pattern that triggers the action. This action will be executed
        by the malware for websites matching the given url pattern. """
        return self.raw["url_pattern"]

    @property
    def act_type(self):
        """ Type of the action.
        Supported types are: redirect, steal_data, vnc, proxy and hide. """
        return self.raw["act_type"]

    @property
    def malicious_url(self):
        """ Malicious url targeted by the action. """
        return self.raw["malicious_url"]


class Inject:
    def __init__(self, raw):
        self.raw = raw

    @property
    def url_pattern(self):
        """ Url pattern that triggers injection. Inject will be executed
        by the malware for websites matching the given url pattern. """
        return self.raw["url_pattern"]

    @property
    def data_before(self):
        """ Inject malicious code after this pattern in the website. """
        return self.raw["data_before"]

    @property
    def data_inject(self):
        """ Code that will be injected to the website. """
        return self.raw["data_inject"]


class Attack:
    def __init__(self, raw):
        self.raw = raw

    @property
    def config_id(self):
        """ Raw config id, represented by sha256 hash. Cryprographically
        guarenteed to be unique for distinct configs.
        Internally, this is MWDB config id (https://mwdb.cert.pl/). It's
        possible to cross-search, if you have a mwdb account. """
        return self.raw["config_id"]

    @property
    def family(self):
        """ Family of malware that triggered this attack (for example,
        "trickbot" or "isfb") """
        return self.raw["family"]

    @property
    def first_seen(self):
        """ Datetime object representing first recorded config with
        this attack. This property works only on python 3 """
        return parse_iso(self.raw["first_seen"])

    @property
    def first_seen_iso(self):
        """ iso-8601 string representing first recorded config with
        this attack. Works on all python versions """
        return self.raw["first_seen"]

    @property
    def last_seen(self):
        """ Datetime object representing last recorded config with
        this attack. This property works only on python 3 """
        return parse_iso(self.raw["last_seen"])

    @property
    def last_seen_iso(self):
        """ iso-8601 string representing last recorded config with
        this attack. Works on all python versions """
        return self.raw["last_seen"]

    @property
    def actions(self):
        """ Return a list of actions (see also: `Action` type) executed by
        this attack """
        return [Action(act) for act in self.raw["data"]["actions"]]

    @property
    def injects(self):
        """ Return a list of injects (see also: `Inject` type) executed by
        this attack """
        return [Inject(act) for act in self.raw["data"]["injects"]]


class InjectsApi:
    def __init__(self, token, api_root="https://injects.cert.pl"):
        self.token = token
        self.root = api_root.rstrip('/')
        self.token_info = TokenData(token)
        self.orgname = self.token_info.organisation

    def get(self, endpoint):
        assert endpoint.startswith('/')
        url = self.root + endpoint
        return requests.get(
            url,
            headers={"Authorization": "Bearer " + self.token},
        ).json()

    def organisation(self):
        return Organisation(self.get(
            '/organisation/{}/export_organisation'.format(self.orgname)
        ))

    def attacks(self):
        data = self.get(
            '/organisation/{}/export_attacks'.format(self.orgname)
        )
        return [Attack(atk) for atk in data]
