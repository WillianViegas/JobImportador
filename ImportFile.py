from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

def download_urls_para_arquivo():
    try:
        #Obter urls para download de algum site
        url = "https://www.imdb.com/calendar/?ref_=nv_mv_cal"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        lista_urls = []
        linhas = 0

        file = open("lista_urls.txt", "r")
        conteudo = file.read()
        co_lista = conteudo.split("\n")
        for linha in co_lista:
            if(linha):
                linhas += 1

        if linhas <= 0:
            for a_href in soup.find_all("a", href=True):
                if "imdb" not in a_href["href"] and "title" in a_href["href"]:
                    lista_urls.append("https://www.imdb.com" + a_href["href"])

        #Salvar as urls em um arquivo txt
        for url in lista_urls:
            with open("lista_urls.txt", "a") as urlfile:
                urlfile.write(url + "\n")

        meu_arquivo = open("lista_urls.txt", "r")
        linhas_arquivo = meu_arquivo.readlines()
        urls_arquivo = linhas_arquivo

        print(len(urls_arquivo))

        for l in urls_arquivo:
            print(l.strip())

        #Fazer tratativa no arquivo para nao repetir as urls
        print("download_arquivo")
    except Exception as e:
        print(e)

def scrapping_dados_urls():
    try:
        print("scrapping_dados_urls")
        meu_arquivo = open("lista_urls.txt", "r")
        linhas_arquivo = meu_arquivo.readlines()
        urls_arquivo = linhas_arquivo

        for l in urls_arquivo:
            url = l
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            print(soup.find("h1"))
        #realizar o download utilizando as urls salvas e guardar o que foi baixado em uma pasta

    except Exception as e:
        print(e)

def importar_dados():
    try:
        #Instanciar conexao com o MongoDB
        #Realizar a leitura dos arquivos baixados salvos na pasta
        #Fazer tratativas nos dados
        #Salvar os dados válidos no banco
        #Salvar os dados com erro em um arquivo txt
        print("importar_dados")
    except Exception as e:
        print(e)


# download_urls_para_arquivo()
scrapping_dados_urls()
importar_dados()