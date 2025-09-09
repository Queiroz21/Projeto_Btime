import os
import csv
from datetime import datetime
from climatempo_utils import ClimaTempoUtils
from logger_utils import get_logger

def salvar_csv(dados, localidade):
        """
        Salva os dados em CSV dentro da pasta 'Dados'.
        - Se o arquivo não existir: cria com cabeçalho.
        - Se já existir: adiciona linha.
        """

        # Cria a pasta Dados se não existir
        pasta = os.path.join(os.getcwd(), "Dados")
        os.makedirs(pasta, exist_ok=True)

        # Nome do arquivo padrão: ClimaTempo_Cidade_dd_mm_yyyy.csv
        data_hoje = datetime.now().strftime("%d_%m_%Y")
        cidade_formatada = localidade.replace(" - ", "_")
        nome_arquivo = f"ClimaTempo_{cidade_formatada}_{data_hoje}.csv"
        caminho_arquivo = os.path.join(pasta, nome_arquivo)

        # Verifica se o arquivo existe
        arquivo_existe = os.path.exists(caminho_arquivo)

        try:
            with open(caminho_arquivo, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=dados.keys())
                # Se não existir -> escreve cabeçalho
                if not arquivo_existe:
                    writer.writeheader()
                    logger.info(f"Cabeçalho criado no CSV: {caminho_arquivo}")

                # Escreve os dados
                writer.writerow(dados)

            logger.info(f"Dados salvos com sucesso em: {caminho_arquivo}")
        except Exception as e:
            logger.error(f"Erro ao salvar CSV: {e}")


if __name__ == "__main__":
    #localidade = 'aaaaa - SP'
    logger = get_logger("BuscadorCidade_WEB")
    localidade = sys.argv[1]
    
    if " - " not in localidade:
        print("Uso: python main.py <'Local - Sigla'> (utilize aspas no nome a ser buscado)")
        sys.exit(1)
        
    busca = localidade.split(" - ")[0]
    try:
        ctu = ClimaTempoUtils()
        ctu.open_web()
        ctu.busca_clima(localidade=localidade, localidade_parcial=busca)
        ctu.aguarda_clima_15()
        dados = ctu.coleta_dados()
        salvar_csv(dados=dados,localidade=localidade)
    except Exception as e:
        logger.error(f"Revise as configurações e logs base do programa para melhor análise causa/raíz")
    finally:
        ctu.finalizar()
    
