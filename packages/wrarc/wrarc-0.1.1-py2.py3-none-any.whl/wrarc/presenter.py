def display_task_info(sp, t, created):
    sp.write('> Created Task: %s - %s' % (t['title'], ('https://code.uberinternal.com/T%s' % created['id'])))


def display_message(sp, msg):
    sp.write('> %s' % msg)
