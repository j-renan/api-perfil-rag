from app import app

print("Aplicação Flask importada com sucesso!")

print("Rotas registradas:")

for regra in app.url_map.iter_rules():
    print(regra)