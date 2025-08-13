import streamlit as st
from database import Database, EmbeddingModel
from scopus_api import busca_fwci_artigo
from datetime import datetime

driver = Database()
embeddingModel = EmbeddingModel()

SEARCH_TYPE = 0


def computa_info_professores(data):
    professores = {}
    for doc, score in data:
        artigo = doc.page_content
        autor = driver.busca_nome_prof(artigo)
        ano = doc.metadata.get("anoPublicado")
        h_index = driver.busca_hindex_prof(autor)
        fwci = busca_fwci_artigo(artigo)
        if autor in professores:
            professores[autor]["artigos"].append({
                "titulo": artigo,
                "ano": ano,
                "precision_score": score,
                "fwci": fwci,
            })
        else:
            professores[autor] = {
                "h_index": h_index,
                "artigos": [{
                    "titulo": artigo,
                    "ano": ano,
                    "precision_score": score,
                    "fwci": fwci
                }]
            }
    return professores


def calculate_max_fwci(professores):
    fwcis = []
    for prof, info in professores:
        for article in info["artigos"]:
            fwcis.append(article["fwci"])

    return max(fwcis)


def calcula_art_score(fwci, maxFwci, anoArtigo, score):
    anoAtual = datetime.now().year
    normalized_fwci = fwci / maxFwci
    if fwci == 0:
        return (score / (anoAtual - anoArtigo)) * 10
    if anoArtigo != anoAtual:
        return (normalized_fwci * score**2 / (anoAtual - anoArtigo)) * 10
    else:
        return (normalized_fwci * score**2) * 10


def calculate_color_by_score(score):
    if score >= 1:
        color = '#00ff7f'
    elif score >= 0.5 and score <= 0.3:
        color = '#32cd32'
    else:
        color = '#adff2f'
    return color


def formata_markdown(professores):
    final_md = "<ul>"

    sorted_profs = sorted(professores.items(), key=lambda x: x[1]["h_index"],
                          reverse=True) if SEARCH_TYPE else professores.items()

    for prof, info in sorted_profs:
        final_md += f"<li><strong>{prof}</strong><br>"
        for article in info["artigos"]:
            maxFwci = calculate_max_fwci(sorted_profs)
            artScore = calcula_art_score(article["fwci"],
                                         maxFwci,
                                         article["ano"],
                                         article["precision_score"])
            color = calculate_color_by_score(artScore)
            final_md += f'''<ul>
            <li><span style='background-color: {color}; border-radius: 3px;
                padding-bottom: 5px;'>
                {article["titulo"]} - {article["ano"]}: {artScore}
                </span></li>
            </ul>'''
    final_md += "</ul>"
    return final_md


input = st.text_input(
    "Pesquise por algum tema de seu interesse: ", key="query")

if input:
    data = embeddingModel.busca_artigos(st.session_state.query)

    import torch
    torch.cuda.empty_cache()
    st.write(f"Aqui estão alguns professores que tem relação com: {
             st.session_state.query}")

    professores = computa_info_professores(data)

    final_md = formata_markdown(professores)

    st.markdown(final_md, unsafe_allow_html=True)
