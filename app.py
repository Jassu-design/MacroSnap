import requests
from google import genai
from google.genai import types
import streamlit as st
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE,SUMMARY_REQUEST_PROMPT

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]



@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key = GEMINI_API_KEY)


gemini_client = get_gemini_client()
Model_Name = "gemini-3.6-flash"
submitted=""

def render_message(messages):
    with st.chat_message(messages["role"]):
        if messages["content_type"] == "text":
            st.write(messages["content"])
        elif messages["content_type"] == "image":
            st.image(messages["content"])
    

def add_message(role, content_type, content):
    st.session_state.messages.append({
        "role": role,
        "content_type": content_type,
        "content": content
    })
    render_message(st.session_state.messages[-1])


def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry Something went Wron {error}"

def clean_telegram_text(text):
    if not text:
        return "No nutrition summary available."
    text = " ".join(text.split())  # collapse whitespace/newlines
    return text[:4000] + "..." if len(text) > 4000 else text

def send_telegram(chat_id, name, summary):
    try:
        message = (
            f"🥗 *MacroSnap Daily Summary*\n\n"
            f"Hi {name}!\n\n"
            f"{clean_telegram_text(summary)}"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(
            url,
            json=payload,
            timeout=15
        )

        data = response.json()

        if response.ok and data.get("ok"):
            return True, data["result"]["message_id"]

        return False, data.get("description", "Telegram API error")

    except Exception as error:
        return False, str(error)


#step 1: onboarding
if 'onboarded' not in st.session_state:
    st.title("Welcome to MacroSnap! 🥗")
    st.caption("Your instant calorie & macro decoder 🥗")

    with st.form("onboarding_form"):
        name = st.text_input("What's your name?",
        placeholder="Enter your name")

        telegram_id = st.text_input("What's your Telegram ID?",
        placeholder="Enter your Telegram ID")

        submitted = st.form_submit_button("Let's get started!")
    if submitted:
        if not name.strip() or not telegram_id.strip():
            st.warning("Please fill in all the fields before proceeding.")
        else:
            st.session_state.name = name.strip()
            st.session_state.telegram_id = telegram_id.strip()
            # Active my AI
            st.session_state.chat = gemini_client.chats.create(
                model = Model_Name,
                config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
            )
            st.session_state.messages=[]
            st.session_state.onboarded=True
            st.rerun()
    st.stop()

# Create a chat Interface
header_col, button_col = st.columns([5, 2], vertical_alignment="center")

with header_col:
    st.title("🥗 MacroSnap")

with button_col:
    send_disabled = len(st.session_state.messages) <= 1
    if st.button("📤 Send to Telegram", disabled=send_disabled,
                  use_container_width=True):
        with st.spinner("Summarizing your day..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
        success, info = send_telegram(st.session_state.telegram_id, st.session_state.name, summary)
        if success:
            st.success("Sent! Check your Telegram 📲")
        else:
            st.error(f"Couldn't send that: {info}")


st.caption(f"Logged in as {st.session_state.name} - updates go to {st.session_state.telegram_id}")

if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)

user_input = st.chat_input(
        "Ask a question or upload an image of your meal",
        accept_file = True,
        file_type=["png", "jpg", "jpeg"]
        )
if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user","image",photo_bytes)
        parts.append(types.Part.from_bytes(data = photo_bytes, mime_type=photo.type))
    if text:
        add_message("user","text",text)
        parts.append(text)
    elif photo is not None: #if user uplaod an image and not aske any question
        parts.append("What is this meal? Give me the calories  and macros!")

    with st.spinner("Wait for a moment......."):
        answer = ask_gemini(parts)
    add_message("assistant", "text", answer)



