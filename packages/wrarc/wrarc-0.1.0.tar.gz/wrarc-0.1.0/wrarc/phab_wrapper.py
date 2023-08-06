from helpers import *


def edit_task(p, transactions, task_phid):
    if task_phid is not None and type(task_phid) is str:
        # Update an existing task
        created = p.maniphest.edit(objectIdentifier=task_phid, transactions=transactions)
    else:
        # Create a new task
        created = p.maniphest.edit(transactions=transactions)

    return created.__getitem__('object')


def get_tag_from_query(p, query):
    tag = p.project.search(constraints={'query': query}, limit=1)
    return tag.__getitem__('data')[0]


def close_task(p, task_phid, transaction):
    p.maniphest.edit(objectIdentifier=task_phid,
                     transactions=transaction)


def get_tag_phids_from_ids(p, tag_ids):
    tag_ids_str = get_comma_delimitted_list(clean_string(tag_ids))
    tag_ids = []

    for id in tag_ids_str:
        tag_ids.append(int(id, 10))

    tag_resps = p.project.search(
        constraints={'ids': tag_ids}).__getitem__('data')

    phids = []
    for t in tag_resps:
        phids.append(t['phid'])

    return phids
