from flask import Flask, request, jsonify
from model.user import SistemaLogin

app = Flask(__name__)
sistema = SistemaLogin()

@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    dados = request.json
    nome = dados.get("nome")
    senha = dados.get("senha")
    cargo = dados.get("cargo")
    resultado = sistema.cadastrar_usuario(nome, senha, cargo)
    return jsonify(resultado)

@app.route('/atualizar/<int:user_id>', methods=['PUT'])
def atualizar_usuario(user_id):
    dados = request.json
    nome = dados.get("nome")
    senha = dados.get("senha")
    cargo = dados.get("cargo")
    resultado = sistema.atualizar_usuario(user_id, nome, senha, cargo)
    return jsonify(resultado)

@app.route('/deletar/<int:user_id>', methods=['DELETE'])
def deletar_usuario(user_id):
    resultado = sistema.deletar_usuario(user_id)
    return jsonify(resultado)

@app.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    dados = request.json
    nome = dados.get("nome")
    senha = dados.get("senha")
    resultado = sistema.autenticar(nome, senha)
    return jsonify(resultado)

@app.route('/id', methods=['GET'])
def obter_id():
    dados = request.json
    nome = dados.get("nome")
    resultado = sistema.obter_id(nome)
    return jsonify(resultado)

@app.route('/nome/<int:user_id>', methods=['GET'])
def obter_nome(user_id):
    resultado = sistema.obter_nome(user_id)
    return jsonify(resultado)

@app.route('/cargo/<int:user_id>', methods=['GET'])
def obter_cargo(user_id):
    resultado = sistema.obter_cargo(user_id)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
