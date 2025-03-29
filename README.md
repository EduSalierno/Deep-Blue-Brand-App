# Deep Blue Brand System

Questa è l'applicazione Streamlit per l'analisi semiotica e strategia di brand con integrazione OneDrive e supporto Copilot.

## 🔧 Requisiti
- Account Microsoft 365 con accesso a OneDrive
- API Key OpenAI
- Credenziali MSAL per autenticazione Microsoft

## 🚀 Deploy su Streamlit Cloud

1. Crea una nuova repository GitHub
2. Carica i file:
   - `app.py`
   - `requirements.txt`
   - `README.md`
3. Crea i secrets su Streamlit Cloud:

```toml
# .streamlit/secrets.toml
openai_api_key = "your-openai-key"
ms_client_id = "your-client-id"
ms_client_secret = "your-client-secret"
ms_tenant_id = "your-tenant-id"
```

4. Connetti la repo a [streamlit.io/cloud](https://streamlit.io/cloud) e clicca **Deploy**

## 📁 Funzionalità
- Upload e analisi di file PDF, Word, Excel, PowerPoint, ePub
- Generazione atlanti semiotici, cluster, mappe visive
- Salvataggio e gestione progetti su OneDrive
- Esportazione automatica di file Word e PPTX con prompt per Microsoft Copilot
