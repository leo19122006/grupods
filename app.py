from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
solicitacoes = []

@app.route("/")
def home():
    return render_template("index.html", solicitacoes=solicitacoes)

@app.route("/solicitacoes", methods=["POST"])
def criar_solicitacao():
    data = request.json
    if not data.get("titulo") or not data.get("descricao"):
        return jsonify({"erro": "Campos obrigatórios não preenchidos"}), 400
    
    nova = {
        "id": len(solicitacoes) + 1,
        "titulo": data["titulo"],
        "descricao": data["descricao"],
        "status": "registrada"
    }
    solicitacoes.append(nova)
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
            return jsonify(s)
    return jsonify({"erro": "Solicitação não encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)