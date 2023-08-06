import click
import logging
import os
import pprint

from libpagure import libpagure

_log = logging.getLogger(__name__)

api_token = os.getenv("PAGURE_USER_TOKEN")


@click.group()
def merge():
    pass


@merge.command(name="pr")
@click.option("--request-id", required=True)
@click.pass_context
def merge_pr(ctx, request_id):
    """This command merges a pull request"""
    try:
        api_token = ctx.obj['api_token']
    except KeyError:
        raise click.UsageError('Missing required API token to merge PRs')
    project = ctx.obj['project']
    instance_url = ctx.obj['instance_url']
    PAGURE = libpagure.Pagure(
        pagure_token=api_token, pagure_repository=project, instance_url=instance_url
    )
    try:
        request = PAGURE.merge_request(request_id=request_id)
        print("Pull request succesfully merged")
    except Exception:
        _log.exception("Failed to connect to the server")
