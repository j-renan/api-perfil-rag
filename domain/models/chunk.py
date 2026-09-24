from dataclasses import dataclass


@dataclass
class Chunk:
    documento_id: int
    chunk_id: int
    texto: str
    embedding: list[float] | None = None
    id: int | None = None