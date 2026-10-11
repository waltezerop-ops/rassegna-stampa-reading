import pypdf
import streamlit as st
from gtts import gTTS

st.set_page_config(page_title="Listen AI Clone", page_icon="🎧", layout="centered")

st.title("🎧 Lettore Audio AI")
st.write("Carica un documento o incolla il testo per ascoltarlo.")

# Selezione lingua e voce
lingua = st.selectbox(
    "Seleziona Lingua",
    ["it", "en", "es", "fr", "de"],
    format_func=lambda x: {
        "it": "Italiano",
        "en": "Inglese",
        "es": "Spagnolo",
        "fr": "Francese",
        "de": "Tedesco",
    }[x],
)

tab1, tab2 = st.tabs(["📄 Carica PDF/TXT", "✍️ Incolla Testo"])

testo_da_leggere = ""

with tab1:
    uploaded_file = st.file_uploader(
        "Carica un file PDF o TXT", type=["pdf", "txt"]
    )
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            reader = pypdf.PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    testo_da_leggere += text + "\n"
        else:
            testo_da_leggere = str(uploaded_file.read(), "utf-8")

with tab2:
    testo_manuale = st.text_area("Incolla qui il tuo testo:", height=200)
    if testo_manuale:
        testo_da_leggere = testo_manuale

if st.button("▶️ Genera Audio", use_container_width=True):
    if testo_da_leggere.strip():
        with st.spinner("Generazione audio in corso..."):
            tts = gTTS(text=testo_da_leggere, lang=lingua, slow=False)
            tts.save("audio_output.mp3")

            st.success("Audio pronto!")
            st.audio("audio_output.mp3", format="audio/mp3")
    else:
        st.warning("Per favore inserisci del testo o carica un documento.")