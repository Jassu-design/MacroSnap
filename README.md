# 🥗 MacroSnap

MacroSnap is a simple AI-powered nutrition assistant that helps you understand what you're eating.

You can either **upload a photo of your meal** or describe it in text, and MacroSnap uses Google Gemini to estimate the calories and macros such as protein, carbohydrates, and fat.

At the end of the conversation, you can also send a summary of your meals directly to **Telegram**.

## 🚀 Live Demo

[Try MacroSnap](https://macrosnap-cweianxadg7zii3pxymjy8.streamlit.app/)

## ✨ Features

- 📸 Upload a photo of your meal
- 💬 Describe your meal using text
- 🤖 AI-powered meal analysis using Google Gemini
- 🔥 Estimated calorie breakdown
- 💪 Protein, carbs, and fat estimation
- 💬 Conversational interface for discussing multiple meals
- 📊 Generate a summary of all meals discussed
- 📲 Send the daily nutrition summary to Telegram
- 🔐 API keys are handled through Streamlit secrets

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – Web interface
- **Google Gemini API** – Meal and nutrition analysis
- **Telegram Bot API** – Sending nutrition summaries
- **Requests** – API requests
- **Google GenAI SDK** – Gemini integration

## 📂 Project Structure

```text
MacroSnap/
│
├── app.py              # Main Streamlit application
├── prompts.py          # AI system and summary prompts
├── requirements.txt    # Python dependencies
└── .gitIgnore          # Ignored files
```

## ⚙️ How It Works

The basic flow is:

```text
User
  ↓
Upload meal photo / Enter meal description
  ↓
Streamlit
  ↓
Google Gemini
  ↓
Meal + Calories + Macros
  ↓
Conversation continues
  ↓
Generate daily summary
  ↓
Send summary to Telegram
```

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Jassu-design/MacroSnap.git
cd MacroSnap
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API keys

Create a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
```

Keep this file private and **never upload your API keys to GitHub**.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🤖 AI Prompting

MacroSnap uses a custom system prompt to keep Gemini focused on nutrition-related questions.

For each meal, the AI is instructed to provide:

- What the meal appears to be
- Estimated calories
- Estimated protein
- Estimated carbohydrates
- Estimated fat

The project also uses a separate prompt to combine the meals discussed in the conversation into a single nutrition summary.

## ⚠️ Note

The nutrition values provided by MacroSnap are **AI-generated estimates** and should not be treated as exact nutritional measurements. Actual calories and macros can vary depending on ingredients, portion sizes, and preparation methods.

## 📌 Future Improvements

Some things I would like to add in the future:

- Save meal history between sessions
- Add a proper daily/weekly dashboard
- Track nutrition goals
- Add charts for calories and macros
- Support more nutrition information
- Improve accuracy using a structured food database

## 👨‍💻 Author

**Jaswant Prajapat**

BCA Graduate | MERN Stack Developer | Python & AI Enthusiast

GitHub: [Jassu-design](https://github.com/Jassu-design)
