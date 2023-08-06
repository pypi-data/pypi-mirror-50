from util import *
from phab_wrapper import *
from yaspin import yaspin
import click

@click.command()
@click.pass_context
@click.argument('id')
def lookup(ctx, id):
    with yaspin():
        p = get_phab_cli(ctx)
        print find_task_phid_from_object_identifier(p, id)


@click.command()
@click.pass_context
@click.argument('query')
def lookup_tags(ctx, query):
    with yaspin() as sp:
        p = get_phab_cli(ctx)
        data = get_tag_from_query(p, query)
        sp.write('> name:\t%s' % data['fields']['name'])
        sp.write('> id:\t%s' % data['id'])
