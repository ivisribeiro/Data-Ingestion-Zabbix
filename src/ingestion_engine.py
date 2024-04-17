import requests 
import json
import pandas as pd
from datetime import datetime, timedelta


url = ""
user = ""
password = ""

# Função para autenticação na API do Zabbix
def authenticate(url, user, password):
    headers = {'Content-Type': 'application/json'}
    data = {
        'jsonrpc': '2.0',
        'method': 'user.login',
        'params': {
            'user': user,
            'password': password
        },
        'id': 1
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            token = result['result']
            return token
        else:
            print("Falha na autenticação. Código de status: {}".format(response.status_code))
    except requests.exceptions.RequestException as e:
        print("Ocorreu um erro durante a conexão: {}".format(str(e)))

# Autenticar na API do Zabbix
token = authenticate(url, user, password)

def call_api(url, token, method, params=None):
    headers = {'Content-Type': 'application/json'}
    data = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params or {},
        'auth': token,
        'id': 1
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            return result.get('result', None)
        else:
            print("Falha na chamada da API. Código de status: {}".format(response.status_code))
    except requests.exceptions.RequestException as e:
        print("Ocorreu um erro durante a conexão: {}".format(str(e)))

def result_to_dataframe(result):
    # Verifica se há algum resultado
    if result is None:
        return None
    
    # Cria um DataFrame diretamente a partir da lista de dicionários
    df = pd.DataFrame(result, index=None)
    
    return df

def transform_inventory_to_dict(list_hosts):
    transformed_data_list = []
    for item in list_hosts:
        inventory = item.pop('inventory', {})  # Remover o 'inventory' do dicionário principal
        if isinstance(inventory, dict):  # Verificar se 'inventory' é um dicionário
            for key, value in inventory.items():
                item[key] = value  # Adicionar os elementos de 'inventory' ao dicionário principal
        transformed_data_list.append(item)
    return transformed_data_list


method = 'hostgroup.get'
params = {
    'output': ['groupid', 'name', 'hosts'],
    "search": {"name": "META *"},
    "searchWildcardsEnabled": 'true',
    "selectHosts": ['hostid', 'host', 'description'] 

}
# Chamada à API do Zabbix para obter informações dos grupos de hosts
host_groups = call_api(url, token, method, params)

rows = []

for item in host_groups:
    for host in item['hosts']:
        row = {
            'hostgroupid': item['groupid'],
            'name': item['name'],
            'hostid': host['hostid'],
            'host': host['host'],
            'description': host['description']
        }
        rows.append(row)
df_hostgroup = pd.DataFrame(rows)


method = 'hostgroup.get'
params = {
    'output': ['groupid', 'name', 'hosts'],
    "search": {"name": "META *"},
    "searchWildcardsEnabled": 'true',
    "selectHosts": ['hostid', 'host', 'description'] 

}

# Chamada à API do Zabbix para obter informações dos grupos de hosts
lista_dicts = call_api(url, token, method, params)
lista_host_group_id = list(map(lambda x: int(x['groupid']), lista_dicts))


method = 'host.get'
params = {
    "monitored_hosts": 'true',
    'groupids': lista_host_group_id,
    'output': ['hostid'],
    'selectInventory': ['os', 'type', 'location', "contact"],
}
list_hosts = call_api(url, token, method, params)
list_hosts_id = [item['hostid'] for item in list_hosts]
df_hosts = pd.DataFrame(transform_inventory_to_dict(list_hosts))



columns_to_keep = ['name', 'host', 'description', 'location', 'contact', 'os', 'type','hostid']


# Realizar o join

df_merged = pd.merge(df_hostgroup, df_hosts, on='hostid', how='inner')[columns_to_keep]
