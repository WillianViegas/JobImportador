from pymongo import MongoClient
from bs4 import BeautifulSoup


def download_arquivo():
    try:
        #Obter urls para download de algum site
        #Salvar as urls em um arquivo txt
        #Fazer tratativa no arquivo para nao repetir as urls
        #realizar o download utilizando as urls salvas e guardar o que foi baixado em uma pasta
        print("download_arquivo")
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


download_arquivo()
importar_dados()