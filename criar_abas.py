import pandas as pd
from datetime import datetime
import os

def criar_abas_mensais(arquivo_entrada):
    """
    Cria abas mensais com apenas os cabeçalhos, preservando dados existentes.
    """
    # Ler o arquivo e identificar abas existentes
    xls = pd.ExcelFile(arquivo_entrada)
    abas_existentes = xls.sheet_names
    df_modelo = pd.read_excel(xls, sheet_name=abas_existentes[0], nrows=0)  # Lê SÓ os cabeçalhos

    # Preparar arquivo de saída
    nome_saida = os.path.splitext(arquivo_entrada)[0] + '_com_abas_mensais.xlsx'
    
    with pd.ExcelWriter(nome_saida, engine='openpyxl') as writer:
        # Copiar TODAS as abas existentes (com dados completos)
        for aba in abas_existentes:
            pd.read_excel(xls, sheet_name=aba).to_excel(
                writer, 
                sheet_name=aba, 
                index=False
            )
        
        # Criar novas abas (apenas cabeçalhos) para meses faltantes
        ano_atual = datetime.now().year
        meses_existentes = [
            aba.split('_')[-1] 
            for aba in abas_existentes 
            if aba.startswith(str(ano_atual))
        ]

        for mes in range(1, 13):
            nome_aba = f"{ano_atual}_{mes:02d}"
            if nome_aba not in abas_existentes:
                df_modelo.to_excel(  # Grava só os cabeçalhos
                    writer, 
                    sheet_name=nome_aba, 
                    index=False
                )
    
    print(f"✅ Arquivo gerado: {nome_saida}")
    return nome_saida

if __name__ == "__main__":
    try:
        criar_abas_mensais('dados.xlsx')
    except Exception as e:
        print(f"❌ Erro: {e}")
