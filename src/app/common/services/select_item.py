from typing import Any


def to_select_item(value: Any, label: str | None = None) -> dict[str, Any]:
    """Port SelectItemTrait — { value, label }."""
    return {"value": value, "label": label if label is not None else str(value)}


def to_select_items(pairs: list[tuple[Any, str]]) -> list[dict[str, Any]]:
    return [to_select_item(v, label) for v, label in pairs]
