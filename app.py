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

    try:
        cur = conn.cursor()
        dic_cliente = request.json
        nome = dic_cliente.get("nome", '')
        email = dic_cliente.get("email", None) #obrigatorio
        cpf = dic_cliente.get("cpf", None) #obrigatorio
        senha = dic_cliente.get("senha",'')

        if not email or not cpf:
            return {"mensagem": "email e cpf sao colunas obrigatorias."},400
        
        cur.execute("SELECT * FROM clientes WHERE cpf = %s", (cpf,))
        cliente_existente = cur.fetchone()
        if cliente_existente:
            return {"mensagem": "Cliente já existe."}, 400

        cur.execute("INSERT INTO clientes (nome, email, cpf, senha) VALUES(%s, %s,%s,%s)",
                    (nome, email, cpf, senha))
        conn.commit()
        
        resp = {"mensagem": "Cliente cadastrado", "cliente":dic_cliente}

        return resp, 201
    except Exception as e:
        conn.rollback()
        return{"mensagem":str(e)}, 500
    finally:
        cur.close()

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
        return {"mensagem":str(e)}, 500

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
    
    return atualizado, 200

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

#Entidade produto
        
@app.route('/produtos', methods=['GET'])
def lista_produtos():
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM produtos")
        produtos = cur.fetchall()
    except psycopg2.Error() as e:
        cur.rollback()
        return {"mensagem":str(e)}, 500
    finally:
        cur.close()
    
    lista_produtos = []

    for produto in produtos:
        lista_produtos.append(
            {
                "id":produto[0],
                "nome":produto[1],
                "descricao":produto[2],
                "preco":produto[3],
                "estoque":produto[4]
            }
        )

    return lista_produtos, 200

@app.route('/produtos', methods=['POST'])
def registra_produto():
    try:
        cur = conn.cursor()
        dic_produto = request.json
        nome = dic_produto.get("nome",None)
        descricao = dic_produto.get("descricao",'')
        preco = dic_produto.get("preco", None)
        estoque = dic_produto.get("estoque", None)

        if not nome or not preco or not estoque:
            return {"mensagem":"campos obrigatorios!"}, 400
        
        cur.execute('SELECT * FROM produtos WHERE nome = %s', (nome,))
        produto = cur.fetchone()
        if produto:
            return {"mensagem":"Produto ja existe"}, 400
        
        cur.execute("INSERT INTO produtos (nome, descricao, preco, estoque) VALUES(%s, %s, %s, %s)",
                    (nome, descricao, preco, estoque))
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem":str(e)}, 500
    finally:
        cur.close()
    
    resp = {"produto cadastrado": dic_produto}
    return resp, 201

@app.route('/produtos/<int:id>', methods=['GET'])
def consulta_produto(id):
    cur =  conn.cursor()

    try:
        cur.execute("SELECT * FROM produtos WHERE id =%s",(id,))
        produto = cur.fetchone()
        if produto is None:
            return {"mensagem":"produto nao encontrado"}, 404
        
    except psycopg2.Error as e:
        cur.rollback()
        return {"mensagem": str(e)}, 500
    
    finally:
        cur.close()
    
    dic_produto = {
        "id":produto[0],
        "nome":produto[1],
        "descricao":produto[2],
        "preco":produto[3],
        "estoque":produto[4]
    }

    return dic_produto, 200

@app.route('/produtos/<int:id>', methods=['PUT'])
def atualiza_produto(id):
    dic_produto = request.json
    cur = conn.cursor()
    atualizado = {"colunas atualizadas": []}

    try:
        cur.execute("SELECT * FROM produtos WHERE id = %s",(id,))
        produto = cur.fetchone()
        if produto is None:
            return {"mensagem":"produto nao encontrado, nada foi alterado"}, 404
        
        for coluna in dic_produto:
                if coluna != 'id':
                    cur.execute(f'UPDATE produtos SET {coluna} = %s WHERE id = %s',(dic_produto[coluna],id))
                    atualizado["colunas atualizadas"].append(coluna)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem":str(e)}, 500
    
    finally:
        cur.close()
    
    return atualizado, 200

