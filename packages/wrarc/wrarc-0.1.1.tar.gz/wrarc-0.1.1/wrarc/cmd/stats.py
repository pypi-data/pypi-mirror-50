from util import *
from phab_wrapper import *
from yaspin import yaspin
from presenter import display_message
from unidiff import PatchSet
from cStringIO import StringIO
import click


@click.command()
@click.pass_context
def stats(ctx):
    with yaspin() as sp:
        p = get_phab_cli(ctx)
        user = find_user(p)

        done = False
        after = ''
        commit_ids = []
        message = []
        while not done:
            display_message(sp, 'Searching with cursor %s' % after)
            results = p.differential.revision.search(constraints={
                'authorPHIDs': [user['phid']]
            }, after=after)
            for d in results['data']:
                is_closed = d['fields']['status']['closed']
                if is_closed:
                    commit_ids.append({'id': d['id'], 'phid': d['phid']})
                    message.append(d['fields']['summary'])
            after = results['cursor']['after']
            if after is None:
                done = True
        print commit_ids
        print len(commit_ids)

        # Parse the rawdiff
        for c in commit_ids:
            print int(c['id'])
            raw_diff = p.differential.getrawdiff(diffID=int(c['id']))
            print raw_diff
            print type(raw_diff)
            break

        # for m in message:
        #     print m
