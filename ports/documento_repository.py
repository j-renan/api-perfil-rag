from typing import Protocol


class DocumentoRepository(Protocol):

    def salvar(self, nome: str) -> int:
        ...

    def existe(self, nome: str) -> bool:
        ...