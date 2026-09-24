import os

from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from database import testar_conexao, criar_conexao
from sentence_transformers import SentenceTransformer


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "chave-super-secreta"
jwt = JWTManager(app)

modelo_embedding = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
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
    print("usuariooooooooooooooooooooooo", usuario)
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
        nome
    )

    texto = ler_documento(caminho)
    chunks = dividir_em_chunks(texto)
    documento_id = processar_documento(
        nome,
        chunks
    )
    return {
        "mensagem": "Documento processado com sucesso!",
        "documento_id": documento_id,
        "quantidade_chunks": len(chunks)
    }


@app.get("/buscar")
@jwt_required()
def buscar():
    pergunta = request.args.get("pergunta")
    if not pergunta:
        return {
            "erro": "Informe uma pergunta."
        }, 400

    resultados = buscar_chunks_semelhantes(pergunta)
    return {
        "pergunta": pergunta,
        "resultados": resultados
    }


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


def dividir_em_chunks(texto, tamanho=50, overlap=10):
    if tamanho <= 0:
        raise ValueError("O tamanho deve ser maior que zero.")

    if overlap < 0:
        raise ValueError("O overlap não pode ser negativo.")

    if overlap >= tamanho:
        raise ValueError(
            "O overlap deve ser menor que o tamanho do chunk."
        )

    passo = tamanho - overlap

    chunks = []
    for idx, chk in enumerate(range(0, len(texto), passo)):
        chunk = texto[chk:chk + tamanho]
        obj = {
            "chunk_id": idx + 1,
            "texto": chunk
        }
        chunks.append(obj)
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


def gerar_embeddings(textos):
    embeddings = modelo_embedding.encode(textos)
    return embeddings.tolist()


def buscar_chunks_semelhantes(pergunta, limite=5):
    embedding = modelo_embedding.encode(pergunta).tolist()
    conexao = criar_conexao()
    try:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    documento_id,
                    chunk_id,
                    texto,
                    embedding <=> %s::vector AS distancia
                FROM chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    embedding,
                    embedding,
                    limite
                )
            )
            return cursor.fetchall()
    finally:
        conexao.close()



if __name__ == "__main__":
    app.run(debug=True)


