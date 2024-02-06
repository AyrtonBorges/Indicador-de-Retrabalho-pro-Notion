import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

def query_notion_database(database_id, token):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16"  # use a versão mais recente da API do Notion
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text

def retrieve_notion_page(page_id, token):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16"  # use a versão mais recente da API do Notion
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text

# Substitua com o seu token de acesso e o ID do banco de dados
notion_token = "secret_f0figqQTNo2yaqPjUlrcG1bM1RPbQfaFg5DSwkNqHtn"
database_id = "7f96c1e68f254bdaa0a00ec8e4c19768"
page_id = "e3dc357c034a48c7a2dab77d27bf7be9"

# Chamar a função e imprimir os resultados
result = query_notion_database(database_id, notion_token)['results']
calculoPorcentagem = []
nomes = []
posicao = []
for i in range(0,len(result)):
  HorasTotaisTemp = result[i]['properties']['Total Horas'].get('number')
  HorasRetrabalho = result[i]['properties']['Horas de Retrabalho'].get('number')
  nomes.append(result[i]['properties']['Reunión']['title'][0]['text']['content'])
  posicao.append(result[i]['properties']['ID'].get('number'))
  if(HorasTotaisTemp != None and HorasRetrabalho != None):
    #HorasTotais = HorasTotaisTemp-HorasRetrabalho
    if(HorasRetrabalho > 0 and HorasTotaisTemp > 0):
      Porcentagem = int((HorasRetrabalho/HorasTotaisTemp)*100)
    elif(HorasTotaisTemp == 0):
      Porcentagem = HorasRetrabalho*4
    else:
      Porcentagem = 0
    calculoPorcentagem.append(Porcentagem)
  else:
    calculoPorcentagem.append(0)

df = pd.DataFrame({'nomes':nomes, 'porcentagem': calculoPorcentagem, 'Posição': posicao})
df = df.sort_values('Posição')
plt.figure(figsize=(10,5))
plt.fill_between(df['nomes'],df['porcentagem'], color="skyblue", alpha=0.4)
plt.plot(df['nomes'], df['porcentagem'], color="Slateblue", alpha=0.6, linewidth=2)

data = {'Limite porcentagem de Retrabalho': ["100,00%"] * 9}
data['Limite porcentagem de Retrabalho'] = [float(value.replace(',', '.').rstrip('%')) for value in data['Limite porcentagem de Retrabalho']]
plt.axhline(y=data['Limite porcentagem de Retrabalho'][0], color='red', linestyle='-', linewidth=2)

plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter())

plt.xticks(rotation=45, ha='right')

plt.title('Porcentagem de Retrabalho por Reuniões')
plt.xlabel('Reuniões')
plt.ylabel('Porcentagem de Retrabalho')

plt.tight_layout()

plt.show()
