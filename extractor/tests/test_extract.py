from fastapi.testclient import TestClient
from app.main import app, get_extractor
from app.schemas import ExtractedInvoice, LineItem

client = TestClient(app)
PDF = b"%PDF-1.4 fake"


def test_happy_path():
    r = client.post("/extract", files={"file": ("a.pdf", PDF, "application/pdf")})
    assert r.status_code == 200
    assert r.json()["needs_review"] is False


def test_rejects_wrong_type():
    r = client.post("/extract", files={"file": ("a.txt", b"hi", "text/plain")})
    assert r.status_code == 415


def test_rejects_spoofed_content():
    r = client.post("/extract", files={"file": ("a.pdf", b"not a pdf", "application/pdf")})
    assert r.status_code == 400


def test_flags_bad_totals():
    class Bad:
        async def extract(self, content, content_type):
            return ExtractedInvoice(
                items=[LineItem(description="x", quantity=1, unit_price_minor=1000, amount_minor=1000)],
                total_minor=9999,
            )

    app.dependency_overrides[get_extractor] = lambda: Bad()
    r = client.post("/extract", files={"file": ("a.pdf", PDF, "application/pdf")})
    app.dependency_overrides.clear()
    assert r.json()["needs_review"] is True
    