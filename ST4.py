import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import fitz  # PyMuPDF
import docx

API_KEY = "YOUR_API_KEY"

def chat(question):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        api_key=API_KEY
    )

    # Inisialisasi riwayat percakapan jika belum ada
    if "messages" not in st.session_state:
        st.session_state.messages = [
            (
                "system",
                "You are a helpful assistant. Always answer in Indonesian language.",
            )
        ]

    # Tambahkan pesan pengguna baru
    st.session_state.messages.append(("human", question))

    ai_msg = llm.invoke(st.session_state.messages)
    st.session_state.messages.append(("assistant", ai_msg.content))

    return ai_msg.content

# Tampilan judul dengan gambar balon
col1, col2 = st.columns([2, 1])
with col1:
    st.title("Welcome, di Ai nya Taufiq Bi Usuluddin")
with col2:
    st.image("E:/NLP/razer.png", width=150)

# Inisialisasi riwayat chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tampilkan riwayat chat dari sesi sebelumnya
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Reaksi terhadap input pengguna
if prompt := st.chat_input("Hi, ada yang bisa saya bantu"):
    # Tampilkan pesan pengguna di kotak pesan chat
    st.chat_message("user").markdown(prompt)
    # Tambahkan pesan pengguna ke riwayat chat
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    response = chat(prompt)
    answer = response

    # Tampilkan respons asisten di kotak pesan chat
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Tambahkan respons asisten ke riwayat chat
    st.session_state.chat_history.append({"role": "assistant", "content": answer})

# Bagian untuk unggah dan tampilkan file
st.subheader("Silahkan Unggah file di sini ya :), Jika di diperlukan saja!")
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xls', 'xlsx', 'pdf', 'docx'])

if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        st.write(df)
    elif uploaded_file.type == "application/vnd.ms-excel" or uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
        st.write(df)
    elif uploaded_file.type == "application/pdf":
        # Baca dan tampilkan PDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        st.text_area("PDF Content", text, height=500)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Baca dan tampilkan DOCX
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        st.text_area("DOCX Content", text, height=500)