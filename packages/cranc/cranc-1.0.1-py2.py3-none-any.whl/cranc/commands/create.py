import click
import logging
import os
import pprint

from cranc import utils
from libpagure import exceptions
from libpagure import libpagure

_log = logging.getLogger(__name__)

@click.group()
def create():
    pass


@create.command(name="pr")
@click.option("--repo-to", "-rt", required=True)
@click.option("--title", "-t", required=True)
@click.option("--branch-to", "-bt", required=True)
@click.option("--branch-from", "-bf", required=True)
@click.option("--repo-from", "-rf",  required=True)
@click.pass_context
def create_pr(ctx, repo_to, title, branch_to, branch_from, repo_from):
    """this command creates a new pull request"""
    try:
        api_token = ctx.obj['api_token']
    except KeyError:
        raise click.UsageError('Missing required API token to create a PR')
    project = ctx.obj['project']
    instance_url = ctx.obj['instance_url']
    repo_to = utils.get_dict_from_str(repo_to)
    PAGURE = libpagure.Pagure(
        pagure_token=api_token,
        pagure_repository=repo_to["repo"],
        fork_username=repo_to["username"],
        namespace=repo_to["namespace"],
        instance_url=instance_url,
    )
    PAGURE.log_debug(True)
    try:
        request = PAGURE.create_pull_request(
            title=title, branch_to=branch_to, branch_from=branch_from,
            repo_from=utils.get_dict_from_str(repo_from)
        )
        pprint.pprint(request)
    except Exception:
        _log.exception("Failed to connect to the server")
