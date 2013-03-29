import json
from fabric.api import *


@task
def save_credentials(user, pwd):
    with open('credentials.json', 'wb') as fp:
        json.dump({'username': user, 'password': pwd}, fp, indent=4)

@task
def save_ftp_address(ftp_address):
    with open('ftp_address.json', 'wb') as fp:
        json.dump({'ftpAddress': ftp_address}, fp, indent=4)

def _get_confs():
    try: 
        with open('ftp_address.json', 'r') as fp:
            env.address = json.load(fp)['ftpAddress']
        with open('credentials.json', 'r') as fp:
            usrpass = json.load(fp)
            env.username, env.password = usrpass['username'], usrpass['password']
    except IOError:
        print('You should use save_ftp_address and save_credentials'
              ' to save your FTP address and credentials on this '
              'machine')

@task
def put(subdomain):
    '''put all files in question2answer folder to the desired
    subdomain. Requires the external script ftpsync.py to be
    executable (use chmod +)

    '''

    _get_confs()
    env.update({'subdomain': subdomain})
    remote_url = ('ftp://%(username)s:%(password)s'
        '@'
        '%(address)s/www/%(subdomain)s' % env)

    local('./ftpsync.py %s question2answer/ --upload' % remote_url)
