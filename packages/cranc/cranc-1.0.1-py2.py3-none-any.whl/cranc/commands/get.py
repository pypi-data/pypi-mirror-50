import click
import logging
import os
import pprint

from libpagure import exceptions
from libpagure import libpagure

_log = logging.getLogger(__name__)


@click.group()
def get():
    pass


@get.command(name="prs")
@click.option("--status")
@click.option("--assignee")
@click.option("--author")
@click.pass_context
def pr_list(ctx, status, assignee, author):
    """Prints list of pull requests.
    :param status: filters the status of the requests: Open, Closed, Merged
    :param assignee: filters the assignee of the requests
    :param author: filters the author of the requests
    :return:
    """
    api_token = ctx.obj.get('api_token')
    project = ctx.obj['project']
    instance_url = ctx.obj['instance_url']
    project = ctx.obj['project']
    PAGURE = libpagure.Pagure(pagure_token=api_token,
                              pagure_repository=project,
                              instance_url=instance_url)
    try:
        prs = PAGURE.list_requests(status=status, assignee=assignee, author=author)
        pprint.pprint(prs)
    except Exception:
        _log.exception("Failed to connect to the server")


@get.command(name="issues")
@click.option("--status")
@click.option("--tags")
@click.option("--assignee")
@click.option("--author")
@click.option("--milestones")
@click.option("--priority")
@click.option("--no_stones")
@click.option("--since")
# @click.option("--order")
@click.pass_context
def issue_list(ctx, status, tags, assignee, author, milestones, priority, no_stones, since):
    """Prints list of issues"""
    api_token = ctx.obj.get('api_token')
    project = ctx.obj['project']
    instance_url = ctx.obj['instance_url']
    PAGURE = libpagure.Pagure(pagure_token=api_token,
                              pagure_repository=project,
                              instance_url=instance_url)
    try:
        issues = PAGURE.list_issues(
            status=status,
            tags=tags,
            assignee=assignee,
            author=author,
            milestones=milestones,
            priority=priority,
            no_stones=no_stones,
            since=since,
        )
    except exceptions.APIError:
        pagure_noauth = libpagure.Pagure(pagure_repository=project)
        issues = pagure_noauth.list_issues(
            status=status,
            tags=tags,
            assignee=assignee,
            author=author,
            milestones=milestones,
            priority=priority,
            no_stones=no_stones,
            since=since,
        )
    pprint.pprint(issues)
