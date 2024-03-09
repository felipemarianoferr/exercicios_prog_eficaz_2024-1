from flask import Flask, request
import psycopg2
import json

app = Flask("Mercado_relacional")

conn = psycopg2.connect(
    dbname="ezubpxza",
    user="ezubpxza",
    password="jLYaQWZ3RG0cUBzvL2wI4FLRv5QDsCiR",
    host="kesavan.db.elephantsql.com"
)

@app.route('/')
def hello_world():
    return "Rodando"

#Entidade cliente

@app.route('/clientes', methods=['GET'])
def lista_clientes():
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM clientes")
        clientes = cur.fetchall()
    except psycopg2.Error as e:
        cur.rollback()
        return {"Mensagem":str(e)}, 500
    finally:
        cur.close()
    
    lista_clientes = []

    for cliente in clientes:
        lista_clientes.append(
            {
                "id":cliente[0],
                "nome":cliente[1],
                "email":cliente[2],
                "cpf":cliente[3],
                "senha":cliente[4]
            }
        )    
    return lista_clientes, 200

@app.route('/clientes', methods=['POST'])
def registra_cliente():

    dic_cliente = request.json
    nome = dic_cliente.get("nome", '')
    email = dic_cliente.get("email", None) #obrigatorio
    cpf = dic_cliente.get("cpf", None) #obrigatorio
    senha = dic_cliente.get("senha",'')

    if not email or not cpf:
        return {"mensagem": "email e cpf sao colunas obrigatorias."},400
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO clientes (nome, email, cpf, senha) VALUES(%s, %s,%s,%s)",
                    (nome, email, cpf, senha))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return{"mensagem":str(e)}, 500
    finally:
        cur.close()
    
    resp = {"mensagem": "Cliente cadastrado", "cliente":dic_cliente}

    return resp, 201

@app.route('/clientes/<int:id>', methods=['GET'])
def consulta_cliente(id):
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM clientes WHERE id = %s", (id,))
        cliente = cur.fetchone()

        if cliente is None:
            return {"mensagem": "cliente nao encontrado"}, 404
    
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem":str(e)}

    finally:
        cur.close()
    
    dict_cliente = {
        'id':cliente[0],
        'nome':cliente[1],
        'email':cliente[2],
        'cpf':cliente[3],
        'senha':cliente[4]
    } 

    return dict_cliente, 200

@app.route('/clientes/<int:id>', methods=['PUT'])
def atualiza_cliente(id):
    
    dic_cliente = request.json
    cur = conn.cursor()
    atualizado = {"colunas atualizadas": []}

    try:
        cur.execute("SELECT * FROM clientes WHERE id = %s", (id,))
        cliente = cur.fetchone()

        if cliente is None:
            return {"mensagem": "cliente nao encontrado, nada foi alterado"}, 404
        
        for coluna in dic_cliente:
            if coluna != 'id':
                cur.execute(f'UPDATE clientes SET {coluna} = %s WHERE id = %s',(dic_cliente[coluna], id))
                atualizado['colunas atualizadas'].append(coluna)
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    
    finally:
        cur.close()
    
    return atualizado

@app.route('/clientes/<int:id>', methods=['DELETE'])
def deleta_cliente(id):
    cur = conn.cursor()

    try:
        cur.execute("SELECT nome FROM clientes WHERE id = %s", (id,))
        nome_cliente = cur.fetchone()

        if nome_cliente is None:
            return {"mensagem": "cliente nao foi encontrado, nada foi deletado"}, 404
        else:
            cur.execute("DELETE FROM clientes WHERE id = %s", (id,))
            conn.commit()
            return {"mensagem":f"o cliente {nome_cliente} foi deletado"}, 200
        
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    
    finally:
        cur.close()

if __name__ == '__main__':
    app.run(debug=True)