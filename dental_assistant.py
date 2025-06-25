import streamlit as st
import openai
import smtplib
from email.message import EmailMessage

# --- Impostazioni iniziali ---
st.set_page_config(page_title="Assistente AI - Studio Dentistico Pincopallino")

# --- Interfaccia utente ---
st.title("💬 Chatbot - Studio Dentistico Pincopallino")
st.write("Scrivi qui la tua domanda oppure chiedi un appuntamento:")

user_input = st.text_input("La tua domanda:")

# --- Carica chiavi segrete ---
openai.api_key = st.secrets["OPENAI_API_KEY"]
email_dest = st.secrets["OWNER_EMAIL"]
smtp_pass = st.secrets["SMTP_PASS"]

# --- Prompt base ---
prompt_base = open("prompt.txt").read()

# --- Funzione AI GPT ---
def chiedi_ai(messaggio):
    risposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt_base},
            {"role": "user", "content": messaggio}
        ],
        temperature=0.7
    )
    return risposta.choices[0].message["content"]

# --- Funzione invia email ---
def invia_email(testo_utente, risposta_ai):
    msg = EmailMessage()
    msg["Subject"] = "Nuovo contatto da chatbot"
    msg["From"] = email_dest
    msg["To"] = email_dest
    msg.set_content(f"Messaggio utente:\n{testo_utente}\n\nRisposta AI:\n{risposta_ai}")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_dest, smtp_pass)
        smtp.send_message(msg)

# --- Risposta e invio se ci sono contatti ---
if user_input:
    risposta = chiedi_ai(user_input)
    st.markdown("**Risposta del chatbot:**")
    st.write(risposta)

    parole_chiave = ["email", "telefono", "appuntamento", "contatto"]
    if any(k in user_input.lower() for k in parole_chiave):
        invia_email(user_input, risposta)
        st.success("📩 I tuoi dati sono stati inviati allo studio. Grazie!")
