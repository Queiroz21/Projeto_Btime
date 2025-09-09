# Projeto_Btime
Um projeto para testar as habilidade de utilização de API e Webscrapping no cenário de consumo de dados web de forma simples

---
# Logs
Toda implementação de Log foi feito atraves do modulo Logging do Python, sendo desenvolvido de uma forma a se implementar em diversas classes de inúmeras formas.
A função ainda permite uma regressão na hierarquia para que reduza ainda mais redudancia da existencia de 2 criações em cada projeto, podendo se tornar uma ferramenta ainda mais versátil.

O padrão de log segue este formato.
além de estar salvo dentro de cada pasta de 'Logs' nos respectivos projetos, com o padrão de: **log_dd_mm_yyyy.log**
por questão de boas práticas de rastrerabilidade, existe um indicador de log em diversas partes do código, para em qualquer circunstancia de melhoria, otimizando o tempo de busca da falha, aumentando a eficiencia para mitigação


```txt
[2025-09-09 10:04:00] [INFO] [SeleniumUtils] - Localidade selecionada com sucesso
[2025-09-09 10:12:52] [ERROR] [SeleniumUtils] - Timeout: elemento '//h6[.="Cidades"]/..//span[text()="aaaaa - SP"]' não ficou visível em 15s.
[2025-09-09 03:01:29] [WARNING] [SeleniumUtils] - Isto é um teste
```

---
#Estrutura sugerida
```txt
ProjetoBit/                       # Pasta principal
│
├── README.md                     # Documentação principal do projeto
│
├── API/                          # Backend da API de consulta
│   │
│   ├── API_Main.py               # Arquivo principal da API
│   ├── api_requirements.txt      # Dependências específicas da API
│   ├── API_Functions.py          # Funções utilitárias e módulos da API
│   ├── logger_utils.py            #Modulos utilitarios separados
│   │
│   ├── Dados/                    # Saída de dados da API (CSV)
│   │   └── ClimaTempo_Vila Andrade_08_09_2025.csv
│   │
│   └── Logs/                     # Logs da API
│       └── log_09_09_2025.log
│
└── WEB/                          # Interface / automação web
    │
    ├── climatempo_utils.py        # Funções utilitárias para WEB
    ├── main.py                    # Arquivo principal de execução do projeto
    ├── selenium_utils.py          # modulo para manipulação do selenium e configurações do chromedriver
    ├── logger_utils.py            # modulo de log implementado no projeto
    ├── web_requirements.txt       # requisito/dependencias do projeto
    ├── start.bat                  # executor do projeto de forma automática
    │
    ├── Chromedriver.exe          # Driver do Chrome para automação
    │
    ├── Dados/                    # Saída de dados da WEB
    │   └── ClimaTempo_Bauru_SP_09_09_2025.csv
    │
    └── Logs/                     # Logs da WEB
        └── log_09_09_2025.log
```
