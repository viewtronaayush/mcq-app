import streamlit as st
from pypdf import PdfReader
import docx
import os
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="MCQ Practice App",
    page_icon="🧠",
    layout="centered"
)

st.title("MCQ Practice App")

st.write("Upload your document and generate MCQs")


uploaded_file = st.file_uploader(
    "Upload PDF or DOCX file",
    type=["pdf","docx","txt"]
)


def read_file(file):

    text = ""

    if file.name.endswith(".pdf"):

        pdf = PdfReader(file)

        for page in pdf.pages:

            text += page.extract_text()


    elif file.name.endswith(".docx"):

        doc = docx.Document(file)

        for para in doc.paragraphs:

            text += para.text


    elif file.name.endswith(".txt"):

        text = file.read().decode()


    return text



def generate_mcq(text):

    prompt = f"""
    Generate 5 multiple choice questions from the text below.

    Format:
    Question
    A)
    B)
    C)
    D)
    Answer:

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content

if uploaded_file:

    text = read_file(uploaded_file)

    st.success("Text extracted successfully ✅")


if st.button("Generate MCQs"):

    mcqs = generate_mcq(text)

    st.write(mcqs)
