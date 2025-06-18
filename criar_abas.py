import pandas as pd
from datetime import datetime
import os

def criar_abas_mensais(arquivo_entrada, aba_original='Sheet1'):
    """
    Cria abas mensais em um arquivo Excel baseado em uma estrutura existente.
    
    Args:
        arquivo_entrada (str): Caminho do arquivo Excel de entrada
        aba_original (str): Nome da aba que servirá como modelo
    """
    
    # Ler o arquivo Excel original
    df_modelo = pd.read_excel(arquivo_entrada, sheet_name=aba_original)
    
    # Criar um novo ExcelWriter para o arquivo de saída
    nome_saida = os.path.splitext(arquivo_entrada)[0] + '_com_abas_mensais.xlsx'
    with pd.ExcelWriter(nome_saida, engine='openpyxl') as writer:
        
        # Manter a aba original (opcional)
        df_modelo.to_excel(writer, sheet_name=aba_original, index=False)
        
        # Criar uma aba para cada mês do ano atual
        ano_atual = datetime.now().year
        
        for mes in range(1, 13):
            nome_aba = f"{ano_atual}_{mes:02d}"  # Formato: YYYY_MM
            df_modelo.to_excel(writer, sheet_name=nome_aba, index=False)
            
    print(f"Arquivo gerado com sucesso: {nome_saida}")
    return nome_saida

if __name__ == "__main__":
    # Configuração padrão - pode ser alterada via argumentos
    arquivo_input = 'dados.xlsx'  # Arquivo padrão de entrada
    aba_modelo = 'Sheet1'  # Nome da aba modelo
    
    # Chamar a função principal
    output_file = criar_abas_mensais(arquivo_input, aba_modelo)
