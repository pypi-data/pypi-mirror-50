from transaction_builder import *
from phab_wrapper import *
from helpers import *
from yaspin import yaspin
from presenter import display_task_info
from validation import validation_create
import click


@click.command()
@click.pass_context
@click.argument('f', type=click.File('rb'))
def medit(ctx, f):
    """
    Create phabricator task from yaml
    """
    click.echo('Creating a task...')
    with yaspin() as sp:
        p = get_phab_cli(ctx)
        bulk_task = load_yaml_from_file(f)
        for t in bulk_task:
            try:
                validation_create(t)
                sp.write('> Creating %s' % t['title'])
                created = create_task(p, t)

                if 'id' in t:
                    # This task already exists
                    pass

                display_task_info(sp, t, created)
                if 'child' not in t:
                    continue

                for c in t['child']:
                    print ('\tchild %s' % c)
            except AssertionError as error:
                sp.write(error)
                sp.write('> Error. Could not validate the task. '
                         'Please ensure the file is formatted correctly.')


def create_task(p, t):
    transactions = get_transactions_for_create(
        p,
        t['title'],
        t['description'],
        t['assigned'],
        t['subscribers'],
        t['parent'],
        t['tag_ids'])
    created = edit_task(p, transactions)
    return created


def get_transactions_for_create(p, title, description, assigned, subscribers, parent, tag_ids):
    current_transaction = []

    current_transaction.extend(
        build_transaction_add_task_title(title))
    current_transaction.extend(
        build_transaction_add_task_description(description))
    current_transaction.extend(
        build_transaction_add_task_owner(p, assigned))
    current_transaction.extend(
        build_transaction_add_task_subscribers(p, subscribers))
    current_transaction.extend(
        build_transaction_assign_parent(p, parent))

    # Handle tags
    tag_phids = get_tag_phids_from_ids(p, tag_ids)
    current_transaction.extend(
        build_transaction_add_tags(p, tag_phids)
    )
    return current_transaction
