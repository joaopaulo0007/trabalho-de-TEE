import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

arquivo = pd.read_excel("barragens_sem_aspas.xlsx", engine="openpyxl")
regioes={}
regioes['Nordeste']=['SE','PB','BA','PI','RN','PE','AL','CE','MA']
regioes['Sul']=['RS','SC','PR']
regioes['Sudeste']=['RJ','SP','ES','MG']
regioes['Centro oeste']=['GO','DF','MT','MS']
regioes['Norte']=['AM','RR','RO','AC','PA','TO','AP']
arquivo['Região']=arquivo['UF'].map({estado: regiao for regiao, estados in regioes.items() for estado in estados})

arquivo_dano_potencial_counts = (
    arquivo["Dano Potencial Associado - DPA"].value_counts().reset_index()
)
arquivo_dano_potencial_counts.columns = [
    "Dano Potencial Associado - DPA",
    "Número de Barragens",
]
arquivo_dano_potencial_counts.to_excel(
    "dano potencial.xlsx", index=False, engine="openpyxl"
)

arquivo_situação_operacional_counts=(
    arquivo["Situação Operacional"].value_counts().reset_index()
)
arquivo_situação_operacional_counts.columns=[
    "Situação Operacional",
    "Número de barragens"
]

arquivo_situação_operacional_counts.to_excel(
    "situacao operacional.xlsx",index=False,engine='openpyxl'
)

arquivo_nivel_emergencia_counts = (
    arquivo["Nível de Emergência"].value_counts().reset_index()
)
arquivo_nivel_emergencia_counts.columns = ["Nível de Emergência", "Número de Barragens"]
arquivo_nivel_emergencia_counts.to_excel(
    "nivel emergencia.xlsx", index=False, engine="openpyxl"
)

tipo_barragem_counts = (
    arquivo["Tipo de Barragem de Mineração"].value_counts().reset_index()
)
tipo_barragem_counts.columns = ["Tipo de Barragem de Mineração", "Número de Barragens"]
tipo_barragem_counts.to_excel("tipo barragem.xlsx", index=False, engine="openpyxl")

tipo_minerio_counts = (
    arquivo["Minério principal presente no reservatório"].value_counts().reset_index()
)
tipo_minerio_counts.columns = [
    "Minério principal presente no reservatório",
    "Número de Barragens",
]
tipo_minerio_counts.to_excel("tipo minerio.xlsx", index=False, engine="openpyxl")

usinas_counts = arquivo["Usinas"].value_counts().reset_index()
usinas_counts.columns = ["Usinas", "Número de Barragens"]
usinas_counts.to_excel("usinas.xlsx", index=False, engine="openpyxl")

dano_potencial_regiao = arquivo.groupby(['Região', 'Dano Potencial Associado - DPA']).size().reset_index(name='Quantidade de usinas com dano potencial por região')

dano_potencial_regiao.to_excel("dano potencial por regiao.xlsx",index=False, engine='openpyxl')

plt.bar(
    arquivo_dano_potencial_counts["Dano Potencial Associado - DPA"],
    arquivo_dano_potencial_counts["Número de Barragens"],
)
plt.xlabel("Dano Potencial Associado - DPA")
plt.ylabel("Número de Barragens")
plt.title("Número de Barragens por Dano Potencial")
plt.savefig("dano_potencial_plot.png")
plt.show()

plt.bar(
    arquivo_nivel_emergencia_counts["Nível de Emergência"],
    arquivo_nivel_emergencia_counts["Número de Barragens"],
)
plt.xlabel("Nível de Emergência")
plt.ylabel("Número de Barragens")
plt.title("Número de Barragens por Nível Emergencial")
plt.xticks(rotation=90, ha="right")
plt.savefig("nivel_emergencial.png")
plt.show()

plt.bar(
    tipo_barragem_counts["Tipo de Barragem de Mineração"],
    tipo_barragem_counts["Número de Barragens"],
)
plt.xlabel("Tipo de Barragem de Mineração")
plt.ylabel("Número de Barragens")
plt.title("Número de Barragens por Tipo de Barragem")
plt.xticks(rotation=90, ha="right")
plt.tight_layout()
plt.savefig("tipo_barragem_plot.png")
plt.show()


tipo_minerio_counts_copy = tipo_minerio_counts.copy()
usinas_counts_copy = usinas_counts.copy()

tipo_minerio_counts_copy[
    "Minério principal presente no reservatório"
] = tipo_minerio_counts_copy.apply(
    lambda row: row["Minério principal presente no reservatório"]
    if row["Número de Barragens"] >= 15
    else "Outros",
    axis=1,
)

tipo_minerio_grouped = (
    tipo_minerio_counts_copy.groupby("Minério principal presente no reservatório")
    .sum()
    .reset_index()
)

plt.pie(
    tipo_minerio_grouped["Número de Barragens"],
    labels=tipo_minerio_grouped["Minério principal presente no reservatório"],
    autopct="%1.1f%%",
    startangle=140,
)
plt.axis("equal")
plt.title("Distribuição de Barragens por Tipo de Minério")
plt.legend(
    title="Tipos de Minério", bbox_to_anchor=(1, 0.5), loc="center left", fontsize=8
)
plt.savefig("tipo minerio.png")
plt.show()

usinas_counts_copy["Usinas"] = usinas_counts_copy.apply(
    lambda row: row["Usinas"] if row["Número de Barragens"] >= 15 else "Outros", axis=1
)

usinas_grouped = usinas_counts_copy.groupby("Usinas").sum().reset_index()

plt.pie(
    usinas_grouped["Número de Barragens"],
    labels=usinas_grouped["Usinas"],
    autopct="%1.1f%%",
    startangle=140,
)
plt.axis("equal")
plt.title("Usinas")
plt.legend(title="Usinas", bbox_to_anchor=(1, 0.5), loc="center left", fontsize=8)
plt.savefig("usinas.png")
plt.show()


cores_regioes = {
    'Centro oeste': 'blue',
    'Nordeste': 'orange',
    'Norte': 'green',
    'Sudeste': 'red',
    'Sul': 'purple'
}


cores = dano_potencial_regiao['Região'].map(cores_regioes)

plt.bar(
    dano_potencial_regiao["Região"] + '-' + dano_potencial_regiao['Dano Potencial Associado - DPA'],
    dano_potencial_regiao["Quantidade de usinas com dano potencial por região"],
    color=cores
)

legendas = [plt.Rectangle((0,0),1,1, color=cores_regioes[regiao], edgecolor='none') for regiao in cores_regioes]
plt.legend(legendas, cores_regioes.keys(), title='Região')

plt.xlabel("Região - Dano Potencial")
plt.ylabel("Número de Barragens")
plt.title("Quantidade de usinas com dano potencial por região")
plt.xticks(rotation=90, ha="right")
plt.tight_layout()
plt.savefig("Quantidade de usinas com dano potencial por região.png")
plt.show()

