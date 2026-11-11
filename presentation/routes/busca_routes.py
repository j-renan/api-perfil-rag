from flask import Blueprint, jsonify, request
from application.use_cases.buscar_chunks_semelhantes import (
    BuscarChunksSemelhantes
)


busca_bp = Blueprint(
    "busca",
    __name__,
    url_prefix="/api"
)


def criar_busca_routes(use_case: BuscarChunksSemelhantes) -> Blueprint:
    @busca_bp.post("/busca")
    def buscar():
        dados = request.get_json()
        if not dados:
            return jsonify({
                "erro": "O corpo da requisição é obrigatório."
            }), 400

        pergunta = dados.get("pergunta")
        limite = dados.get("limite", 5)

        if not isinstance(pergunta, str):
            return jsonify({
                "erro": "O campo 'pergunta' é obrigatório."
            }), 400

        try:
            resultados = use_case.executar(
                pergunta=pergunta,
                limite=limite
            )
            return jsonify([
                {
                    "id": resultado.id,
                    "documento_id": resultado.documento_id,
                    "chunk_id": resultado.chunk_id,
                    "texto": resultado.texto
                }
                for resultado in resultados
            ])

        except ValueError as erro:
            return jsonify({
                "erro": str(erro)
            }), 400

    return busca_bp