#!/bin/python3
#Cliente OMNI (Antigo BRMA) para autenticação de usuário
#victor.oliveira@gmx.com
import ssl
from re import findall
from time import sleep
from binascii import hexlify
from urllib.request import urlopen
from urllib.parse import urlencode

class proxy:
    def __init__(self):
        self.server = 'INSIRA O ENDEREÇO IP DO SERVER'
        self.user = 'INSIRA O USUARIO'
        self.senha = 'INSIRA A SENHA'
        self.url = 'https://{}:9803/authd.fcgi'.format(self.server)

        # Cria contexto SSL
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        # Codifica em bytes
        self.user = self.user.encode()
        self.user = hexlify(self.user)
        self.senha = self.senha.encode()
        self.senha = hexlify(self.senha)

    def _req(self):
        self.post = urlencode(self.post).encode()
        req = urlopen(self.url, self.post, context=self.ctx)
        resp = req.read().decode()
        if '101' in resp:
            print('Usuário ou senha incorreto.')
            exit(1)
        self.ticket = findall('\w{32}', resp)[0]
        print(resp)

    def auth(self):
        self.post = {'Action' : 'AUTH_LOGIN',
            'Login' : self.user,
            'Password' : self.senha}
        self._req()

    def keep(self):
        self.post = {'Action' : 'AUTH_KEEPALIVE',
            'Login' : self.user,
            'Ticket' : self.ticket}
        self._req()

    def logout(self):
        self.post = {'Action' : 'AUTH_LOGOUT',
            'Login' : self.user,
            'Ticket' : self.ticket}
        self._req()

p = proxy()
p.auth()
try:
    while True:
        sleep(480)
        p.keep()
except KeyboardInterrupt:
    p.logout()
    exit()
