from transaction_builder import *
from phab_wrapper import *
from helpers import *
from yaspin import yaspin
from presenter import display_task_info, display_message
import click


@click.command()
@click.pass_context
@click.option(
    '--title',
    default='Default title',
    help='title of the task',
)
@click.option(
    '--description',
    default='',
    help='description of the task',
)
@click.option(
    '--assigned',
    default='',
    help='phab handle of the user assigned to this task. example: wrahman',
)
@click.option(
    '--subscribers',
    default='',
    help='phab handles of users subscribed to this task. example: \'angie,ethanh\'',
)
@click.option(
    '--parent',
    default='',
    help='assigns a parent for this new task, ie T3610447',
)
@click.option(
    '--tag-ids',
    default='',
    help='ids of tags',
)
def create(ctx, title, description, assigned, subscribers, parent, tag_ids):
    """
    Create phabricator task
    """
    with yaspin() as sp:
        p = get_phab_cli(ctx)
        transactions = get_transactions_for_create(
            p, title, description, assigned, subscribers, parent, tag_ids)
        created = edit_task(p, transactions, None)
        display_message(sp, 'Task: https://code.uberinternal.com/T%s' % created['id'])


@click.command()
@click.pass_context
@click.argument('input', type=click.File('rb'))
def mcreate(ctx, input):
    """
    Bulk creating phabricator task
    """
    with yaspin() as sp:
        display_message(sp, 'Multi-create...')
        p = get_phab_cli(ctx)
        task_list = load_json_from_file(input)
        for t in task_list:
            transactions = get_transactions_for_create(
                p, t['title'], t['description'], t['assigned'], t['subscribers'], t['parent'], t['tag_ids'])
            created = edit_task(p, transactions, t)
            display_task_info(sp, t, created['phid'])


def get_transactions_for_create(p, title, description, assigned, subscribers, parent, tag_ids):
    current_transaction = []
    current_transaction.extend(build_transaction_add_task_title(title))
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
