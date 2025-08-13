import requests
from dotenv import load_dotenv
import urllib.parse
load_dotenv()


def busca_prof_hindex(nome_prof):
    nome_completo = nome_prof.split()
    nome = nome_completo[0]
    sobrenome = nome_completo[-1]
    url = f"https://api.openalex.org/authors?filter=display_name.search:{
        nome}%20{sobrenome}"

    try:
        resp = requests.get(url)
        resp.raise_for_status()

        data = resp.json()
        prof_count = 0
        id_instituicao = ""
        while (id_instituicao != "https://openalex.org/I2699952"
               and prof_count <= len(data["results"])):
            prof = data["results"][prof_count]
            id_instituicao = prof["affiliations"][0]["institution"]["id"]
            prof_count += 1

        if (prof_count > len(data["results"])):
            return
        else:
            h_index = prof["summary_stats"]["h_index"]
            return h_index

    except Exception as e:
        print(e)


def busca_fwci_artigo(nome_artigo):
    encoded_nome = urllib.parse.quote(nome_artigo)
    url = f"https://api.openalex.org/works?search={
        encoded_nome}"

    try:
        resp = requests.get(url)
        resp.raise_for_status()

        data = resp.json()

        if not data["results"]:
            fwci = 0
            return float(fwci)

        work = data["results"][0]
        if not work["fwci"]:
            fwci = 0
            return float(fwci)

        fwci = float(work["fwci"])
        return fwci
    except Exception as e:
        print(e)

