from pathlib import Path
import streamlit as st
import json

from src.writeup_engine import GDocHandler

local_writeup_path = "local_storage/writeup.md"
local_version_path = "local_storage/version_state.json"


def start_engine(json_key):
    return GDocHandler(json_key=json_key).init_service()


def check_for_updates(engine):

    with Path(local_version_path).open(encoding="UTF-8") as source:
        local_state = json.load(source)

    if (
        local_state["version"] != engine.gdoc_fields.get("version")
        or not Path(local_writeup_path).exists()
    ):

        with st.spinner(
            f"New writeup (version {engine.gdoc_fields.get('version')}) available. Summoning.. 🪄"
        ):
            engine.export_to_markdown(path=local_writeup_path)

    local_state["version"] = engine.gdoc_fields.get("version")
    with Path(local_version_path).open("w", encoding="UTF-8") as target:
        json.dump(local_state, target)


if "engine" not in st.session_state:

    engine = start_engine("secrets/service-account-key.json")
    st.session_state["engine"] = engine

st.session_state["engine"].get_file_info(
    "1RMfhEvBb94N1JiU1gAzxrUkJowM87WbFn03zfLxnyk0"
)
check_for_updates(st.session_state["engine"])

st.sidebar.text(
    f"Version: {st.session_state['engine'].gdoc_fields.get('version')}"
)
st.markdown(Path(local_writeup_path).read_text(), unsafe_allow_html=True)
