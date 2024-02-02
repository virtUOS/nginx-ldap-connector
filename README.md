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
    image: ghrc.io/virtuos/nginx-ldap-connector:latest
    restart: unless-stopped
    ports:
      - '5555:5555'
    environment:
      ldap_server: 'ldap.example.org'
      ldap_port: 636
      ldap_base_dn: 'ou=,dc=,dc='
      ldap_user_dn: 'uid={username},ou=,dc=,dc='
      ldap_search_filter: '(uid={username})'
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
flask --app nginx-ldap-auth run
```
