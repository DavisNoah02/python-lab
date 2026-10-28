from datetime import date
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str
    quantity: float = Field(default=1, gt=0)   # float: receipts have 0.5 kg, 1.5 hrs
    unit_price_minor: int = Field(ge=0)        # integer minor units, never float money
    amount_minor: int = Field(ge=0)


class ExtractedInvoice(BaseModel):
    vendor_name: str | None = None
    invoice_number: str | None = None
    issue_date: date | None = None
    due_date: date | None = None
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    items: list[LineItem] = []
    subtotal_minor: int | None = None
    tax_minor: int | None = None
    total_minor: int | None = None


class ExtractionResult(BaseModel):
    data: ExtractedInvoice
    warnings: list[str]
    needs_review: bool