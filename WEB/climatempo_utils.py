from selenium_utils import SeleniumUtils

# Conjunto de XPaths centralizados (boa prática: constantes UPPER_CASE)
XPATH_INPUT_BUSCA = '//input[@type="search" and @placeholder="Busque por uma cidade..."]'
XPATH_CIDADE_LOCALIZADA = '//h6[.="Cidades"]/..//span[text()="{}"]'
XPATH_TITULO_ESPERA_CARREGAMENTO = '//a[@title="{}"]'
OPCAO_CLIMA_15_DIAS = 'Previsão 15 dias para '
XPATH_CARDS_COM_DADOS = '//input[@id="chk-accordion-daily-info-1"]/..//div[contains(@class,"variable-card")]'

class ClimaTempoUtils:
    """
    Classe modular para interagir com a página do ClimaTempo.
    Permite abrir a página, buscar por uma localidade, aguardar o carregamento
    e coletar dados meteorológicos de forma estruturada, permitindo implementação de novas funções.
    """
    def __init__(self, url="https://www.climatempo.com.br/"):
        self.selenium_util = SeleniumUtils()
        self.url = url
        self.logger = self.selenium_util.logger  # Reaproveitar logger já configurado
        self.localidade = None  # guardamos a cidade pesquisada para nomear o CSV

        
    def open_web(self):
        """Abre a página inicial do ClimaTempo e aguarda o campo de busca ficar visível."""
        self.selenium_util.open_chrome(self.url)
        self.selenium_util.wait_element_visible(element =XPATH_INPUT_BUSCA)
        self.logger.info("Página aberta com sucesso")

    def busca_clima(self, localidade, localidade_parcial):
        """
        Realiza a busca de uma cidade no campo de pesquisa:
        - Digita o nome parcial da localidade.
        - Seleciona a opção correspondente ao nome completo. (devido a comportamento mapeado da página)
        Retorna um dicionário estruturado.
        """
        self.localidade = localidade
        self.selenium_util.click_element(element=XPATH_INPUT_BUSCA)
        self.selenium_util.digitar_e_validar(element=XPATH_INPUT_BUSCA, text=localidade_parcial)
        self.logger.info("Texto parcial inserido")
        self.selenium_util.click_element(element=XPATH_CIDADE_LOCALIZADA.format(localidade))
        self.logger.info("Localidade selecionada com sucesso")

    def aguarda_clima_15(self):
        """
        Aguarda a página de clima estar carregada usando o título esperado.
        """
        parcial = self.localidade.split(" - ")[0]
        self.selenium_util.click_element(element =XPATH_TITULO_ESPERA_CARREGAMENTO.format(f'{OPCAO_CLIMA_15_DIAS}{parcial}'))
        self.logger.info("Carregamento de clima finalizado.")
    
    def coleta_dados(self):
        """
        Coleta informações meteorológicas a partir dos cards exibidos na página.
        Retorna um dicionário estruturado.
        """
        # Espera múltiplos elementos (cards) ficarem visíveis
        sections = self.selenium_util.wait_elements(element=XPATH_CARDS_COM_DADOS,timeout=20)
        self.logger.info("Seção de cards coletada")
        dados = {}

        for sc in sections:
            linhas = [linha.strip() for linha in sc.text.split("\n") if linha.strip()]
            if not linhas:continue

            titulo = linhas[0].upper()

            # Ignora linhas desnecessárias
            if "ARCO" in titulo:
                self.logger.info("Pulando card de arco iris")
                continue

            # Caso especial: Nascer/Pôr do Sol
            if titulo == "SOL" and len(linhas) >= 2:
                try:
                    nascer, por = linhas[1].split(" - ", maxsplit=1)
                    dados["NASCER DO SOL"] = nascer.strip()
                    dados["POR DO SOL"] = por.strip()
                    self.logger.info("Dados referente a sol tratado com sucesso")
                except ValueError:
                    self.logger.warning(f"Formato inesperado para SOL: {linhas}")
                continue

            # Caso genérico: chave + valor (não possuem min/max)
            if len(linhas) == 2:
                dados[titulo] = linhas[1].strip()

            # Caso com mínimo e máximo
            elif len(linhas) == 3:
                dados[f"{titulo} MIN"] = linhas[1].strip()
                dados[f"{titulo} MAX"] = linhas[2].strip()

            #captura estrutura inesperada para debug
            else:
                self.logger.warning(f"Formato inesperado em card: {linhas}")

        return dados

    def finalizar(self):
        self.selenium_util.fechar()