@app.route('/produtos/<int:id>', methods=['DELETE'])
def deleta_produto(id):
    
    cur = conn.cursor()

    try:
        cur.execute("SELECT nome FROM produtos WHERE id = %s",(id,))
        nome_Produto = cur.fetchone()

        if nome_Produto is None:
            return {"mensagem":"prdotuo nao encontrado, nada foi deletado"}, 404
        else:
            cur.execute("DELETE from produtos WHERE id = %s",(id,))
            conn.commit()
            return {"mensagem":f"o produto {nome_Produto} foi deletado"}, 200
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem":str(e)}, 500
    finally:
        cur.close()

#Entidade fornecedores

@app.route('/fornecedores', methods=['GET'])
def lista_fornecedores():
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM fornecedores")
        fornecedores = cur.fetchall()
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem":str(e)}, 500
    finally:
        cur.close()
    
    lista_fornecedores = []
    for fornecedor in fornecedores:
        lista_fornecedores.append(
            {
                "id": fornecedor[0],
                "nome": fornecedor[1],
                "email": fornecedor[2],
                "cnpj": fornecedor[3]
            }
        )

    return lista_fornecedores, 200

@app.route('/fornecedores',methods=["POST"])
def registra_fornecedor():
    dic_fornecedor = request.json
    nome = dic_fornecedor.get("nome", '')
    email = dic_fornecedor.get("email", None)
    cnpj = dic_fornecedor.get("cnpj", None)

    if not email or not cnpj:
        return {"mensagem":"email e cnpj sao obrigatorios"}, 400
    
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO fornecedores (nome, email, cnpj) VALUES(%s, %s, %s)",
                    (nome, email, cnpj))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    finally:
        cur.close()

    resp = {"fornecedor cadastrado":dic_fornecedor}

    return resp, 201

@app.route('/fornecedores/<int:id>', methods=["GET"])
def consulta_fornecdor(id):
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM fornecedores WHERE id = %s", (id,))
        fornecedor = cur.fetchone()
        if fornecedor is None:
            return {"mensagem": "fornecedor nao encontrado"}, 404
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    finally:
        cur.close()

    dic_fornecedor = {
        "id":fornecedor[0],
        "nome":fornecedor[1],
        "email":fornecedor[2],
        "cnpj":fornecedor[3]
    }
    return dic_fornecedor, 200

@app.route('/fornecedores/<int:id>', methods=["PUT"])
def atualiza_fornecedor(id):
    dic_fornecedores = request.json
    cur = conn.cursor()
    atualizado = {"colunas atualizadas": []}

    try:
        cur.execute("SELECT * FROM fornecedores WHERE id = %s", (id,))
        fornecedor = cur.fetchone()

        if fornecedor is None:
            return {"mensagem": "fornecedor nao encontrado, nada foi alterado"}, 404
        
        for coluna in dic_fornecedores:
            if coluna != 'id':
                cur.execute(f'UPDATE fornecedores SET {coluna} = %s WHERE id = %s',(dic_fornecedores[coluna], id))
                atualizado['colunas atualizadas'].append(coluna)
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    
    finally:
        cur.close()
    
    return atualizado, 200

@app.route('/fornecedores/<int:id>', methods=['DELETE'])
def deleta_fornecedores(id):
    cur = conn.cursor()

    try:
        cur.execute("SELECT nome FROM fornecedores WHERE id = %s", (id,))
        nome_fornecedor = cur.fetchone()

        if nome_fornecedor is None:
            return {"mensagem": "fornecedor nao foi encontrado, nada foi deletado"}, 404
        else:
            cur.execute("DELETE FROM fornecedores WHERE id = %s", (id,))
            conn.commit()
            return {"mensagem":f"o cliente {nome_fornecedor[0]} foi deletado"}, 200
        
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    
    finally:
        cur.close()

#Entidade carrinho
        
