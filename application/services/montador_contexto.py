
from domain.models import Chunk


class MontadorContexto:
    def montar(self, chunks: list[Chunk]) -> str:
        """
        Monta um contexto textual a partir dos chunks recuperados.
        """

        if not chunks:
            return ""

        partes_contexto = []

        for chunk in chunks:
            parte = (
                f"[Documento: {chunk.documento_id} | "
                f"Trecho: {chunk.chunk_id}]\n"
                f"{chunk.texto.strip()}"
            )

            partes_contexto.append(parte)

        return "\n\n".join(partes_contexto)
