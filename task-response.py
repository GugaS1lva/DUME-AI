import requests

# URL do seu servidor Replit
url_replit = "https://d5576599-4028-4958-a439-ccf82356c7d9-00-izf00olxizlu.spock.replit.dev/add-task"

# Dados da tarefa
tarefa = {"titulo": "Dobrar panos"}

# Enviar a requisição para o Replit
response = requests.post(url_replit, json=tarefa)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    print("Tarefa adicionada com sucesso!")
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
