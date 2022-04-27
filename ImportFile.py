from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import os

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
        # O que pegar da tela:
        # Titulo  OK
        # duracao OK
        # nota de avaliacao OK
        # imagem OK
        # descricao OK

        print("scrapping_dados_urls")
        meu_arquivo = open("lista_urls.txt", "r")
        linhas_arquivo = meu_arquivo.readlines()
        urls_arquivo = linhas_arquivo
        lista_filmes_dados = []

        for l in urls_arquivo:
            url = l
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            filme_titulo = ""
            nota = ""
            capa = ""
            filme_descricao = ""
            duracao = ""

            # titulo
            titulo_original_div = soup.find('div', class_="sc-94726ce4-3 eSKKHi")
            if titulo_original_div is not None:
                for t in titulo_original_div:
                    if "ul" not in str(t):
                        titulo = t.text.split(":")
                        filme_titulo = titulo[1].strip()

            # duracao
            div_especificacoes = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-none ipc-metadata-list--compact ipc-metadata-list--base")
            if div_especificacoes is not None:
                for esp in div_especificacoes:
                    if "Runtime" in esp.text:
                        duracao = esp.text.replace("Runtime", "")


            #nota avaliacao
            nota_avaliacao = soup.find('span', class_='sc-7ab21ed2-1 jGRxWM')
            if nota_avaliacao is not None:
                nota = nota_avaliacao.text

            #imagem
            imagem_capa_div = soup.find('div', class_='ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img')
            if imagem_capa_div is not None:
                imagem_tag = imagem_capa_div.find(('img'))
                capa = imagem_tag['src']

            # descricao
            descricao = soup.find('span', class_='sc-16ede01-2 gXUyNh')
            if descricao is not None:
                filme_descricao = descricao.text

            # Montar lista para o arquivo
            if filme_titulo == "" or filme_descricao == "" or nota == "" :
                continue

            filme_dados = (filme_titulo, filme_descricao, nota, duracao, capa)
            registro = ";".join(filme_dados)
            lista_filmes_dados.append(registro)
            print(registro)

        # salvar dados em um arquivo txt
        with open("lista_filmes.txt", "w") as regis:
            for ls in lista_filmes_dados:
                regis.write(ls + "\n")


    except Exception as e:
        print(e)

def importar_dados():
    try:
        print("importar_dados")
        filebase = "lista_filmes.txt"


        #Instanciar conexao com o MongoDB
        client = MongoClient('mongodb://jobimportador_mongodb_1')
        db = client['Filmes']
        col = db['Dados']

        #Realizar a leitura dos arquivos baixados salvos na pasta
        fileRead = open(filebase, 'r')

        for line in fileRead:
            texto = line.split(';')
            print(len(texto))
            print(texto[0])
            print(texto[1])
            print(texto[2])
            print(texto[3])
            print(texto[4])

            #Salvar os dados válidos no banco
            col.insert_many(
                [
                    {
                        "Titulo": texto[0],
                        "Descricao": texto[1],
                        "Nota": texto[2],
                        "Duracao": texto[3],
                        "Capa": texto[4]
                    }
                ]
            )

            print("Inserido")

        fileRead.close()
        os.remove(filebase)
    except Exception as e:
        #Salvar os dados com erro em um arquivo txt
        print(e)


download_urls_para_arquivo()
scrapping_dados_urls()
importar_dados()