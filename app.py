"""Streamlit demo for Sahara-powered, human-confirmed public-service form completion."""
from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from sautiform.asr.factory import build_backend
from sautiform.dialogue.engine import next_prompt
from sautiform.forms.extraction import extract_form
from sautiform.forms.public_service import PublicServiceForm

st.set_page_config(
    page_title="SautiForm Africa",
    page_icon="🎙️",
    layout="centered",
)
st.title("SautiForm Africa")
st.caption(
    "Code-switching voice assistance for public-service form completion"
)
st.info(
    "This prototype assists form completion. It does not make legal or "
    "administrative decisions and does not submit data to a government system."
)

backend_name = "sahara"
st.markdown("**Speech recognition:** Intron Sahara v2.5 · Swahili–English")
st.caption(
    "The product demo is intentionally fixed to Sahara. Comparison models are "
    "available only through the benchmark scripts."
)

audio = st.audio_input("Record a Kiswahili–English response")

with st.expander("Developer transcript fallback"):
    manual_text = st.text_area(
        "Test the downstream form workflow without calling Sahara",
        placeholder=(
            "Ninaishi Mbozi District, occupation yangu ni farmer, "
            "household ina watu sita, nataka birth certificate."
        ),
    )
    st.caption(
        "This fallback is for software testing only. A competition demo should "
        "use recorded audio so the Sahara API is exercised."
    )

transcript: str | None = None
if st.button("Process response", type="primary"):
    if audio is not None:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
            temp.write(audio.getvalue())
            temp_path = Path(temp.name)
        try:
            with st.spinner("Transcribing with Intron Sahara v2.5..."):
                transcript = build_backend(backend_name).transcribe(temp_path).text
        except Exception as exc:
            st.error(f"Transcription failed: {type(exc).__name__}: {exc}")
        finally:
            temp_path.unlink(missing_ok=True)
    elif manual_text.strip():
        transcript = manual_text.strip()
        st.info(
            "Developer transcript fallback used. No Sahara API request was made."
        )
    else:
        st.warning("Record audio or provide a developer transcript first.")

if transcript:
    st.session_state["transcript"] = transcript
    st.session_state["record"] = extract_form(transcript).to_dict()

if "transcript" in st.session_state:
    st.subheader("Recognised response")
    st.write(st.session_state["transcript"])

    values = st.session_state["record"]
    st.subheader("Structured record")
    district = st.text_input("District", value=values.get("district") or "")
    occupation = st.text_input(
        "Occupation",
        value=values.get("occupation") or "",
    )
    household_raw = st.text_input(
        "Household size",
        value=(
            ""
            if values.get("household_size") is None
            else str(values["household_size"])
        ),
    )
    service_request = st.text_input(
        "Service request",
        value=values.get("service_request") or "",
    )

    try:
        household_size = int(household_raw) if household_raw.strip() else None
    except ValueError:
        household_size = -1

    reviewed = PublicServiceForm(
        district=district.strip() or None,
        occupation=occupation.strip() or None,
        household_size=household_size,
        service_request=service_request.strip() or None,
    )
    st.write(next_prompt(reviewed))

    if not reviewed.missing_fields() and not reviewed.validate():
        confirmed = st.checkbox(
            "I confirm that the read-back record is correct."
        )
        if confirmed:
            st.success(
                "Record confirmed. No external submission is performed "
                "in this prototype."
            )
