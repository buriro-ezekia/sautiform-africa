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


def test_recovers_structure_but_not_content_from_observed_asr_variation():
    form = extract_form(
        "Naishim bozdi district, kupeshini angu ni farmer "
        "householdi inawatu sita nataka basic certificate."
    )

    assert form.district == "Bozdi"
    assert form.occupation == "farmer"
    assert form.household_size == 6
    assert form.service_request == "basic certificate"


def test_bare_district_word_does_not_invent_location():
    form = extract_form(
        "I live when I can't own a district because I am a driver."
    )
    assert form.district is None


def test_optional_article_does_not_become_district():
    form = extract_form("I live in the Mwaza district.")
    assert form.district == "Mwaza"


def test_occupation_stops_before_following_possession_clause():
    form = extract_form(
        "I live in Kenan Down District kazi yangu ni driver "
        "Kaminaya yangu ina watu watano Nataka base certificate"
    )
    assert form.occupation == "driver"


def test_split_swathili_number_and_location_cue_are_recovered():
    form = extract_form(
        "Naishu Morogoro District, kazi yangu ni teacher "
        "household ina watu wa wili. Nataka marriage certificate."
    )
    assert form.district == "Morogoro"
    assert form.occupation == "teacher"
    assert form.household_size == 2
    assert form.service_request == "marriage certificate"


def test_service_cue_spacing_and_licence_spelling_are_canonicalised():
    form = extract_form(
        "Naishi Ilala District, kazi yangu ni biashara, "
        "household ina watu saba, na itaji business license."
    )
    assert form.service_request == "business licence"


def test_service_article_is_removed_without_changing_content():
    form = extract_form("I need a marriage certificate.")
    assert form.service_request == "marriage certificate"


def test_content_level_asr_errors_are_not_silently_corrected():
    form = extract_form(
        "Inaishi Mbosy district, household ina watu sita, "
        "nataka besi certificate."
    )
    assert form.district == "Mbosy"
    assert form.service_request == "besi certificate"
