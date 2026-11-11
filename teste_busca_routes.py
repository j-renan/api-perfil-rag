from flask import Flask

from application.use_cases.buscar_chunks_semelhantes import (
    BuscarChunksSemelhantes
)

from domain.models import Chunk

from presentation.routes.busca_routes import (
    criar_busca_routes
)


class FakeBuscarChunksSemelhantes:

    def executar(
        self,
        pergunta: str,
        limite: int = 5
    ) -> list[Chunk]:

        print(f"Pergunta recebida: {pergunta}")
        print(f"Limite recebido: {limite}")

        return [
            Chunk(
                id=1,
                documento_id=1,
                chunk_id=1,
                texto="Python é uma linguagem de programação.",
                embedding=None
            )
        ]


app = Flask(__name__)

use_case = FakeBuscarChunksSemelhantes()

app.register_blueprint(
    criar_busca_routes(use_case)
)


client = app.test_client()


resposta = client.post(
    "/api/busca",
    json={
        "pergunta": "Quais tecnologias eu conheço?",
        "limite": 5
    }
)


print(f"Status: {resposta.status_code}")
print(f"Resposta: {resposta.get_json()}")