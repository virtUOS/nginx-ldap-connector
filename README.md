# nginx-ldap-connector

Just a very simple service to be able to use ldap with nginx basic auth.

## Usage

### Run the connector

You can run the service simply with docker like in the following docker-compose example.
Just make sure to configure it to be compatible with your ldap.

```yml
---
version: '3'

services:
  nginx-ldap-connector:
    image: ghcr.io/virtuos/nginx-ldap-connector:main
    restart: unless-stopped
    ports:
      - '5555:5555'
    environment:
      LDAP_SERVER: 'ldap.example.org'
      LDAP_PORT: 636
      LDAP_BASE_DN: 'ou=,dc=,dc='
      LDAP_USER_DN: 'uid={username},ou=,dc=,dc='
      LDAP_SEARCH_FILTER: '(uid={username})'
      LISTEN_ADDR: '0.0.0.0'
      LISTEN_PORT: 5555
      LOGLEVEL: info
```

### NGINX

To configure authentication in nginx for a location (named `/private/` in this case)
you can do the following:

```
    location /private/ {
        auth_request /auth;
        #...
    }

    location = /auth {
        internal;
        proxy_pass              http://127.0.0.1:5555;
        proxy_pass_request_body off;
        proxy_set_header        Content-Length "";
        proxy_set_header        X-Original-URI $request_uri;
    }
```

See https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/
for more information.

## Development

For development just install the requirements in a python virtual environment
and run the flask app:

```
pip install -r requirements.txt
python nginx-ldap-connector.py
```
