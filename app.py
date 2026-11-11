import os

from flask import Flask, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from domain.models import Documento

from application.use_cases.processar_documento import (
    ProcessarDocumento,
)
from database import criar_conexao, testar_conexao
from application.use_cases.buscar_chunks_semelhantes import (
    BuscarChunksSemelhantes,
)
from infrastructure.database.postgres_connection_factory import (
    PostgresConnectionFactory,
)
from infrastructure.embeddings.sentence_transformer_service import (
    SentenceTransformerEmbeddingService,
)
from infrastructure.database.postgres_unit_of_work import (
    PostgresUnitOfWork,
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "chave-super-secreta"
jwt = JWTManager(app)

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

connection_factory = PostgresConnectionFactory()

embedding_service = SentenceTransformerEmbeddingService(
    model_name=MODEL_NAME
)


def criar_unit_of_work() -> PostgresUnitOfWork:
    return PostgresUnitOfWork(
        connection_factory=connection_factory
    )


@app.get("/")
def home():
    return {
        "mensagem": "API RAG funcionando!"
    }

@app.get("/test_db")
def test_db():
    teste = testar_conexao()
    return {"mensagem": teste}


@app.post("/login")
def login():

    dados = request.get_json()

    email = dados["email"]
    senha = dados["senha"]

    conexao = criar_conexao()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT id, nome, email, senha
        FROM usuarios
        WHERE email = %s
        """,
        (email,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not usuario:
        return {
            "erro": "E-mail ou senha inválidos"
        }, 401

    senha_valida = check_password_hash(
        usuario["senha"],
        senha
    )

    if not senha_valida:
        return {
            "erro": "E-mail ou senha inválidos"
        }, 401

    token = create_access_token(
        identity=str(usuario["id"])
    )

    return {
        "access_token": token
    }


@app.get("/usuarios")
@jwt_required()
def listar_usuarios():
    conexao = criar_conexao()
    cursor = conexao.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "SELECT id, nome, email FROM usuarios"
    )
    usuarios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return usuarios


@app.post("/usuarios")
# @jwt_required()
def criar_usuario():
    dados = request.get_json()
    nome = dados["nome"]
    email = dados["email"]
    senha = dados["senha"]

    senha_hash = generate_password_hash(senha)
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO usuarios (nome, email, senha)
        VALUES (%s, %s, %s)
        """,
        (nome, email, senha_hash)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    return {
        "mensagem": "Usuário criado com sucesso!"
    }, 201


@app.get("/me")
@jwt_required()
def perfil():
    id_usuario = get_jwt_identity()
    conexao = criar_conexao()
    cursor = conexao.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "SELECT nome, email FROM usuarios WHERE id = %s", (id_usuario,)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()
    return {
        "id": id_usuario,
        "nome": usuario.get("nome"),
        "email": usuario.get("email"),
    }


@app.get("/api")
def api():
    return {
        "nome": "api-perfil-rag",
        "status": "online",
        "versao": "1.0",
        "Criador": "João Renan Celso"
    }


DIRETORIO_DOCUMENTOS = "documentos"

@app.get("/documento")
@jwt_required()
def documento():
    texto = ler_documento(
        os.path.join(DIRETORIO_DOCUMENTOS, "flask.txt")
    )

    return {
        "documento": texto
    }


@app.get("/documentos")
@jwt_required()
def buscar_documentos():
    documentos = listar_documentos(DIRETORIO_DOCUMENTOS)

    return {
        "documentos": documentos
    }


@app.get("/documentos/completos")
@jwt_required()
def buscar_documentos_completos():
    documentos = carregar_documentos(DIRETORIO_DOCUMENTOS)
    return documentos



@app.post("/processar-documento")
@jwt_required()
def processar_documento_rota():

    nome = "flask.txt"

    caminho = os.path.join(
        DIRETORIO_DOCUMENTOS,
        nome,
    )

    try:
        # 1. Ler o conteúdo do arquivo
        texto = ler_documento(caminho)

        # 2. Dividir o conteúdo em chunks
        chunks = dividir_em_chunks(texto)

        # 3. Criar o objeto de domínio Documento
        documento = Documento(
            nome=nome,
            conteudo=texto,
        )

        # 4. Criar o caso de uso
        processar_documento_use_case = ProcessarDocumento(
            unit_of_work=criar_unit_of_work(),
            embedding_service=embedding_service,
        )

        # 5. Executar o processamento
        documento_id = processar_documento_use_case.executar(
            documento=documento,
            chunks=chunks,
        )

        return {
            "mensagem": "Documento processado com sucesso!",
            "documento_id": documento_id,
            "quantidade_chunks": len(chunks),
        }, 201

    except FileNotFoundError:
        return {
            "erro": f"Arquivo '{nome}' não encontrado."
        }, 404

    except ValueError as erro:
        return {
            "erro": str(erro)
        }, 400




@app.get("/buscar")
@jwt_required()
def buscar():

    pergunta = request.args.get("pergunta")

    if not pergunta:
        return {"erro": "Informe uma pergunta."}, 400

    try:
        unit_of_work = criar_unit_of_work()

        buscar_chunks_use_case = BuscarChunksSemelhantes(
            unit_of_work=unit_of_work,
            embedding_service=embedding_service,
        )

        resultados = buscar_chunks_use_case.executar(
            pergunta=pergunta
        )

        return {
            "pergunta": pergunta,
            "resultados": [
                {
                    "id": resultado.id,
                    "documento_id": resultado.documento_id,
                    "chunk_id": resultado.chunk_id,
                    "texto": resultado.texto,
                }
                for resultado in resultados
            ],
        }

    except ValueError as erro:
        return {"erro": str(erro)}, 400


def ler_documento(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def listar_documentos(caminho):
    arquivos = os.listdir(caminho)
    documentos = []

    for arquivo in arquivos:
        if arquivo.endswith(".txt"):
            documentos.append(arquivo)

    return documentos


def carregar_documentos(caminho):
    arquivos = listar_documentos(caminho)
    resultado = []

    for arquivo in arquivos:
        caminho_arquivo = os.path.join(caminho, arquivo)
        conteudo = ler_documento(caminho_arquivo)
        chunks = dividir_em_chunks(conteudo)

        documento = {
            "nome": arquivo,
            "chunks": chunks
        }

        resultado.append(documento)

    return resultado



def dividir_em_chunks(
    texto: str,
    tamanho: int = 500,
    overlap: int = 100,
) -> list[dict[str, int | str]]:

    if tamanho <= 0:
        raise ValueError("O tamanho deve ser maior que zero.")

    if overlap < 0:
        raise ValueError("O overlap não pode ser negativo.")

    if overlap >= tamanho:
        raise ValueError(
            "O overlap deve ser menor que o tamanho do chunk."
        )

    texto = texto.strip()

    if not texto:
        raise ValueError("O texto não pode estar vazio.")

    chunks = []
    inicio = 0

    while inicio < len(texto):

        limite = min(inicio + tamanho, len(texto))
        fim = limite

        if limite < len(texto):

            # Procura primeiro limites de parágrafos,
            # depois frases e, por último, palavras.
            janela_inicio = inicio + int(tamanho * 0.7)

            separadores = [
                "\n\n",
                "\n",
                ". ",
                "! ",
                "? ",
                " ",
            ]

            for separador in separadores:
                posicao = texto.rfind(
                    separador,
                    janela_inicio,
                    limite,
                )

                if posicao != -1:
                    fim = posicao + len(separador)
                    break

            else:
                # Caso não encontre um separador,
                # utiliza o limite máximo de caracteres.
                posicao = texto.rfind(" ", inicio, limite)

                if posicao > inicio:
                    fim = posicao + 1

        conteudo = texto[inicio:fim].strip()

        if conteudo:
            chunks.append({
                "chunk_id": len(chunks) + 1,
                "texto": conteudo,
            })

        if fim >= len(texto):
            break

        # Calcula o início do próximo chunk,
        # preservando parte do conteúdo anterior.
        proximo_inicio = max(inicio + 1, fim - overlap)

        # Evita começar o próximo chunk no meio de uma palavra.
        while (
            proximo_inicio < fim
            and not texto[proximo_inicio].isspace()
        ):
            proximo_inicio += 1

        # Ignora espaços antes da próxima palavra.
        while (
            proximo_inicio < fim
            and texto[proximo_inicio].isspace()
        ):
            proximo_inicio += 1

        if proximo_inicio <= inicio:
            proximo_inicio = fim

        inicio = proximo_inicio

    return chunks



def salvar_documento(nome):
    conexao = criar_conexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documentos (nome)
                VALUES (%s)
                RETURNING id
                """,
                (nome,)
            )
            documento_id = cursor.fetchone()[0]
            conexao.commit()
            return documento_id
    finally:
        conexao.close()


def salvar_chunk(documento_id, chunk_id, texto, embedding):
    conexao = criar_conexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO chunks (
                    documento_id,
                    chunk_id,
                    texto,
                    embedding
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    documento_id,
                    chunk_id,
                    texto,
                    embedding
                )
            )
            conexao.commit()
    finally:
        conexao.close()


def processar_documento(nome, chunks):
    documento_id = salvar_documento(nome)
    textos = [
        chunk["texto"]
        for chunk in chunks
    ]
    embeddings = gerar_embeddings(textos)

    for chunk, embedding in zip(chunks, embeddings):
        salvar_chunk(
            documento_id=documento_id,
            chunk_id=chunk["chunk_id"],
            texto=chunk["texto"],
            embedding=embedding
        )
    return documento_id


def gerar_embeddings(textos: list[str]) -> list[list[float]]:
    return embedding_service.gerar_embeddings(textos)


if __name__ == "__main__":
    app.run(debug=True)
