from transaction_builder import *
from phab_wrapper import *
from helpers import *
from yaspin import yaspin
import click


@click.command()
@click.pass_context
@click.argument('id')
@click.option('--status',
              type=click.Choice(['resolved', 'invalid', 'wontfix']),
              default='resolved',
              )
def close(ctx, id, status):
    with yaspin():
        p = get_phab_cli(ctx)
        phid = find_task_phid_from_object_identifier(p, id)
        current_transaction = []
        current_transaction.extend(
            build_transaction_close_task(p, phid, status))
        close_task(p, phid, current_transaction)


@click.command()
@click.pass_context
@click.argument('ids')
@click.option('--status',
              type=click.Choice(['resolved', 'invalid', 'wontfix']),
              default='resolved',
              )
def mclose(ctx, ids, status):
    with yaspin() as sp:
        p = get_phab_cli(ctx)
        ids = get_comma_delimitted_list(clean_string(ids))
        if ids == '':
            return

        for id in ids:
            phid = find_task_phid_from_object_identifier(p, id)
            close_task(p, phid, build_transaction_close_task(p, phid, status))
            sp.write('> updated %s as %s' % (id, status))
