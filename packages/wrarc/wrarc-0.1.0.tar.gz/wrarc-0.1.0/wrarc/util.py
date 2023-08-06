from helpers import *


def find_user_phid(p, user):
    """
    Fetches a phid for a given user.
    """
    phabUser = p.user.find(aliases=[user])
    return phabUser[user]


def find_task_phid_from_object_identifier(p, id):
    """
    Fetches the phid of an object identifier ie T3383713
    """
    task = p.maniphest.edit(objectIdentifier=id, transactions=[])
    return unicode_to_str(task.__getitem__('object')['phid'])


def get_current_username(p):
    return p.user.whoami().userName


def find_user(p):
    """
    Fetches the phid of an object identifier ie T3383713
    """
    curr_user = p.user.whoami()
    user_json = json.loads(json.dumps(curr_user.__dict__))
    return user_json['response']
