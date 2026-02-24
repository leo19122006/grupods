from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)

DATA_FILE = "data.json"

# ---------- Persistência ----------
def carregar_solicitacoes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def salvar_solicitacoes():
    with open(DATA_FILE, "w") as f:
        json.dump(solicitacoes, f, indent=4)

solicitacoes = carregar_solicitacoes()

# ---------- Rotas ----------

@app.route("/")
def home():
    return render_template("index.html", solicitacoes=solicitacoes)

@app.route("/solicitacoes", methods=["POST"])
def criar_solicitacao():
    data = request.json
    
    if not data or not data.get("titulo") or not data.get("descricao"):
        return jsonify({"erro": "Campos obrigatórios não preenchidos"}), 400
    
    nova = {
        "id": len(solicitacoes) + 1,
        "titulo": data["titulo"],
        "descricao": data["descricao"],
        "status": "registrada"
    }

    solicitacoes.append(nova)
    salvar_solicitacoes()
    return jsonify(nova), 201

@app.route("/solicitacoes", methods=["GET"])
def listar_solicitacoes():
    return jsonify(solicitacoes)

@app.route("/solicitacoes/<int:id>", methods=["GET"])
def obter_solicitacao(id):
    for s in solicitacoes:
        if s["id"] == id:
            return jsonify(s)
    return jsonify({"erro": "Solicitação não encontrada"}), 404

@app.route("/solicitacoes/<int:id>/status", methods=["PATCH"])
def atualizar_status(id):
    data = request.json
    
    for s in solicitacoes:
        if s["id"] == id:
            s["status"] = data.get("status", s["status"])
            salvar_solicitacoes()
            return jsonify(s)

    return jsonify({"erro": "Solicitação não encontrada"}), 404

@app.route("/solicitacoes/<int:id>", methods=["DELETE"])
def deletar_solicitacao(id):
    global solicitacoes
    solicitacoes = [s for s in solicitacoes if s["id"] != id]
    salvar_solicitacoes()
    return jsonify({"mensagem": "Solicitação removida"}), 200


# ---------- Execução ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
