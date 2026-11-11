
import os

from app import (
    DIRETORIO_DOCUMENTOS,
    ler_documento,
    dividir_em_chunks,
)

nome = "flask.txt"

caminho = os.path.join(
    DIRETORIO_DOCUMENTOS,
    nome,
)

texto = ler_documento(caminho)

chunks = dividir_em_chunks(texto)

print(f"Documento: {nome}")
print(f"Caracteres originais: {len(texto)}")
print(f"Quantidade de chunks: {len(chunks)}")
print("-" * 50)

for chunk in chunks:
    print(
        f"Chunk {chunk['chunk_id']} - "
        f"{len(chunk['texto'])} caracteres"
    )

print("-" * 50)
print("Análise dos chunks concluída!")
