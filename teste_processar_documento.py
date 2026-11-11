
from domain.models import Chunk, Documento
from application.use_cases.processar_documento import ProcessarDocumento


class FakeDocumentoRepository:
    def __init__(self):
        self.documentos_salvos = []

    def salvar(self, nome: str) -> int:
        self.documentos_salvos.append(nome)
        return 101

    def existe(self, nome: str) -> bool:
        return nome in self.documentos_salvos


class FakeChunkRepository:
    def __init__(self, falhar_no_chunk_id=None):
        self.chunks_salvos = []
        self.falhar_no_chunk_id = falhar_no_chunk_id

    def salvar(self, chunk: Chunk) -> Chunk:
        if chunk.chunk_id == self.falhar_no_chunk_id:
            raise RuntimeError("Falha simulada ao salvar o chunk.")

        chunk.id = len(self.chunks_salvos) + 1
        self.chunks_salvos.append(chunk)
        return chunk


class FakeEmbeddingService:
    def gerar_embeddings(self, textos: list[str]) -> list[list[float]]:
        return [
            [float(indice + 1)] * 384
            for indice, _ in enumerate(textos)
        ]


class FakeUnitOfWork:
    def __init__(self, falhar_no_chunk_id=None):
        self.documento_repository = FakeDocumentoRepository()
        self.chunk_repository = FakeChunkRepository(
            falhar_no_chunk_id=falhar_no_chunk_id
        )

        self.commit_count = 0
        self.rollback_count = 0

    def __enter__(self):
        self.documentos_anteriores = list(
            self.documento_repository.documentos_salvos
        )
        self.chunks_anteriores = list(
            self.chunk_repository.chunks_salvos
        )
        return self

    def __exit__(self, tipo_excecao, excecao, traceback):
        if tipo_excecao is None:
            self.commit()
        else:
            self.rollback()

        return False

    def commit(self):
        self.commit_count += 1

    def rollback(self):
        self.rollback_count += 1

        self.documento_repository.documentos_salvos = (
            self.documentos_anteriores
        )
        self.chunk_repository.chunks_salvos = (
            self.chunks_anteriores
        )


# --------------------------------------------------
# Teste 1: processamento realizado com sucesso
# --------------------------------------------------

unit_of_work = FakeUnitOfWork()

embedding_service = FakeEmbeddingService()

processar_documento = ProcessarDocumento(
    unit_of_work=unit_of_work,
    embedding_service=embedding_service,
)

documento = Documento(
    nome="curriculo-teste-uow.md",
    conteudo="Conteúdo de teste.",
)

chunks = [
    {
        "chunk_id": 1,
        "texto": "Conhecimentos em Python.",
    },
    {
        "chunk_id": 2,
        "texto": "Experiência com Flask.",
    },
]

documento_id = processar_documento.executar(
    documento=documento,
    chunks=chunks,
)

print("TESTE 1: Processamento com sucesso")
print(f"ID do documento: {documento_id}")
print(
    "Documentos salvos:",
    unit_of_work.documento_repository.documentos_salvos,
)
print(
    "Quantidade de chunks:",
    len(unit_of_work.chunk_repository.chunks_salvos),
)
print(f"Commits realizados: {unit_of_work.commit_count}")
print(f"Rollbacks realizados: {unit_of_work.rollback_count}")

assert documento_id == 101
assert len(unit_of_work.chunk_repository.chunks_salvos) == 2
assert unit_of_work.commit_count == 1
assert unit_of_work.rollback_count == 0

print("Resultado: aprovado!\n")


# --------------------------------------------------
# Teste 2: documento duplicado
# --------------------------------------------------

print("TESTE 2: Documento duplicado")

try:
    processar_documento.executar(
        documento=documento,
        chunks=chunks,
    )
except ValueError as erro:
    print(f"Exceção capturada: {erro}")

assert unit_of_work.commit_count == 1
assert unit_of_work.rollback_count == 1
assert len(unit_of_work.documento_repository.documentos_salvos) == 1

print("Rollback realizado após a rejeição do documento duplicado.")
print("Resultado: aprovado!\n")


# --------------------------------------------------
# Teste 3: falha durante o salvamento dos chunks
# --------------------------------------------------

print("TESTE 3: Falha durante o processamento")

unit_of_work_falha = FakeUnitOfWork(
    falhar_no_chunk_id=2
)

processar_documento_falha = ProcessarDocumento(
    unit_of_work=unit_of_work_falha,
    embedding_service=embedding_service,
)

try:
    processar_documento_falha.executar(
        documento=Documento(
            nome="documento-teste-rollback.md",
            conteudo="Conteúdo de teste.",
        ),
        chunks=chunks,
    )
except RuntimeError as erro:
    print(f"Exceção capturada: {erro}")

assert unit_of_work_falha.commit_count == 0
assert unit_of_work_falha.rollback_count == 1
assert len(unit_of_work_falha.documento_repository.documentos_salvos) == 0
assert len(unit_of_work_falha.chunk_repository.chunks_salvos) == 0

print("Documento removido da memória após rollback.")
print("Chunks removidos da memória após rollback.")
print("Resultado: aprovado!\n")


print("Todos os testes do ProcessarDocumento passaram!")
