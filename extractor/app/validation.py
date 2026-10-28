from app.schemas import ExtractedInvoice


def check_totals(inv: ExtractedInvoice) -> list[str]:
    warnings: list[str] = []

    for i, item in enumerate(inv.items):
        expected = round(item.quantity * item.unit_price_minor)
        if abs(expected - item.amount_minor) > 1:
            warnings.append(f"Line {i + 1}: quantity x unit price != amount")

    items_sum = sum(i.amount_minor for i in inv.items)
    if inv.subtotal_minor is not None and inv.items and items_sum != inv.subtotal_minor:
        warnings.append("Sum of line items != subtotal")

    base = inv.subtotal_minor if inv.subtotal_minor is not None else items_sum
    if inv.total_minor is not None and base + (inv.tax_minor or 0) != inv.total_minor:
        warnings.append("Subtotal + tax != total")

    if inv.total_minor is None:
        warnings.append("Total not found")
    if not inv.items:
        warnings.append("No line items found")
    return warnings