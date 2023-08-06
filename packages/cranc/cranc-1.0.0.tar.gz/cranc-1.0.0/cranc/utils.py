import subprocess
import sys

from giturlparse import parser


def get_dict_from_str(string):
    """
    Converts repo_from string into dictionary.
    Expected strings:
    'repo'
    'namespace/repo'
    'fork/username/repo'
    'fork/username/namespace/repo'
    """

    if string:
        words = string.split('/')
        if len(words) == 4:
            fork, username, namespace, repo = words
            return {"username": username, "namespace": namespace, "repo": repo}
        elif len(words) == 3:
            fork, username, repo = words
            return {"username": username, "namespace": None, "repo": repo}
        elif len(words) == 2:
            namespace, repo = words
            return {"username": None, "namespace": namespace, "repo": repo}
        elif len(words) == 1:
            repo, = words
            return {"username": None, "namespace": None, "repo": repo}
        else:
            raise Exception("Wrong formatted repo path")


def get_repo():
    repo = subprocess.check_output(
        ['git', 'config', '--get', 'remote.origin.url'],
        encoding=sys.stdout.encoding)
    return repo.strip()


def project_name(remote_url):
    parsed = parser.Parser(remote_url).parse()
    return parsed.name



def guess_instance_url(remote_url):
    parsed = parser.Parser(remote_url).parse()
    if parsed.protocol in ('https', 'ssh'):
        protocol = 'https'
    else:
        protocol = 'http'

    return f'{protocol}://{parsed.resource}'
