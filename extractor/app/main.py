from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, UploadFile

from app.extractors.base import Extractor
from app.extractors.fake import FakeExtractor
from app.schemas import ExtractionResult
from app.validation import check_totals

app = FastAPI(title="Invoice Extractor")

MAX_BYTES = 5 * 1024 * 1024
MAGIC = {
    "application/pdf": b"%PDF-",
    "image/png": b"\x89PNG\r\n\x1a\n",
    "image/jpeg": b"\xff\xd8\xff",
}


def get_extractor() -> Extractor:
    return FakeExtractor()


@app.post("/extract", response_model=ExtractionResult)
async def extract(file: UploadFile, extractor: Annotated[Extractor, Depends(get_extractor)]):
    if file.content_type not in MAGIC:
        raise HTTPException(415, "Only PDF, PNG or JPEG are supported")

    content = await file.read(MAX_BYTES + 1)          # read at most cap + 1 byte
    if len(content) > MAX_BYTES:
        raise HTTPException(413, "File exceeds 5 MB")
    if not content.startswith(MAGIC[file.content_type]):
        raise HTTPException(400, "File content does not match its declared type")

    data = await extractor.extract(content, file.content_type)
    warnings = check_totals(data)
    return ExtractionResult(data=data, warnings=warnings, needs_review=bool(warnings))