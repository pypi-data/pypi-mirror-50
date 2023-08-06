from util import *


def build_transaction_assign_parent(p, parent_id):
    if parent_id == '':
        return []

    parent_phid = find_task_phid_from_object_identifier(p, parent_id)
    return [{'type': 'parent', 'value': parent_phid}]


def build_transaction_close_task(p, phid, resolution):
    supported_resolutions = ['resolved', 'invalid', 'wontfix']
    if resolution in supported_resolutions:
        return [{'type': 'status', 'value': resolution}]
    # TODO: Print error
    return []


def build_transaction_add_task_subscribers(p, subscribers):
    if subscribers == '':
        return []

    # clean list
    sub_list = get_comma_delimitted_list(clean_string(subscribers))
    if len(sub_list) == 0:
        return []

    phids = []
    print sub_list
    for sub in sub_list:
        phids.append(find_user_phid(p, sub))
    return [{'type': 'subscribers.add', 'value': phids}]


def build_transaction_add_task_owner(p, assigned):
    """
    Takes the current assigned user and tries to fetch it.
    Returns a transaction with the current user assigned.
    """
    # validate the assigned user
    if assigned == '':
        assigned = get_current_username(p)
    phid = find_user_phid(p, assigned)
    return [{'type': 'owner', 'value': phid}]


def build_transaction_add_task_title(title):
    return [{'type': 'title', 'value': title}]


def build_transaction_add_task_description(description):
    return [{'type': 'description', 'value': description}]


def build_transaction_add_tags(p, tag_phids):
    return [{'type': 'projects.add', 'value': tag_phids}]
