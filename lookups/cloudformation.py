from ansible import utils, errors

try:
    import boto
    import boto.cloudformation
except ImportError:
    raise errors.AnsibleError(
        "Can't LOOKUP(cloudformation): module boto is not installed")

class LookupModule(object):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        aws_access_key = inject['aws_access_key']
        aws_secret_key = inject['aws_secret_key']
        region = inject['aws_region']
        stack, key = terms.split('/')

        value = False
        conn = boto.cloudformation.connect_to_region(region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        stack = conn.describe_stacks(stack_name_or_id=stack)[0]
        value = [output.value for output in stack.outputs if output.key == key]

        return value
