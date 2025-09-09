# Coletor de Clima via API

Este projeto  coleta de dados meteorológicos da API  [ClimaTempo]([https://www.climatempo.com.br/](https://weatherstack.com/documentation)) utilizando **Python**.  
Os resultados retornados em um JSON são tratados e salvos em **CSV** de forma estruturada.

---
## Pré-requisitos

- **Python 3.9+** instalado e configurado no PATH.  
- **Windows** (execução principal via `.bat`).

---
## Dependências

As dependências são gerenciadas via **`api_requirements.txt`**:

```txt
logging==0.4.9.6
requests==2.32.5
```
o .bat criará uma virtualenv (venv/) automaticamente, instalará as dependências e rodará o script.

---

## Como executar

-Clone o repositório ou baixe os arquivos do projeto.
-Localize o arquivo 'start.bat' na raiz de cada do projeto.

Execute o comando no terminal:

```txt
start_program.bat "Bauru"
```


---
## Observações importantes
caso queira adicionar um traço ou uma virgula para colocar outro identificador como estado e país, pode ajudar
a api em questão, não é tão robusta em localização de Homónimos dentro do paises 

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
pip install -r api_requirements.txt
*python API_Main.py "Bauru - SP"*
```

---
## Sugestão
Sempre valide os logs disponibilizados
