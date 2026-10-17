# 🌍 Language Translation Tool

A simple, interactive language translation application developed using Python and Streamlit. The application uses LibreTranslate to translate text between supported languages through a clean, user-friendly interface.

## ✨ Features

* Translate text between supported languages.
* Select source and target languages.
* Automatically detect the source language when supported.
* Swap the source and target languages.
* Copy translated text to the clipboard.
* Download translated text.
* Clear the input and output.
* Display helpful messages when an error occurs.
* Use a modern, responsive interface.

## 🛠️ Technologies Used

* Python
* Streamlit
* Requests
* LibreTranslate API

## 📁 Project Structure

```text
CodeAlpha_LanguageTranslationTool/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/                 # Local environment; not uploaded to GitHub
```

## ⚙️ Prerequisites

Before running the project, install:

* Python 3
* Git
* A web browser
* LibreTranslate running locally

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual URL of your GitHub repository.

### 2. Open the project directory

```bash
cd CodeAlpha_LanguageTranslationTool
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Start LibreTranslate

LibreTranslate must be installed and running locally. Start it using the installation method configured on your computer.

The application expects the translation API to be available at:

```text
http://127.0.0.1:5000
```

Keep the LibreTranslate server running while using the application.

### 7. Run the application

Open another terminal in the project directory and run:

```bash
streamlit run app.py
```

Open the local address displayed in the terminal, normally:

```text
http://localhost:8501
```

## 🧪 Testing

Test the application using these scenarios:

1. Translate English text into Hindi.
2. Translate English text into Marathi.
3. Change the source and target languages.
4. Swap the selected languages.
5. Copy the translated text.
6. Download the translation.
7. Submit empty input and verify the application's response.
8. Stop the LibreTranslate server and verify that the application displays an understandable error message.

## 🎯 Project Objective

The objective of this project is to demonstrate how Python, Streamlit, and a translation API can be combined to build an interactive language translation application.

## 👨‍💻 Author

Developed as part of the CodeAlpha Artificial Intelligence Internship.

## 📄 License

This project is intended for educational and internship purposes.
