import os
from StringIO import StringIO

def handler(self):
    form = self.form
    env = form['environ']
    result = StringIO()
    if env == 'beta':
        proj_base = '/home/zhanglei3/apps/bitsurvey-%s/' % env
        result.write(run_command('cd %s && git pull' % proj_base))
    elif env == 'release':
        proj_base = '/home/zhanglei3/apps/bitsurvey-%s/' % env
        result.write(run_command('cd %s && git pull' % proj_base))
    elif env == 'online':
        proj_base = '/home/zhanglei3/apps/bitsurvey-%s/' % env
        result.write(run_command('cd %s && git pull' % proj_base))
    result.write(run_command('cd /home/zhanglei3/supervisord && supervisorctl restart bitsurvey-%s' % env))
    return '<pre>' + result.getvalue() + '</pre>'

def run_command(cmd):
    with os.popen(cmd) as f:
        return f.read()
    
