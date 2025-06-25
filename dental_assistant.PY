import streamlit as st
import openai
import smtplib
from email.message import EmailMessage

# 1️⃣ Configurazione pagina Streamlit
st.set_page_config(page_title="Assistente AI - Studio Dentistico Pincopallino")

# 2️⃣ Interfaccia utente
st.title("🦷 Chatbot – Studio Dentistico Pincopallino")
user_input = st.text_input("Fai una domanda o chiedi un appuntamento:")

# 3️⃣ Chiavi segrete (definite in Streamlit ➜ Secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"]
OWNER_EMAIL    = st.secrets["OWNER_EMAIL"]
SMTP_PASS      = st.secrets["SMTP_PASS"]

# 4️⃣ Prompt base
PROMPT_BASE = Path("prompt.txt").read_text()

def ai_reply(message: str) -> str:
    """Interroga GPT-4/3.5 e restituisce la risposta."""
    completion = openai.ChatCompletion.create(
        model="gpt-4o",               # o gpt-3.5-turbo-1106 se vuoi risparmiare
        temperature=0.7,
        messages=[
            {"role": "system", "content": PROMPT_BASE},
            {"role": "user", "content": message}
        ],
    )
    return completion.choices[0].message.content.strip()

def send_email(question: str, answer: str) -> None:
    """Invia i dettagli del lead al dentista via Gmail."""
    msg = EmailMessage()
    msg["Subject"] = "Nuovo contatto dal chatbot"
    msg["From"] = OWNER_EMAIL
    msg["To"] = OWNER_EMAIL
    msg.set_content(f"DOMANDA UTENTE:\n{question}\n\nRISPOSTA AI:\n{answer}")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(OWNER_EMAIL, SMTP_PASS)
        smtp.send_message(msg)

if user_input:
    risposta = ai_reply(user_input)
    st.markdown("**Risposta del chatbot:**")
    st.write(risposta)

    # invia mail se l’utente menziona contatti/appuntamento
    trigger = any(x in user_input.lower() for x in ["email", "telefono", "appuntamento"])
    if trigger:
        send_email(user_input, risposta)
        st.success("📩 Dati inviati allo studio. Grazie!")
