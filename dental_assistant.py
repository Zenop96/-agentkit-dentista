import streamlit as st
from pathlib import Path
from openai import OpenAI
import smtplib
from email.message import EmailMessage

# --- Config pagina ---
st.set_page_config(page_title="Assistente AI - Studio Dentistico Pincopallino")

st.title("🦷 Chatbot – Studio Dentistico Pincopallino")
user_input = st.text_input("Fai una domanda o chiedi un appuntamento:")

# --- Client OpenAI ---
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# --- Prompt base ---
PROMPT_BASE = Path('prompt.txt').read_text()

def ai_reply(msg: str) -> str:
    completion = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': PROMPT_BASE},
            {'role': 'user',   'content': msg}
        ],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()

def send_email(question: str, answer: str) -> None:
    owner = st.secrets['OWNER_EMAIL']
    smtp_pass = st.secrets['SMTP_PASS']
    msg = EmailMessage()
    msg['Subject'] = 'Nuovo contatto dal chatbot'
    msg['From'] = owner
    msg['To'] = owner
    msg.set_content(f'DOMANDA UTENTE:\n{question}\n\nRISPOSTA AI:\n{answer}')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(owner, smtp_pass)
        smtp.send_message(msg)

if user_input:
    answer = ai_reply(user_input)
    st.markdown('**Risposta del chatbot:**')
    st.write(answer)

    if any(k in user_input.lower() for k in ['email', 'telefono', 'appuntamento', 'contatto']):
        send_email(user_input, answer)
        st.success('📩 I tuoi dati sono stati inviati allo studio. Grazie!')
