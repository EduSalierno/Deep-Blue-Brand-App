... (il codice corrente) ...

                # --- Gestione progetti salvati su OneDrive con tag, dashboard, ricerca e commenti ---
                st.subheader("📁 Progetti salvati su OneDrive")
                drive_response = requests.get(
                    url="https://graph.microsoft.com/v1.0/me/drive/root:/DeepBlue:/children",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                if drive_response.status_code == 200:
                    files = drive_response.json().get("value", [])
                    project_files = [f for f in files if f['name'].endswith(('.txt', '.docx', '.pptx'))]

                    if project_files:
                        st.markdown("### 📊 Dashboard progetti")

                        search_query = st.text_input("🔎 Cerca per nome o tag")
                        filtered_projects = []

                        for f in project_files:
                            filename = f['name']
                            modified = f['lastModifiedDateTime'][:10]
                            size_kb = int(f['size']) // 1024
                            tag = "Testuale" if filename.endswith(".txt") else "Word" if filename.endswith(".docx") else "Slide"

                            if search_query.lower() in filename.lower() or search_query.lower() in tag.lower():
                                filtered_projects.append((filename, modified, size_kb, tag))

                        if not search_query:
                            filtered_projects = [(f['name'], f['lastModifiedDateTime'][:10], int(f['size']) // 1024,
                                                  "Testuale" if f['name'].endswith(".txt") else "Word" if f['name'].endswith(".docx") else "Slide")
                                                 for f in project_files]

                        for filename, modified, size_kb, tag in filtered_projects:
                            st.markdown(f"**📌 {filename}**  ")
                            st.markdown(f"Tag: `{tag}` | Modificato: {modified} | Dimensione: {size_kb} KB")

                        selected_project = st.selectbox("📂 Apri un progetto esistente:", [fp[0] for fp in filtered_projects])
                        if st.button("🔍 Visualizza contenuto"):
                            selected_file = next(f for f in project_files if f['name'] == selected_project)
                            file_download = requests.get(
                                selected_file['@microsoft.graph.downloadUrl'],
                                headers={"Authorization": f"Bearer {access_token}"}
                            )
                            st.subheader(f"📄 Contenuto di {selected_project}")
                            if selected_project.endswith(".txt"):
                                st.text(file_download.text)
                            elif selected_project.endswith(".docx"):
                                from docx import Document
                                from io import BytesIO
                                doc = Document(BytesIO(file_download.content))
                                for para in doc.paragraphs:
                                    st.markdown(para.text)
                            elif selected_project.endswith(".pptx"):
                                st.info("Visualizzazione di presentazioni non ancora supportata, ma il file è stato aperto correttamente.")

                            # Campo note/commenti per progetto selezionato
                            st.markdown("### 🗒️ Aggiungi nota al progetto")
                            comment_text = st.text_area("Scrivi una nota (non salvata su OneDrive)")
                            if comment_text:
                                st.success("Nota registrata in sessione: puoi copiarla o salvarla manualmente nel progetto.")
                                st.markdown(f"**📝 Nota:** {comment_text}")
                    else:
                        st.info("Nessun progetto salvato trovato nella cartella /DeepBlue su OneDrive.")
                else:
                    st.warning("Errore nell'accesso a OneDrive. Verifica i permessi o riprova.")
