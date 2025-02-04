import pandas as pd
import re


caminho_arquivo = 'base.xlsx'  
df = pd.read_excel(caminho_arquivo, dtype=str)


df.columns = df.columns.str.strip()


colunas_fone = ['Fone 1', 'fone 2', 'Fone 3', 'Fone 4', 'Fone 5']  
id_vars = ['fullname'] 


df_melted = df.melt(id_vars=id_vars, value_vars=colunas_fone, var_name='Tipo', value_name='Fone')


df_melted.dropna(subset=['Fone'], inplace=True)
df_melted['Fone'] = df_melted['Fone'].astype(str).str.strip()


def formatar_numero(numero):
    numero = re.sub(r'\D', '', numero) 
    
    if len(numero) == 11:  
        return f"55{numero}"
    elif len(numero) == 10: 
        return f"55{numero}"
    return ""

df_melted['Fone'] = df_melted['Fone'].apply(formatar_numero)

df_melted = df_melted[df_melted['Fone'] != ""]


df_melted.drop_duplicates(subset=['fullname', 'Fone'], inplace=True)

contagem_fones = df_melted['Fone'].value_counts()


fones_duplicados = contagem_fones[contagem_fones > 1].index
df_duplicados = df_melted[df_melted['Fone'].isin(fones_duplicados)]


df_unicos = df_melted[~df_melted['Fone'].isin(fones_duplicados)]


df_unicos = df_unicos.sort_values(by=['fullname'])
df_duplicados = df_duplicados.sort_values(by=['fullname'])


if not df_unicos.empty:
    df_unicos.to_excel('lista_formatada.xlsx', index=False)
    print("Arquivo 'lista_formatada.xlsx' salvo com os números únicos.")

if not df_duplicados.empty:
    df_duplicados.to_excel('duplicados.xlsx', index=False)
    print(" Arquivo 'duplicados.xlsx' salvo com os números duplicados.")

print("Processamento concluído com sucesso!")
