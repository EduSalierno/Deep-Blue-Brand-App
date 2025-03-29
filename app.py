import streamlit as st
import openai
import os
from PyPDF2 import PdfReader
from ebooklib import epub
from bs4 import BeautifulSoup
import docx
from pptx import Presentation
import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

st.set_page_config(page_title="Deep Blue Brand System", layout="wide")
st.title("🔵 Deep Blue Brand System (versione semplificata)")
st.subheader("Analisi semiotica e strategia di brand potenziata da AI")

openai.api_key = st.secrets["openai_api_key"]

# Upload documenti
uploaded_file = st.file_uploader("📂 Carica un file (PDF, EPUB, Word, PowerPoint, Excel)", type=["pdf", "epub", "docx", "pptx", "xlsx", "xls"])

full_text = ""
if uploaded_file:
    st.success("✅ File caricato correttamente!")
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    if file_extension == ".pdf":
        reader = PdfReader(uploaded_file)
        full_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_extension == ".epub":
        book = epub.read_epub(uploaded_file)
        chapters = []
        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                chapters.append(soup.get_text())
        full_text = "\n".join(chapters)
    elif file_extension == ".docx":
        doc = docx.Document(uploaded_file)
        full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    elif file_extension == ".pptx":
        prs = Presentation(uploaded_file)
        slides_text = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    slides_text.append(shape.text)
        full_text = "\n".join(slides_text)
    elif file_extension in [".xlsx", ".xls"]:
        df = pd.read_excel(uploaded_file)
        full_text = df.to_string(index=False)

    analysis_type = st.selectbox("📊 Scegli un tipo di analisi", [
        "Analisi semiotica di base",
        "Atlante semiotico",
        "Insight strategici"
    ])

    if st.button("🚀 Avvia analisi"):
        with st.spinner("Elaborazione in corso con GPT-4..."):
            prompt = f"Esegui una {analysis_type.lower()} sul seguente testo:\n\n{full_text}\n\nRispondi in modo strutturato, identificando codici, tropi, opposizioni binarie, valori culturali e insight strategici. Elenca i codici principali come lista."

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sei un esperto di semiotica e brand strategy."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            output_text = response.choices[0].message.content
            st.subheader("🧠 Risultato dell'analisi")
            st.markdown(output_text)
            st.download_button("📥 Scarica il risultato", output_text, file_name="analisi_deepblue.txt")

            # Mappa dei codici
            st.subheader("🕸️ Mappa visuale dei codici")
            code_matches = re.findall(r"- (.+?)\n", output_text)
            unique_codes = list(set(code_matches))

            if len(unique_codes) > 1:
                G = nx.Graph()
                for code in unique_codes:
                    G.add_node(code)
                for i in range(len(unique_codes)):
                    for j in range(i + 1, len(unique_codes)):
                        G.add_edge(unique_codes[i], unique_codes[j])
                fig, ax = plt.subplots(figsize=(10, 6))
                pos = nx.spring_layout(G, seed=42)
                nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10, ax=ax)
                st.pyplot(fig)

            # Cluster
            st.subheader("🔍 Cluster semiotici tematici")
            try:
                vectorizer = TfidfVectorizer(stop_words='english')
                X = vectorizer.fit_transform(unique_codes)
                num_clusters = min(5, len(unique_codes))
                kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(X)
                clusters = {i: [] for i in range(num_clusters)}
                for i, label in enumerate(kmeans.labels_):
                    clusters[label].append(unique_codes[i])
                for label, codes in clusters.items():
                    st.markdown(f"**Cluster {label+1}**: {', '.join(codes)}")
            except Exception as e:
                st.warning(f"Impossibile generare cluster: {e}")
