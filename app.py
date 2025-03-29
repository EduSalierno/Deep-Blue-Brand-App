st.set_page_config(page_title="Deep Blue Brand – Chat", layout="wide")
st.title("💬 Deep Blue Brand – Chat Conversazionale")
st.markdown("Parla direttamente con il tuo agente strategico semiotico. Usa linguaggio naturale o attiva le funzioni rapide (es. `/claim`, `/benchmark`).")

# API Key e Assistant ID (personale dell'utente)
openai.api_key = st.secrets["openai_api_key"]
assistant_id = "asst_NemsAtDQojTsh7Jt1rdHR406"

# Stato di sessione per i messaggi
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostra la chat pregressa
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input dell'utente
prompt = st.chat_input("Scrivi qui la tua richiesta (anche con /funzioni)...")

if prompt:
    # Mostra subito il messaggio dell'utente
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Crea il thread se non esiste
    if "thread_id" not in st.session_state:
        thread = openai.beta.threads.create()
        st.session_state.thread_id = thread.id

    # Invia il messaggio al thread
    openai.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt
    )

    # Avvia esecuzione con l'agente Deep Blue Brand
    run = openai.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id,
    )

    # Attendi la risposta
    with st.spinner("Analisi in corso con il tuo agente Deep Blue..."):
        while True:
            run_check = openai.beta.threads.runs.retrieve(thread_id=st.session_state.thread_id, run_id=run.id)
            if run_check.status == "completed":
                break
            time.sleep(1)

        messages = openai.beta.threads.messages.list(thread_id=st.session_state.thread_id)
        reply = messages.data[0].content[0].text.value

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
