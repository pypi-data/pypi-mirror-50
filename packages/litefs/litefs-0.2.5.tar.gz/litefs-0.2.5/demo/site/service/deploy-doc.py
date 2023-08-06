import os
from StringIO import StringIO

def handler(self):
    form = self.form
    env = form['environ']
    result = StringIO()
    if env == 'beta':
        doc_base = '/home/zhanglei3/apps/wpapi-doc-beta/'
    elif env == 'online':
        doc_base = '/home/zhanglei3/apps/wpapi-doc/'
    result.write(run_command('cd %s && git pull' % doc_base))
    result.write(run_command('cd %s && bundle exec middleman build --clean' % doc_base))
    return '<pre>' + result.getvalue() + '</pre>'

def run_command(cmd):
    with os.popen(cmd) as f:
        return f.read()
