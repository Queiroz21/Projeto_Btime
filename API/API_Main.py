import os
import sys
import csv
import requests

from datetime import datetime

from API_Functions import BuscadorClimaCidade
from logger_utils import get_logger


def salvar_campos_json_csv(json_data, campos_map: dict, cidade: str):
    """
    Salva campos específicos de um JSON em CSV usando nomes de colunas customizados.
    """
    logger.info(f"Iniciando salvamento do CSV para a cidade: {cidade}")

    if isinstance(json_data, dict):
        json_data = [json_data]

    pasta_dados = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dados")
    os.makedirs(pasta_dados, exist_ok=True)

    nome_arquivo = f"ClimaTempo_{cidade}_{datetime.now().strftime('%d_%m_%Y')}.csv"
    caminho_arquivo = os.path.join(pasta_dados, nome_arquivo)
    logger.info(f"Pasta e arquivo .csv iniciados com sucesso!")
    # Se o arquivo não existir, forçamos a criação
    criar_cabecalho = not os.path.isfile(caminho_arquivo)

    def extrair_valor(item, campo):
        """Extrai valor de um campo ou subcampo usando notação ponto.
            Metodologia escolhida devido a forma de devolução do JSON com a co-relação do nome das colunas
            Permitindo que em situações futuras, se torne mais fácil a manutenção"""
        partes = campo.split(".")
        valor = item
        for parte in partes:
            if isinstance(valor, dict):
                valor = valor.get(parte, "")
            else:
                valor = ""
        return valor

    try:
        with open(caminho_arquivo, mode="a", newline="", encoding="utf-8") as csv_file:
            #trabalhando com o módulo csv, para escrever diretamente os campos do JSON/Dict, evitando contornos de de-para
            writer = csv.DictWriter(csv_file, fieldnames=campos_map.values())

            if criar_cabecalho: #validação anterior, caso o arquivo não exista, criará a primeira linha, seguindo premissa que sempre se buscará as mesmas informações
                writer.writeheader()
                logger.info(f"Cabeçalho criado no CSV: {caminho_arquivo}")

            #percorrendo todo o json para coletar os dados escolhidos e agrupalos como solicitado.
            for item in json_data:
                linha = {nome_coluna: extrair_valor(item, campo_json)
                         for campo_json, nome_coluna in campos_map.items()}
                writer.writerow(linha)

        logger.info(f"CSV salvo com sucesso: {caminho_arquivo}")
    except Exception as e:
        logger.error(f"Erro ao salvar o CSV: {e}")
        

if __name__ == "__main__":
    logger = get_logger("BuscadorCidade")
    

    nome_script = os.path.basename(__file__)  # pega o nome real do script em execução
    if len(sys.argv) != 3:
        logger.error(f"Uso incorreto. Esperado: python {nome_script} 'Nome Local' <CHAVE_API>")
        print(f"Uso: python {nome_script} 'Nome Local' <CHAVE_API>")
        sys.exit(1)

    localidade = sys.argv[1]
    chave_api = sys.argv[2]

    try:
        buscador = BuscadorClimaCidade(chave_api)
        resultado = buscador.buscar_cidade(localidade)
        logger.info(f"Resultado obtido: {resultado}")
        campos = {"request.query": "Cidade","location.country":"Pais", "current.astro.sunrise":"Nascer do Sol","current.astro.sunset":"Por do Sol","current.astro.moon_phase":"Lua","current.temperature":"Temperatura atual","current.humidity":"Umidade atual","current.wind_speed":"Velocidade Vento", "current.wind_degree":"Grau do vento", "current.wind_dir":"Direção do vento"}
        salvar_campos_json_csv(json_data=resultado,campos_map=campos,cidade=localidade)
        logger.info("Resultado da busca salvo dentro do diretório: 'Dados'")
    except Exception as e:
        logger.error(f"Erro durante execução: {e}")
        print("Erro:", e)
        
print("Execução finalizada, consulte o LOG para mais informações")

