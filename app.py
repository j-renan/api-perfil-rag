from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

from database import testar_conexao, criar_conexao

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "chave-super-secreta"
jwt = JWTManager(app)


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
@jwt_required()
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




if __name__ == "__main__":
    app.run(debug=True)