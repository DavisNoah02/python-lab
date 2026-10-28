from typing import Protocol
from app.schemas import ExtractedInvoice


class Extractor(Protocol):
    async def extract(self, content: bytes, content_type: str) -> ExtractedInvoice: ...