from phabricator import Phabricator
from cmd.create import create, mcreate
from cmd.close import close, mclose
from cmd.lookup import lookup, lookup_tags
from cmd.medit import medit
from cmd.stats import stats

import click

# TODO: add links to the task after they have been created.
# ie code.uberinternal.com/T3610447
@click.group()
@click.pass_context
def phab(ctx):
    p = Phabricator()
    p.update_interfaces()
    ctx.obj['phabricator'] = p


if __name__ == "__main__":
    phab.add_command(create)
    phab.add_command(mcreate)
    phab.add_command(lookup)
    phab.add_command(close)
    phab.add_command(mclose)
    phab.add_command(lookup_tags)
    phab.add_command(medit)
    phab.add_command(stats)
    phab(obj={})
