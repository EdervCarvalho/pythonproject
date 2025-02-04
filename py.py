import pandas as pd
import re 

caminho_arquivo = 'base para  ferramenta de higienização.xlsx' 
df = pd.read_excel(caminho_arquivo)
df.columns = df.columns.str.strip()  


colunas_fone = ['Fone 1', 'fone 2', 'Fone 3', 'Fone 4', 'Fone 5'] 
id_vars = ['fullname']  


df_melted = df.melt(id_vars=id_vars, value_vars=colunas_fone, var_name='Tipo', value_name='Fone')


df_melted.dropna(subset=['Fone'], inplace=True)


def formatar_numero(numero):
    numero = re.sub(r'\D', '', str(numero))  

    if len(numero) == 11:  
        return f"+55 ({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    elif len(numero) == 10:  
        return f"+55 ({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    else:
        return numero 


df_melted['Fone'] = df_melted['Fone'].apply(formatar_numero)


df_melted.drop_duplicates(inplace=True)


df_melted.to_excel('saida_formatada.xlsx', index=False)

print("✅ Processamento concluído com sucesso!")
