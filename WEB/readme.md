# Coletor de Clima com Selenium

Este projeto automatiza a coleta de dados meteorológicos do site [ClimaTempo](https://www.climatempo.com.br/) utilizando **Selenium + Python**.  
Os resultados retornados em um JSON são tratados e salvos em **CSV** de forma estruturada.

---
## Pré-requisitos

- **Google Chrome** instalado na máquina.  
   Importante: o **ChromeDriver** deve ser **inferior à versão 140** (a versão recomendada está disponível no projeto.).  
- **Python 3.9+** instalado e configurado no PATH.  
- **Windows** (execução principal via `.bat`).

---
## Dependências

As dependências são gerenciadas via **`requirements.txt`**:

```txt
logging==0.4.9.6
requests==2.32.5
pandas==2.3.2
env==0.1.0
selenium==4.35.0
```
o .bat criará uma virtualenv (venv/) automaticamente, instalará as dependências e rodará o script.

---

## Como executar

-Clone o repositório ou baixe os arquivos do projeto.
-Localize o arquivo 'start.bat' na raiz de cada do projeto.

Execute o comando no terminal:

```txt
start_program.bat "Bauru - SP"
```

---
## Observações importantes
```txt
Sempre coloque o nome da cidade entre aspas, pois pode haver espaços.
Evite nomes totalmente em maiúsculas.

Forma correta -> "Bauru - SP"
Forma que falha -> "BAURU - SP" (a página não reconhece corretamente).
```

---
## Estrutura de saída

Os arquivos serão criados dentro da pasta Dados/ (na raiz do projeto), no formato:
**ClimaTempo_<Cidade>_dd_mm_yyyy.csv**
Ex: *Dados/ClimaTempo_Bauru_SP_09_09_2025.csv*

---
## Execução manual (opcional)

Caso não queira usar o .bat, você pode rodar manualmente:

```txt
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
*python main.py "Bauru - SP"*
```

---
## Sugestão
Sempre valide se a versão do Chrome instalada é compatível com o ChromeDriver (máximo 139.x).
