
import streamlit as st
import openai

st.set_page_config(page_title="Deep Blue Brand System", layout="wide")
st.title("🔵 Deep Blue Brand System")
st.markdown("**Sistema operativo per l’analisi semiotica e la strategia di marca**")

openai.api_key = st.secrets["openai_api_key"]

# Upload file
uploaded_file = st.file_uploader("📂 Carica un file di testo (TXT per ora)", type=["txt"])

if uploaded_file:
    st.success("File caricato. Scegli una funzione strategica dalla sidebar.")
    base_text = uploaded_file.read().decode("utf-8", errors="ignore")
else:
    base_text = None

prompt_interni = {
    "/report": "Analizza il contenuto fornito e genera un'analisi semiotica discorsiva e interpretativa, evidenziando i principali codici, simboli e significati presenti.",
    "/benchmark": "Confronta due o più brand presenti nel testo, creando schede individuali e una tabella comparativa che evidenzi differenze e somiglianze nei loro posizionamenti.",
    "/scoring": "Valuta il profilo semio-simbolico del brand su 5 dimensioni, presentando i risultati in un radar visivo accompagnato da un commento strategico.",
    "/atlante": "Costruisci un Atlante Semiologico visivo, identificando cluster, archetipi, codici e opposizioni presenti nel contenuto analizzato.",
    "/claim": "Analizza il claim o payoff presente, identificandone l'archetipo, le polarità e le figure retoriche utilizzate. Propone alternative strategiche.",
    "/naming": "Esegui un'analisi semiotica del naming, valutandone struttura, sonorità, simbolismo e archetipo sottostante, con eventuali proposte alternative.",
    "/mappa": "Crea una mappa semiotica con assi valoriali, posizionando simbolicamente gli elementi chiave presenti nel testo.",
    "/visualcheck": "Analizza l'identità visiva descritta, valutando logo, palette colori, font e stile, fornendo un feedback progettuale basato su una lettura semiotica.",
    "/riflesso": "Esamina il 'mondo possibile' implicito nel brand, analizzando quale tipo di società, persona o utente viene rappresentato o evocato.",
    "/scenario": "Analizza lo scenario culturale o i trend emergenti descritti, evidenziando le principali dinamiche e implicazioni per il brand.",
    "/posizionamento": "Valuta il posizionamento simbolico del brand rispetto ai codici di settore, individuando spazi liberi e opportunità strategiche.",
    "/brandidentity": "Fornisce un'analisi completa dell'identità di marca, includendo core, promessa, naming, tono, visual, storytelling, identificando eventuali gap e incoerenze.",
    "/brandstrategy": "Costruisce una strategia di marca dettagliata, definendo purpose, vision, mission, value map, brand essence e narrative platform.",
    "/creativecopy": "Genera contenuti creativi strategicamente orientati, come naming, payoff, headline, concept di campagna e brand manifesto.",
    "/brandcanvas": "Guida attraverso una sessione completa utilizzando i canvas e gli strumenti di 'Brand the Change', come mission composer, insight generator, values game, brand essence, brand ladder, bullshit radar e brand thinking canvas.",
    "/namingbrief": "Genera un brief completo per un progetto di naming, definendo approccio, tono, target, esclusioni, costruzione e categorie.",
    "/namingconcepts": "Costruisce mappe associative, metafore, archetipi e territori semantici per facilitare l'ideazione di nomi.",
    "/namegen": "Genera proposte di naming in diverse categorie, come descrittivo, evocativo, coined, composto, astratto e fonosimbolico.",
    "/nameradar": "Valuta i nomi proposti secondo criteri strategici, quali evocatività, memorabilità, originalità e coerenza, presentando i risultati in un radar visivo.",
    "/experiencejourney": "Mappa l'esperienza dell'utente nel tempo, identificando touchpoint chiave, valore promesso vs. generato e codici simbolici coinvolti.",
    "/valorevissuto": "Analizza l'evoluzione del significato del brand nell'esperienza dell'utente, evidenziando cambiamenti percepiti e implicazioni.",
    "/brandlive": "Valuta la coerenza tra l'identità di marca e il comportamento osservato nei vari canali di contatto con il pubblico.",
    "/swot_analysis": "Genera una SWOT Analysis classica o narrativa, includendo un'interpretazione simbolica e strategica dei punti di forza, debolezza, opportunità e minacce.",
    "/pest_analysis": "Costruisce una PEST Analysis, offrendo una lettura culturale, competitiva, sociale e simbolica dei fattori politici, economici, sociali e tecnologici.",
    "/btc_canvas1": "Compila la Parte 1 del Brand Thinking Canvas, focalizzandosi su Brand Core, Identity e Interactions.",
    "/btc_canvas2": "Compila la Parte 2 del Brand Thinking Canvas, concentrandosi sulla mappatura degli Audience Insight."
}

selected_funzione = st.sidebar.selectbox("🧠 Scegli la funzione strategica", list(prompt_interni.keys()))

if selected_funzione and base_text:
    st.subheader(f"🧪 Funzione attiva: {selected_funzione}")
    funzione_descrizione = prompt_interni[selected_funzione]
    prompt_base = f"""Attiva la funzione `{selected_funzione}` del modello Deep Blue Brand. {funzione_descrizione}

Usa il seguente contenuto testuale come base culturale per generare un output strategico, non riassuntivo ma interpretativo:

{base_text}"""

    with st.spinner("Analisi in corso con GPT-4..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Agisci come un brand strategist specializzato in semiotica, design e copywriting."},
                {"role": "user", "content": prompt_base}
            ],
            temperature=0.7
        )
        output = response.choices[0].message.content
        st.markdown(output)
        st.download_button("📥 Scarica risultato", output, file_name=f"{selected_funzione[1:]}_deepblue.txt")
else:
    st.info("Per iniziare, carica un file e seleziona una funzione dalla sidebar.")
