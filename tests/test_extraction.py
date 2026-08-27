"""Tests for code-switched field extraction."""
from sautiform.forms.extraction import extract_form


def test_extracts_complete_code_switched_form():
    form = extract_form(
        "Ninaishi Mbozi District, occupation yangu ni farmer, "
        "household ina watu sita, nataka birth certificate."
    )
    assert form.district == "Mbozi"
    assert form.occupation == "farmer"
    assert form.household_size == 6
    assert form.service_request == "birth certificate"
    assert form.missing_fields() == []


def test_missing_fields_are_not_invented():
    form = extract_form("Ninaishi Mbozi District")
    assert form.district == "Mbozi"
    assert set(form.missing_fields()) == {"occupation", "household_size", "service_request"}
