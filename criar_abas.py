import pandas as pd
from datetime import datetime
import os

def criar_abas_mensais(arquivo_entrada):
    """
    Cria abas mensais em um arquivo Excel, mantendo as existentes.
    
    Args:
        arquivo_entrada (str): Caminho do arquivo Excel de entrada
    """
    
    # Ler o arquivo Excel e verificar abas existentes
    xls = pd.ExcelFile(arquivo_entrada)
    abas_existentes = xls.sheet_names
    df_modelo = pd.read_excel(xls, sheet_name=abas_existentes[0])  # Usa a primeira aba como modelo
    
    # Criar um novo ExcelWriter para o arquivo de saída
    nome_saida = os.path.splitext(arquivo_entrada)[0] + '_com_abas_mensais.xlsx'
    with pd.ExcelWriter(nome_saida, engine='openpyxl') as writer:
        
        # Copiar todas as abas existentes primeiro
        for aba in abas_existentes:
            pd.read_excel(xls, sheet_name=aba).to_excel(
                writer, 
                sheet_name=aba, 
                index=False
            )
        
        # Criar abas para os meses faltantes
        ano_atual = datetime.now().year
        meses_existentes = [aba.split('_')[-1] for aba in abas_existentes if aba.startswith(str(ano_atual))]
        
        for mes in range(1, 13):
            nome_aba = f"{ano_atual}_{mes:02d}"
            if nome_aba not in abas_existentes:
                df_modelo.to_excel(writer, sheet_name=nome_aba, index=False)
                
    print(f"Arquivo gerado com sucesso: {nome_saida}")
    return nome_saida

if __name__ == "__main__":
    # Configuração
    arquivo_input = 'dados.xlsx'  # Nome do arquivo de entrada
    
    # Chamar a função principal
    try:
        output_file = criar_abas_mensais(arquivo_input)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        exit(1)
