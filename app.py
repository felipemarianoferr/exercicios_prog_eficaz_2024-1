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

if __name__ == '__main__':
    app.run(debug=True)