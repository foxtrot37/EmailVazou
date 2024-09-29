import requests
import smtplib
import sys

# Verificar se o arquivo de e-mails foi passado
if len(sys.argv) < 2:
    print('Uso: python vazou.py arquivo_com_emails.txt')
    sys.exit()

# Função para verificar se o e-mail foi comprometido em vazamentos
def vazou(conta: str, api_key: str):
    '''Verifica se o email foi comprometido em vazamentos de dados'''
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0',
        'hibp-api-key': api_key
    }
    url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{conta}'
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print(f'[+] O e-mail {conta} foi comprometido em um vazamento.')
        return True
    else:
        print(f'[-] O e-mail {conta} não foi comprometido.')
        return False

# Função para enviar e-mail caso o e-mail tenha sido vazado
def enviando(admin_m, admin_p, vazou_s):
    '''Envia uma mensagem para o usuário caso o email tenha sido vazado'''
    # Mensagem de alerta
    msg = f'Subject: Alerta de Segurança\n\nSua senha foi comprometida em um vazamento. Mude-a imediatamente.'
    
    try:
        # Conectar ao servidor SMTP (no caso, Gmail)
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(admin_m, admin_p)
        smtp.sendmail(admin_m, vazou_s, msg)
        smtp.quit()
        print(f'[*] E-mail de alerta enviado para {vazou_s}')
    except Exception as e:
        print(f'[!] Falha ao enviar e-mail: {e}')

# Nome do arquivo contendo os e-mails
n_arquivo = sys.argv[1]

# API key do Have I Been Pwned (deve ser obtida previamente)
api_key = input("Insira sua API key do Have I Been Pwned: ")

# Abrir o arquivo e ler os e-mails
with open(n_arquivo, 'r') as f:
    emails = [e.strip() for e in f.readlines()]

# Solicitar credenciais do administrador para o envio de e-mails
admin = input('E-mail do Administrador (Gmail): ')
senha = input('Senha do Administrador: ')

# Verificar se cada e-mail foi comprometido
email_vazou = []
for email in emails:
    if vazou(email, api_key):
        email_vazou.append(email)

# Enviar alertas para os e-mails comprometidos
for email in email_vazou:
    enviando(admin, senha, email)

print('Verificação concluída.')
