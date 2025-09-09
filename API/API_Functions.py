import os
import sys
import requests

from datetime import datetime

from logger_utils import get_logger

"""OBSERVAÇÕES
O modelo de API escolhido, foi um público envolvendo clima de cidades, algo simples.
Apesar da pouca segurança, a estrutura da API segue passando parametro via link de requisição ao invés do corpo,
case escolhido somente devido a ser cenário de testes e hipotético.
"""

class BuscadorClimaCidade:
    def __init__(self, chave_api: str, url_base: str = "https://api.weatherstack.com/current"):
        self._chave_api = chave_api.strip() #evitar falha de digitação no cmd ou .bat
        self._url_base = f"{url_base}?access_key={self._chave_api}"
        self._tempo_limite = 10  # segurança contra requisições travadas
        self.logger = get_logger(self.__class__.__name__)

    def _tratar_erros(self, codigo_status: int):
        """Mapeia os erros possíveis para mensagens customizadas, informado na própria API."""
        mapa_erros = {
            404: "404_nao_encontrado: O recurso solicitado não existe.",
            101: "nao_autorizado: Chave de acesso inválida ou ausente.",
            429: "muitas_requisicoes: Limite de solicitações atingido.",
            601: "consulta_ausente: Consulta inválida ou ausente."
        }
        if codigo_status in mapa_erros:
            self.logger.error(mapa_erros[codigo_status])
            raise Exception(mapa_erros[codigo_status])
        elif codigo_status != 200:
            msg = f"Erro inesperado (HTTP {codigo_status})."
            self.logger.error(msg)
            raise Exception(msg)

    def buscar_cidade(self, cidade: str):
        
        try:
            self.logger.info(f"Iniciando requisição para cidade '{cidade}'.")
            resposta = requests.get(
                url=self._url_base,
                params={"query":cidade},
                timeout=self._tempo_limite
            )
            self._tratar_erros(resposta.status_code)
            self.logger.info(f"Requisição bem-sucedida para cidade '{cidade}'.")
            return resposta.json()

        except requests.Timeout:
            self.logger.error("A requisição excedeu o tempo limite.")
            raise TimeoutError("A requisição excedeu o tempo limite.")
        except requests.RequestException as e:
            self.logger.error(f"Erro de requisição: {e}")
            raise Exception(f"Erro de requisição: {e}")
