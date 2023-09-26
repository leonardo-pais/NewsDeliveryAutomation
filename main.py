from bs4 import BeautifulSoup
import requests
from datetime import datetime


# Função que coleta notícias do Estadão
def coleta_estadao():
    index = {
        'internacional': 'https://www.estadao.com.br/internacional/',
        'saude': 'https://www.estadao.com.br/saude/',
        'economia': 'https://www.estadao.com.br/economia/',
        'politica': 'https://www.estadao.com.br/politica/',
    }

    titulos = []
    link = []
    res = {}

    # Realize a solicitação HTTP para obter o conteúdo da página
    for topico, url in index.items():
        response = requests.get(url)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Analisa o conteúdo da página com BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontra os elementos que contêm os títulos das notícias
            try:
                a_tags = soup.find_all('a', class_='image')
                for tag in a_tags:
                    titulos.append(tag.get('title'))
                    link.append(tag.get('href'))
                res = dict(zip(titulos, link))
            except Exception as e:
                return e
        else:
            print('Falha ao acessar a página:', response.status_code)
            res[url] = response.status_code
    return res


# Função que coleta notícias da CNN Brasil
def coleta_cnnbrasil():
    # URL dos tópicos do site da CNN Brasil
    index = {
        'internacional': 'https://www.cnnbrasil.com.br/internacional/',
        'saude': 'https://www.cnnbrasil.com.br/saude/',
        'economia': 'https://www.cnnbrasil.com.br/economia/',
        'politica': 'https://www.cnnbrasil.com.br/politica/'
    }

    titulos = []
    link = []
    res = {}


    for topico, url in index.items():
        response = requests.get(url)


        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')


            try:
                noticias = soup.find_all('ul', class_='three__highlights__list row')
                for noticia in noticias:
                    titles = noticia.find_all('h2', 'block__news__title')
                for titulo in titles:
                    titulos.append(titulo.text)

                for i in noticia.find_all('a'):
                    if i.find_all('h3') == []:
                        link.append(i.get('href'))

                res = dict(zip(titulos, link))
            except Exception as e:
                return e

        else:
            print('Falha ao acessar a página:', response.status_code)
            res[url] = response.status_code

    return res


def enviar_msg_whats(msg):
    url = "https://whin2.p.rapidapi.com/send"

    payload = {"text": msg}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": "whin2.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())


# CHAMANDO AS FUNÇÕES
estadao = coleta_estadao()
cnn = coleta_cnnbrasil()

# TRATANDO OS DADOS
saudacao = ''
if datetime.now().hour < 12:
    saudacao = '\nBom dia! Essas são as últimas notícias deste início de dia!\n'
elif 12 < datetime.now().hour < 18:
    saudacao = '\nBoa tarde! Essas são as últimas notícias desta tarde!\n'
else:
    saudacao = '\nBoa noite! Essas são as últimas notícias deste fim de dia!\n'

corpo_texto = '\nNotícias Do Estadão:\n'

for chave, valor in estadao.items():
    corpo_texto += f'Título: {chave} | Link: {valor} \n'

corpo_texto += '\nNotícias Da CNN Brasil:\n'

for chave, valor in cnn.items():
    corpo_texto += f'Título: {chave} | Link: {valor} \n'

mensagem_final = saudacao + corpo_texto

#print(mensagem_final)

enviar_msg_whats(mensagem_final)
