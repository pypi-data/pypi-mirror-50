def validation_create(task):
    validation_error_template = 'Error: %s missing'
    required_fields = ['title', 'description', 'assigned']
    for r in required_fields:
        if r not in task:
            raise Exception(validation_error_template % r)


