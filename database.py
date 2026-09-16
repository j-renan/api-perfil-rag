import psycopg2



def criar_conexao():
    try:
        return psycopg2.connect(
            host="localhost",
            database="rag_perfil",
            user="postgres",
            password="1234",
            port=5432
        )
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {str(e)}")
        return None


def testar_conexao():
    conexao = None
    try:
        conexao = criar_conexao()
        return f"Status de conexão do banco de dados: {str(conexao)}"
    except Exception as erro:
        return f"Erro ao testar conexão com o banco de dados: {erro}"
    finally:
        if conexao:
            conexao.close()

    # if type(conexao) == str:
    #     print('Erro ao conectar ao banco de dados')
    #     return conexao
    # conexao.close()
    # return "Conectado com sucesso!"
