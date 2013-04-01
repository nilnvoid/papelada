import json
from fabric.api import *


@task
def save_credentials(user, pwd):
    with open('credentials.json', 'wb') as fp:
        json.dump({'username': user, 'password': pwd}, fp, indent=4)


@task
def save_ftp_address(ftp_address):
    with open('ftp_address.json', 'wb') as fp:
        json.dump({'address': ftp_address}, fp, indent=4)


def _get_confs():
    try:
        with open('ftp_address.json', 'r') as ftpconf:
            env.update(json.load(ftpconf))
        with open('credentials.json', 'r') as credfile:
            env.update(json.load(credfile))
    except IOError:
        print('You should use save_ftp_address and save_credentials'
              ' to save your FTP address and credentials on this '
              'machine')

def _get_base_url(subdomain=None):
    ret = ('ftp://%(username)s:%(password)s'
        '@'
        '%(address)s/www/' % env)
    if subdomain:
        return ret + subdomain
    else:
        return ret


@task
def put(subdomain):
    '''put all files in question2answer folder to the desired
    subdomain. Requires the external script ftpsync.py to be
    executable (use chmod +)

    '''

    _get_confs()
    local('./ftpsync.py %s question2answer/ --upload' % _get_base_url(subdomain))

@task
def get(subdomain):
    '''get files from server. use cautiously

    '''

    _get_confs()
    local('./ftpsync.py %s question2answer/ --download' % _get_base_url(subdomain))


