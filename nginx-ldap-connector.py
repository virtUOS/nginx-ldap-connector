import logging
import os

from flask import Flask, request
from ldap3 import Server, Connection, ALL, AUTO_BIND_NO_TLS

# Logger
logging.root.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

ldap_server = os.environ['LDAP_SERVER']
ldap_port = int(os.environ['LDAP_PORT'])
ldap_base_dn = os.environ['LDAP_BASE_DN']
ldap_user_dn = os.environ['LDAP_USER_DN']
ldap_search_filter = os.environ['LDAP_SEARCH_FILTER']

app = Flask(__name__)


def connect(user_dn=None, password=None):
    server = Server(ldap_server,
                    port=ldap_port,
                    use_ssl=True,
                    get_info=ALL)
    # Note: AUTO_BIND_NO_TLS means no Start TLS
    # See: https://github.com/cannatag/ldap3/issues/1061
    return Connection(server, user_dn, password, auto_bind=AUTO_BIND_NO_TLS)


def ldap_login(username: str, password: str) -> dict[str, list]:
    '''Login to LDAP and return user attributes.

    The idea of this is basically for the user to login to LDAP and request its
    own attributes. Obviously, this code will do that for the user with the
    provided credentials.

    :param username: Username to log in with.
    :param password: Password to log in with.
    :returns: Dictionary containing requested user attributes.
    '''
    user_dn = ldap_user_dn.format(username=username)

    logging.debug('Trying to log into LDAP with user_dn `%s`', user_dn)
    conn = connect(user_dn, password)
    logging.debug('Login successful with user_dn `%s`', user_dn)

    attributes = []

    logging.debug('Searching for user data')
    conn.search(
            ldap_base_dn,
            ldap_search_filter.format(username=username),
            attributes=attributes)
    if len(conn.entries) != 1:
        raise ValueError('Search must return exactly one result', conn.entries)
    logging.debug('Found user data')
    return conn.entries[0].entry_attributes_as_dict


def check_auth(auth):
    if not auth:
        return False
    try:
        ldap_login(auth.username, auth.password)
    except Exception as e:
        logging.debug('Error logging in: %s', e)
        return False
    return True


@app.route('/auth')
def auth():
    if not check_auth(request.authorization):
        return ('Unauthorized', 401, {
            'WWW-Authenticate': 'Basic realm="Login Required"'
        })
    return 'okay'


if __name__ == '__main__':
    app.run(host=os.environ.get('LISTEN_ADDR', '127.0.0.1'),
            port=os.environ.get('LISTEN_PORT' '5000'))
