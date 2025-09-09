import os
import sys
import subprocess
import requests
import zipfile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException

from logger_utils import get_logger

class SeleniumUtils:
    """
    Classe para gerenciar Selenium com Chrome.
    - Validação da versão exata do Chrome.
    - Download automático do ChromeDriver local se necessário.
    - Logging centralizado via logger_utils.
    - Abrir URLs de forma segura.
    """

    #padrão do meu pc pessoal, caos necessário, alterem este valor.
    #VERSAO_CHROME_ESPERADA = "139.0.7258.155"

    def __init__(self, versao_chrome=None):
        # Logger centralizado
        self.logger = get_logger(self.__class__.__name__)
        self._driver = None
        self.versao_chrome = versao_chrome
        self._setup_chromedriver()

    """ DEVIDO A ATUALIZAÇÕES DA PLATAFORMA DO CHROME, ESTÁ FORMA NÃO É MAIS FUNCIONAL PARA CHROME SUPERIOR AO MODELO 114
        DRIVER BAIXADO DE FORMA MANUAL"""
    def _setup_chromedriver(self):
        """Baixa o ChromeDriver para Windows x32 (última versão por padrão) e extrai para raiz do projeto."""
        try:
            destino = os.path.dirname(os.path.abspath(__file__))
            caminho_driver = os.path.join(destino, "chromedriver.exe")
            print(caminho_driver)
            if os.path.exists(caminho_driver):
                self.logger.info(f"ChromeDriver já existe em: {caminho_driver}")
                
                self._driver_path = caminho_driver
                return caminho_driver
            else:
                raise Exception("Falha oa localizar chromedriver, atualize de forma manual no diretório")
        except Exception as e:
            self.logger.error(f"Erro ao baixar ou extrair ChromeDriver: {e}")
            sys.exit(1)
        """
        try:
            # Obtém última versão se não foi passada
            if not self.versao_chrome:
                url_versao = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
                resp = requests.get(url_versao, timeout=30)
                resp.raise_for_status()
                self.versao_chrome = resp.text.strip()
            self.logger.info(f"Versão do ChromeDriver selecionada: {self.versao_chrome}")

            # URL de download para Windows x32
            url = f"https://chromedriver.storage.googleapis.com/{self.versao_chrome}/chromedriver_win32.zip"
            self.logger.info(f"Baixando ChromeDriver de: {url}")

            zip_path = os.path.join(destino, "chromedriver.zip")
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)

            # Extrai apenas chromedriver.exe
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                for member in zip_ref.namelist():
                    if member.lower().endswith("chromedriver.exe"):
                        zip_ref.extract(member, destino)
                        extraido = os.path.join(destino, member)
                        if extraido != caminho_driver:
                            os.replace(extraido, caminho_driver)
                        break

            os.remove(zip_path)
            self.logger.info(f"ChromeDriver baixado com sucesso em: {caminho_driver}")
            self._driver_path = caminho_driver
            return caminho_driver
            """
        
            

    def open_chrome(self, url: str):
        """Abre o Chrome e navega até a URL especificada."""
        if not hasattr(self, "_driver_path"):
            self.logger.error("ChromeDriver não configurado corretamente.")
            sys.exit(1)

        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            #chrome_options.add_argument("--headless=new")  # opcional para CI/CD

            service = Service(self._driver_path)
            self._driver = webdriver.Chrome(service=service, options=chrome_options)

            navegador = self._driver.capabilities.get("browserVersion")
            self.logger.info(f"Abrindo URL: {url} com navegador versão {navegador}")
            self._driver.get(url)

        except WebDriverException as e:
            self.logger.error(f"Erro ao abrir o Chrome: {e}")
            sys.exit(1)

    def get_driver(self):
        """Retorna a instância atual do WebDriver."""
        return self._driver

    def fechar(self):
        """Fecha o navegador de forma segura."""
        if self._driver:
            self._driver.quit()
            self.logger.info("Driver fechado com sucesso.")

    #funções de suporte
    def wait_element(self, element, timeout=15, by=By.XPATH):
        """
        Espera até que um elemento esteja presente no DOM.
        :param by: Tipo de identificador (ex: By.ID, By.XPATH, By.CSS_SELECTOR).
        :param element: String do seletor.
        :param timeout: Tempo máximo de espera (default 15s).
        """
        try:
            self.logger.info(f"Aguardando elemento presente: {element}")
            element = WebDriverWait(driver=self._driver, timeout=timeout).until(
                EC.presence_of_element_located((by, element))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Timeout: elemento '{element}' não encontrado em {timeout}s.")
            raise

    def wait_element_visible(self, element, timeout=15, by=By.XPATH):
        """
        Espera até que um elemento esteja visível na tela.
        :param by: Tipo de seletor (ex: By.ID, By.XPATH, By.CSS_SELECTOR).
        :param element: String do seletor.
        :param timeout: Tempo máximo de espera (default 15s).
        :return: WebElement visível ou None.
        """
        try:
            self.logger.info(f"Aguardando visibilidade do elemento: {element}")
            element = WebDriverWait(driver=self._driver, timeout=timeout).until(
                EC.visibility_of_element_located((by, element))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Timeout: elemento '{element}' não ficou visível em {timeout}s.")
            raise

    def wait_elements(self, element, timeout=15, by=By.XPATH):
        """
        Espera até que mais de um elemento esteja pronto.
        :param by: Tipo de seletor (ex: By.ID, By.XPATH, By.CSS_SELECTOR).
        :param element: String do seletor.
        :param timeout: Tempo máximo de espera (default 15s).
        :return: List WebElement visível ou None.
        """
        try:
            self.logger.info(f"Aguardando visibilidade do elemento: {element}")
            element = WebDriverWait(driver=self._driver, timeout=timeout).until(
                EC.visibility_of_all_elements_located((by, element))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Timeout: elemento '{element}' não ficou visível em {timeout}s.")
            raise

    
    def click_element(self, element, timeout=15, by=By.XPATH):
        """
        Aguarda e clica em um elemento.
        Usa a função wait_element_visible para garantir que esteja clicável.
        :param by: Tipo de seletor (ex: By.ID, By.XPATH, By.CLASS).
        :param element: String do seletor.
        :param timeout: Tempo máximo de espera (default 15s).
        """
        self.logger.info(f"Tentando clicar no elemento: {element}")
        element = self.wait_element_visible(by=by, element=element, timeout=timeout)
        if element:
            try:
                element.click()
                self.logger.info(f"Elemento clicado com sucesso: {element}")
            except Exception as e:
                self.logger.error(f"Erro ao clicar no elemento '{element}': {e}")
                raise
        else:
            self.logger.error(f"Não foi possível clicar, elemento '{element}' não encontrado/visível.")
        

    def digitar_e_validar(self, element, text, timeout=15,by=By.XPATH):
        """Digita um texto no elemento encontrado e valida se foi inserido corretamente."""
        elm = self.wait_element(by=by, element=element, timeout=timeout)

        try:
            elm.clear()
            elm.send_keys(text)
            self.logger.info(f"[DIGITAR] Texto '{text}' digitado em {by}={element}")

            # validar se foi realmente digitado
            valor = (elm.get_attribute("value") or elm.get_attribute("textContent") or elm.get_attribute("innerText"))
            if valor and text in valor:
                self.logger.info(f"[VALIDAR] Texto confirmado no elemento: '{valor}'")
                return True
            else:
                self.logger.warning(f"[VALIDAR] Texto não corresponde. Esperado: '{text}', Obtido: '{valor}'")
                return False

        except Exception as e:
            self.logger.error(f"[ERRO] Falha ao digitar em {by}={element} - {e}")
            raise

    def get_attribute_by_xpath(self, element, attribute, timeout=15, by=By.XPATH):
        """
        Localiza um elemento via XPATH e retorna o valor do atributo informado.
        """
        try:
            elem = self.wait_element(by, element, timeout)
            valor = elem.get_attribute(attribute)

            if valor is not None:
                self.logger.info(f"[GET_ATTRIBUTE] Atributo '{attribute}' encontrado em {xpath}: '{valor}'")
            else:
                self.logger.warning(f"[GET_ATTRIBUTE] Atributo '{attribute}' não encontrado em {xpath}")

            return valor
        except Exception as e:
            self.logger.error(f"[ERRO] Falha ao obter atributo '{attribute}' de {xpath} - {e}")
            raise

        