@app.route('/carrinho',methods=["POST"])
def adiciona_carrinho():
    carrinho = request.json
    cliente_id = carrinho.get('cliente_id',None)
    produto_id = carrinho.get('produto_id', None)
    quantidade = carrinho.get('quantidade', None)

    if not cliente_id or not produto_id or not quantidade:
        return {"mensagem":"Todos os campos sao obrigatorios."}, 400
    cur = conn.cursor()
    try:
        cur.execute("INSERT into carrinho (cliente_id, produto_id, quantidade) VALUES(%s,%s,%s)",
                    (cliente_id, produto_id, quantidade))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return{"mensagem": str(e)}, 500
    finally:
        cur.close()

    resp = {"carrinho cadastrado":carrinho}
    return resp, 201

@app.route('/carrinho', methods=['GET'])
def lista_carrinhos():
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM carrinho")
        carrinhos = cur.fetchall()
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem":str(e)}, 500
    finally:
        cur.close()
    
    lista_carrinho = []
    for carrinho in carrinhos:
        lista_carrinho.append(
            {
                "id": carrinho[0],
                "cliente_id": carrinho[1],
                "produto_id": carrinho[2],
                "quantidade": carrinho[3]
            }
        )

    return lista_carrinho, 200

@app.route('/carrinho/<int:id>', methods=["PUT"])
def atualiza_carrinho(id):
    dic_carrinnho = request.json
    cur = conn.cursor()
    atualizado = {"colunas atualizadas": []}

    try:
        cur.execute("SELECT * FROM carrinho WHERE id = %s", (id,))
        carrinho = cur.fetchone()

        if carrinho is None:
            return {"mensagem": "carrinho nao encontrado, nada foi alterado"}, 404
        
        for coluna in dic_carrinnho:
            if coluna != 'id':
                cur.execute(f'UPDATE carrinho SET {coluna} = %s WHERE id = %s',(dic_carrinnho[coluna], id))
                atualizado['colunas atualizadas'].append(coluna)
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    
    finally:
        cur.close()
    
    return atualizado, 200

@app.route('/carrinho/<int:id>', methods=['DELETE'])
def deleta_carrinho(id):
    cur = conn.cursor()

    try:
        cur.execute("SELECT id FROM carrinho WHERE id = %s", (id,))
        id_carrinho = cur.fetchone()

        if id_carrinho is None:
            return {"mensagem": "carrinho nao foi encontrado, nada foi deletado"}, 404
        else:
            cur.execute("DELETE FROM carrinho WHERE id = %s", (id,))
            conn.commit()
            return {"mensagem":f"o carrinho {id_carrinho[0]} foi deletado"}, 200
        
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    
    finally:
        cur.close()

@app.route('/carrinho/<int:id>', methods=["GET"])
def consulta_carrinho(id):
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM carrinho WHERE id = %s", (id,))
        carrinho = cur.fetchone()
        if carrinho is None:
            return {"mensagem": "carrinho nao encontrado"}, 404
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    finally:
        cur.close()

    dic_carrinho = {
        "id": carrinho[0],
        "cliente_id": carrinho[1],
        "produto_id": carrinho[2],
        "quantidade": carrinho[3]
    }

    return dic_carrinho, 200

#Entidade PEDIDO

@app.route('/pedidos',methods=["POST"])
def adiciona_pedido():
    pedido = request.json
    cliente_id = pedido.get('cliente_id',None)
    data_hora = pedido.get('data_hora', '')
    valor_total = pedido.get('valor_total', None)
    status = pedido.get('status', None)

    if not cliente_id or not valor_total or not status:
        return {"mensagem":"Todos os campos sao obrigatorios."}, 400
    cur = conn.cursor()
    try:
        cur.execute("INSERT into pedido (cliente_id, data_hora, valor_total, status) VALUES(%s,%s,%s, %s)",
                    (cliente_id, data_hora, valor_total, status))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return{"mensagem": str(e)}, 500
    finally:
        cur.close()

    resp = {"pedido cadastrado":pedido}
    return resp, 201

