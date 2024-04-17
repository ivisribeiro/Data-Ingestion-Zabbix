Claro, aqui está o texto formatado em Markdown:

---

# Zabbix Data Ingestion API

Este projeto consiste em uma API desenvolvida para realizar a ingestão de dados do ambiente eqtl Info, utilizando a API do Zabbix. O eqtl Info é um sistema de monitoramento e gerenciamento de redes amplamente utilizado, e a API do Zabbix permite interagir com essa plataforma para obter informações sobre grupos de hosts e hosts monitorados.

## Funcionalidades
- Autenticação na API do Zabbix.
- Chamadas à API do Zabbix para obter informações sobre grupos de hosts e hosts monitorados.
- Transformação e consolidação dos dados obtidos.
- Criação de um DataFrame consolidado com as informações relevantes.

## Requisitos
- Python 3.x
- Bibliotecas: requests, json, pandas

## Como usar
1. Clone este repositório:
    ```
    git clone https://github.com/seu_usuario/zabbix-data-ingestion-api.git
    cd zabbix-data-ingestion-api
    ```
2. Instale as dependências:
    ```
    pip install -r requirements.txt
    ```
3. Edite o arquivo `config.py` e insira as informações de acesso à API do Zabbix, como URL, usuário e senha.
4. Execute o arquivo principal `main.py`:
    ```
    python main.py
    ```

## Documentação
A documentação completa deste projeto pode ser encontrada no arquivo `DOCUMENTACAO.md`.

## Contribuição
Contribuições são bem-vindas! Se você tiver alguma sugestão, correção de bugs ou melhorias no código, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença
Este projeto está licenciado sob a licença MIT.

--- 
