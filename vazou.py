import sys

import requests

if len(sys.argv) < 2:
        print('python vazou.py emails.txt')
        sys.exit()

def vazou(conta: str):
        '''verifica se a senha do email vazou.

        ARG:
            conta: Email que vai ser verificado
        '''
        headers = {'user-Agent': 'Mozilla/5.0 (X11; Linux i586; rb:63.0) Firefox/63.0'}
        r = requests.get(f'https://haveibeenpwned.com/api/v2/breachedaccount/{conta}',
                         headers=headers)
        r_info = r.content.decode('utf-8')
        if r_info:
                #emails que vazou
                print(f'+ {conta} +')


if __name__ == '__main__':
   #nome do arquivo
   n_arquivo = sys.argv[1]

   with open(n_arquivo, 'r') as f:
       emails = [e.strip() for e in f.readlines()]
   for email in emails:
       vazou(email)
