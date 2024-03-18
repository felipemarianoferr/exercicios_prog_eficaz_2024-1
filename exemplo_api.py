import requests 

# r = requests.get("http://viacep.com.br/ws/01001000/json/")

# status_code_resposta = r.status_code
# print (status_code_resposta)
# if status_code_resposta == 200:
#     respsota_json = r.json()
#     print (respsota_json)
#     ddd = respsota_json['ddd']
#     print ("ddd: ", ddd)

# else:
#     print ("CPF inválido")

# cotent = {
#     "nome": "teste",
#     "email": "teste@teste.com",
#     "idade": 27,
#     "cpf": "48"
# }

# r = requests.post('https://deploy-heroku-2024-1-1731d2b34d37.herokuapp.com/cadastra_aluno', json=cotent)
# print(r.json())

# r = requests.get('https://pokeapi.co/api/v2/pokemon/psyduck')
# moves = r.json()['moves']
# movimentos = [move['move']['name'] for move in moves]
# print(movimentos) 

# import json

# # Defina seu token de API da OpenAI

# # URL da API
# url = "https://api.openai.com/v1/chat/completions"

# # Cabeçalhos da solicitação
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {openai_api_key}",
#     "temperature": "1"
# }
# # Dados da solicitação
# data = {
#     "model": "gpt-3.5-turbo",
#     "messages": [
#         {
#             "role": "system",
#             "content":"seja uma princesa barbie patricinha"
#         },
#         {   
#             "role": "user",
#             "content": "qual esporte voce joga?"
#         }
#     ]
# }


# # Enviar solicitação
# response = requests.post(url, headers=headers, data=json.dumps(data))

# # Verificar se a solicitação foi bem-sucedida
# if response.status_code == 200:
#     # Imprimir a resposta
#     #print(response.json())
#     dic_msg = response.json()['choices'][0]['message']['content']
#     print(dic_msg)
# else:
#     print("Erro ao enviar solicitação:", response.text)
