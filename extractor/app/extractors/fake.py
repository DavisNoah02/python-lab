from datetime import date
from app.schemas import ExtractedInvoice, LineItem


class FakeExtractor:
    async def extract(self, content: bytes, content_type: str) -> ExtractedInvoice:
        return ExtractedInvoice(
            vendor_name="Acme Ltd",
            invoice_number="INV-001",
            issue_date=date(2026, 10, 1),
            currency="KES",
            items=[LineItem(description="Web design", quantity=2,
                            unit_price_minor=5_000_000, amount_minor=10_000_000)],
            subtotal_minor=10_000_000,
            tax_minor=1_600_000,
            total_minor=11_600_000,
        )