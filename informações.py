import pandas as pd
arquivo=pd.read_excel("barragens_sem_aspas.xlsx", engine="openpyxl")
arquivo.info()