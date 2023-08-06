# Cranc - A pagure CLI
# Copyright (C) 2019 Lenka Segura
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import logging
import os
import re

import click
import pprint

from cranc.commands import get
from cranc.commands import merge
from cranc.commands import create
from cranc import utils

CONFIG = os.path.expanduser('~/.config/cranc')

class ApiToken(click.ParamType):
    name = 'api-token'

    def convert(self, value, param, ctx):
        found = re.match(r'[0-9a-f]{32}', value)

        if not found:
            self.fail(
                    f'{value} is not a 32-character hexadecimal string',
                    param,
                    ctx,
                )
        return value


api_token = os.getenv("PAGURE_USER_TOKEN")
_log = logging.getLogger(__name__)


@click.group()
@click.option(
        '--api-token', '-a',
        type=ApiToken(),
        help='your API key for Pagure.io',
)
@click.option(
        '--repo-url', '-r',
        help='Repo url'
)
@click.option(
        '--instance-url', '-i',
        help='Pagure instance url'
)
@click.option(
        '--config-file', '-c',
        type=click.Path(),
        default='~/.config/cranc.cfg')
@click.pass_context
def cranc(ctx, api_token, repo_url, instance_url, config_file):
    filename = os.path.expanduser(config_file)

    ctx.obj = {
        'config_file': filename,
    }
    if not repo_url:
        repo_url = utils.get_repo()
    ctx.obj['repo_url'] = repo_url

    if os.path.exists(filename):
        try:
            with open(filename) as cfg:
                json_cfg = json.loads(cfg.read())

        except json.decoder.JSONDecodeError:
            _log.info('No pre-existing cranc json config')
        if repo_url in json_cfg:
            ctx.obj.update(json_cfg[repo_url])

    if api_token:
        ctx.obj['api_token'] = api_token
    if instance_url:
        ctx.obj['instance_url'] = instance_url

    if ctx.obj.get('repo_url'):
        ctx.obj['project'] = utils.project_name(ctx.obj['repo_url'])
    if 'instance_url' not in ctx.obj:
        ctx.obj['instance_url'] = utils.guess_instance_url(repo_url)


@cranc.command()
@click.pass_context
def config(ctx):
    config_file = ctx.obj['config_file']
    api_token = click.prompt('Please enter your API token',
                           default=ctx.obj.get('api_token', '')
                           )
    repo_url = click.prompt('Please enter your repo url',
                           default=ctx.obj.get('repo_url', utils.get_repo())
                           )
    instance_url = click.prompt(
        'Please enter your Pagure instance url',
        default=ctx.obj.get('instance_url',
                            utils.guess_instance_url(repo_url)))
    with open(config_file, 'w') as cfg:
        cfg_content = json.dumps({
            repo_url: {
                'api_token': api_token,
                'repo_url': repo_url,
                'instance_url': instance_url
                }
            }, sort_keys=True, indent=4)
        cfg.write(cfg_content)


cranc.add_command(get.get)
cranc.add_command(merge.merge)
cranc.add_command(create.create)

if __name__ == "__main__":
    cranc()