@app.route('/pedidos', methods=['GET'])
def lista_pedidos():
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM pedido")
        pedidos = cur.fetchall()
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem":str(e)}, 500
    finally:
        cur.close()
    
    lista_pedidos = []
    for pedido in pedidos:
        lista_pedidos.append(
            {
                "id": pedido[0],
                "cliente_id": pedido[1],
                "data_hora": pedido[2],
                "valor_total": pedido[3],
                "status": pedido[4]
            }
        )

    return lista_pedidos, 200

@app.route('/pedidos/<int:id>', methods=["GET"])
def consulta_pedido(id):
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM pedido WHERE id = %s", (id,))
        pedido = cur.fetchone()
        if pedido is None:
            return {"mensagem": "pedido nao encontrado"}, 404
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    finally:
        cur.close()

    dic_pedido = {
        "id": pedido[0],
        "cliente_id": pedido[1],
        "data_hora": pedido[2],
        "valor_total": pedido[3],
        "status": pedido[4]
    }

    return dic_pedido, 200

@app.route('/pedidos/<int:id>', methods=["PUT"])
def atualiza_pedidos(id):
    dic_pedido = request.json
    cur = conn.cursor()
    atualizado = {"colunas atualizadas": []}

    try:
        cur.execute("SELECT * FROM pedido WHERE id = %s", (id,))
        pedido = cur.fetchone()

        if pedido is None:
            return {"mensagem": "pedido nao encontrado, nada foi alterado"}, 404
        
        for coluna in dic_pedido:
            if coluna != 'id':
                cur.execute(f'UPDATE pedido SET {coluna} = %s WHERE id = %s',(dic_pedido[coluna], id))
                atualizado['colunas atualizadas'].append(coluna)
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    
    finally:
        cur.close()
    
    return atualizado, 200

@app.route('/pedidos/<int:id>', methods=['DELETE'])
def deleta_pedido(id):
    cur = conn.cursor()

    try:
        cur.execute("SELECT id FROM pedido WHERE id = %s", (id,))
        id_pedido = cur.fetchone()

        if id_pedido is None:
            return {"mensagem": "pedido nao foi encontrado, nada foi deletado"}, 404
        else:
            cur.execute("DELETE FROM pedido WHERE id = %s", (id,))
            conn.commit()
            return {"mensagem":f"o pedido {id_pedido[0]} foi deletado"}, 200
        
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem": str(e)}, 500
    
    finally:
        cur.close()

#entidade Estoque Fornecedor

@app.route('/estoque_fornecedor',methods=["POST"])
def adiciona_estoque():
    estoque = request.json
    produto_id = estoque.get('produto_id',None)
    fornecedor_id = estoque.get('fornecedor_id',None)
    quantidade = estoque.get('quantidade', None)
    preco_custo = estoque.get('preco_custo', None)

    if not produto_id or not fornecedor_id or not quantidade or not preco_custo:
        return {"mensagem":"Todos os campos sao obrigatorios."}, 400
    cur = conn.cursor()
    try:
        cur.execute("INSERT into estoque_fornecedor (produto_id, fornecedor_id, quantidade, preco_custo) VALUES(%s,%s,%s, %s)",
                    (produto_id, fornecedor_id, quantidade, preco_custo))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return{"mensagem": str(e)}, 500
    finally:
        cur.close()

    resp = {"estoque cadastrado":estoque}
    return resp, 201

@app.route('/estoque_fornecedor', methods=['GET'])
def lista_estoques():
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM estoque_fornecedor")
        estoques = cur.fetchall()
    except psycopg2.Error as e:
        conn.rollback()
        return {"mensagem":str(e)}, 500
    finally:
        cur.close()
    
    lista_estoques = []
    for estoque in estoques:
        lista_estoques.append(
            {
                "produto_id": estoque[0],
                "fornecedor_id": estoque[1],
                "quantidade": estoque[2],
                "preco_custo": estoque[3]
            }
        )

    return lista_estoques, 200

if __name__ == '__main__':
    app.run(debug=True)