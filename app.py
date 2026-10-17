import streamlit as st
import requests
import streamlit.components.v1 as components
import html

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# CONSTANTS
# ==========================================================

API_URL = "http://127.0.0.1:5000/translate"
LANGUAGES_URL = "http://127.0.0.1:5000/languages"

LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Marathi (मराठी)": "mr",
    "Bengali (বাংলা)": "bn",
    "Tamil (தமிழ்)": "ta",
    "Telugu (తెలుగు)": "te",
    "Gujarati (ગુજરાતી)": "gu",
    "Kannada (ಕನ್ನಡ)": "kn",
    "Malayalam (മലയാളം)": "ml",
    "Punjabi (ਪੰਜਾਬੀ)": "pa",
    "Urdu (اردو)": "ur",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Chinese": "zh",
    "Arabic": "ar",
    "Korean": "ko",
    "Dutch": "nl",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Polish": "pl",
    "Indonesian": "id",
    "Vietnamese": "vi",
    "Thai": "th",
    "Swahili": "sw"
}

MAX_CHARACTERS = 5000

# ==========================================================
# SESSION STATE
# ==========================================================

defaults = {
    "source_language": "Auto Detect",
    "target_language": "Hindi (हिन्दी)",
    "input_text": "",
    "translated_text": "",
    "detected_language": "",
    "last_translation_error": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    /* Main application background */

    .stApp {
        background: linear-gradient(
            180deg,
            #f3f7ff 0%,
            #ffffff 55%,
            #f5f8ff 100%
        );
    }

    .block-container {
        max-width: 1600px;
        padding: 1.8rem 2rem 2rem 2rem;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Main heading */

    .hero {
        background: linear-gradient(
            115deg,
            #0869e8 0%,
            #4778f5 50%,
            #9b79f7 100%
        );
        padding: 36px 40px;
        border-radius: 22px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 12px 32px rgba(54, 105, 220, 0.18);
    }

    .hero-title {
        color: #ffffff !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        line-height: 1.25 !important;
        letter-spacing: -1px;
        margin: 0 !important;
        padding: 0 !important;
    }

    .hero-subtitle {
        color: #ffffff !important;
        font-size: 18px !important;
        line-height: 1.6 !important;
        margin-top: 12px !important;
        margin-bottom: 0 !important;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 18px;
        padding: 8px 15px;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.35);
        border-radius: 30px;
        color: #ffffff;
        font-size: 13px;
        font-weight: 650;
    }

    /* Section headings */

    .section-heading {
        color: #173a72;
        font-size: 21px;
        font-weight: 750;
        margin-top: 12px;
        margin-bottom: 14px;
    }

    .panel-heading {
        font-size: 20px;
        font-weight: 750;
        margin-bottom: 12px;
    }

    .input-heading {
        color: #17468d;
    }

    .output-heading {
        color: #087f68;
    }

    /* Language selectors */

    .stSelectbox label {
        color: #244574 !important;
        font-size: 15px !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 52px;
        border-radius: 11px;
        border-color: #d5e1f5;
        background: white;
    }

    div[data-baseweb="select"] * {
        font-size: 15px;
    }

    /* Text input */

    .stTextArea label {
        color: #244574 !important;
        font-size: 15px !important;
        font-weight: 700 !important;
    }

    .stTextArea textarea {
        min-height: 255px !important;
        font-size: 18px !important;
        line-height: 1.7 !important;
        border-radius: 12px !important;
        border: 1px solid #d5e1f5 !important;
        background: #ffffff !important;
        color: #243b5e !important;
        padding: 16px !important;
    }

    .stTextArea textarea:focus {
        border-color: #4c88ff !important;
        box-shadow: 0 0 0 2px rgba(76,136,255,0.12) !important;
    }

    /* Output panel */

    .output-box {
        background: linear-gradient(
            145deg,
            #f1fbf8,
            #f8fffd
        );
        border: 1px solid #c7eee3;
        border-top: 4px solid #21b99a;
        border-radius: 15px;
        padding: 20px;
        min-height: 255px;
        color: #173b4b;
        font-size: 20px;
        line-height: 1.8;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        box-sizing: border-box;
    }

    .output-placeholder {
        color: #8192aa;
        font-size: 17px;
        font-style: italic;
    }

    .output-label {
        color: #087f68;
        font-size: 20px;
        font-weight: 750;
        margin-bottom: 12px;
    }

    /* Buttons */

    .stButton > button {
        border-radius: 11px;
        min-height: 47px;
        font-size: 15px;
        font-weight: 650;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #3478f6;
        transform: translateY(-1px);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(
            100deg,
            #2677fa,
            #3670f4
        );
        color: white;
        border: none;
        min-height: 60px;
        font-size: 19px;
        font-weight: 750;
        box-shadow: 0 5px 15px rgba(38,119,250,0.16);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(
            100deg,
            #155fe0,
            #285ce0
        );
        color: white;
    }

    .stDownloadButton > button {
        border-radius: 10px;
        min-height: 45px;
        font-weight: 650;
    }

    /* Features */

    .features-heading {
        color: #17468d;
        font-size: 23px;
        font-weight: 800;
        text-align: center;
        margin-top: 34px;
        margin-bottom: 20px;
    }

    .feature-card {
        background: linear-gradient(
            145deg,
            #eef5ff,
            #f7f5ff
        );
        border: 1px solid #e0eafb;
        border-radius: 16px;
        padding: 22px 12px;
        min-height: 145px;
        text-align: center;
    }

    .feature-icon {
        font-size: 31px;
        margin-bottom: 8px;
    }

    .feature-title {
        color: #17468d;
        font-size: 15px;
        font-weight: 750;
        margin-bottom: 7px;
    }

    .feature-description {
        color: #637ba2;
        font-size: 13px;
        line-height: 1.5;
    }

    .footer-text {
        text-align: center;
        color: #8092b0;
        font-size: 13px;
        padding-top: 28px;
        padding-bottom: 8px;
    }

    /* Mobile layout */

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        .hero {
            padding: 25px 20px;
            border-radius: 17px;
        }

        .hero-title {
            font-size: 30px !important;
        }

        .hero-subtitle {
            font-size: 15px !important;
        }

        .stTextArea textarea {
            min-height: 190px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data(ttl=300)
def get_available_languages():
    try:
        response = requests.get(
            LANGUAGES_URL,
            timeout=5
        )

        response.raise_for_status()
        data = response.json()

        return {
            item["code"]
            for item in data
            if isinstance(item, dict) and "code" in item
        }

    except (
        requests.RequestException,
        ValueError,
        TypeError
    ):
        return None


available_codes = get_available_languages()

if available_codes is None:
    st.warning(
        "Cannot connect to LibreTranslate. "
        "Please check that the translation server is running "
        "at http://127.0.0.1:5000."
    )

    supported_languages = LANGUAGES.copy()

else:
    supported_languages = {
        name: code
        for name, code in LANGUAGES.items()
        if code == "auto" or code in available_codes
    }

if not any(
    code != "auto"
    for code in supported_languages.values()
):
    st.error(
        "No supported target languages were found. "
        "Please check your LibreTranslate server."
    )
    st.stop()

target_options = [
    name
    for name, code in supported_languages.items()
    if code != "auto"
]

# Correct any saved selection that isn't currently available.

if st.session_state.source_language not in supported_languages:
    st.session_state.source_language = "Auto Detect"

if st.session_state.target_language not in target_options:
    st.session_state.target_language = (
        "Hindi (हिन्दी)"
        if "Hindi (हिन्दी)" in target_options
        else target_options[0]
    )

# ==========================================================
# LANGUAGE SELECTORS
# ==========================================================

st.markdown(
    '<div class="section-heading">🌐 Choose Your Languages</div>',
    unsafe_allow_html=True
)

language_col1, swap_col, language_col2 = st.columns(
    [5, 0.8, 5],
    vertical_alignment="bottom"
)

with language_col1:
    st.selectbox(
        "Translate From",
        options=list(supported_languages.keys()),
        key="source_language"
    )

with swap_col:
    st.write("")

    swap_clicked = st.button(
        "⇄",
        help="Swap source and target languages",
        use_container_width=True
    )

with language_col2:
    st.selectbox(
        "Translate To",
        options=target_options,
        key="target_language"
    )

if swap_clicked:
    source_now = st.session_state.source_language
    target_now = st.session_state.target_language

    if source_now == "Auto Detect":
        st.info(
            "Select a specific source language before swapping."
        )
    else:
        st.session_state.source_language = target_now
        st.session_state.target_language = source_now

        # Move the existing translation into the input box.
        if st.session_state.translated_text:
            st.session_state.input_text = (
                st.session_state.translated_text
            )

        st.session_state.translated_text = ""
        st.session_state.detected_language = ""

        st.rerun()

# ==========================================================
# TRANSLATION PANELS
# ==========================================================

st.markdown("---")

input_col, output_col = st.columns(
    2,
    gap="large"
)

with input_col:
    st.markdown(
        '<div class="panel-heading input-heading">'
        '📝 Enter Text to Translate</div>',
        unsafe_allow_html=True
    )

    input_text = st.text_area(
        "Input text",
        placeholder=(
            "Type or paste your text here...\n\n"
            "Example: Hello, how are you?"
        ),
        height=255,
        max_chars=MAX_CHARACTERS,
        key="input_text",
        label_visibility="collapsed"
    )

    st.caption(
        f"Characters: {len(input_text)} / {MAX_CHARACTERS}"
    )

with output_col:
    st.markdown(
        '<div class="output-label">✨ Translation Result</div>',
        unsafe_allow_html=True
    )

    translated_text = st.session_state.translated_text

    if translated_text:
        safe_text = html.escape(translated_text)

        st.markdown(
            f'<div class="output-box">{safe_text}</div>',
            unsafe_allow_html=True
        )

        st.success("Translation completed successfully!")

        # Download the translated text.
        st.download_button(
            label="⬇️ Download Translation",
            data=translated_text,
            file_name="translated_text.txt",
            mime="text/plain",
            use_container_width=True
        )

        # Copy to clipboard using the browser clipboard API.
        # Clipboard access generally requires localhost or HTTPS.
        clipboard_text = html.escape(
            translated_text,
            quote=True
        )

        copy_html = f"""
        <div style="margin-top: 8px;">
            <button id="copy-translation"
                style="
                    width: 100%;
                    padding: 12px;
                    background: white;
                    border: 1px solid #c7d8ef;
                    border-radius: 10px;
                    color: #17468d;
                    font-size: 15px;
                    font-weight: 650;
                    cursor: pointer;
                ">
                📋 Copy Translation
            </button>
            <div id="copy-status"
                style="
                    color: #087f68;
                    font-size: 13px;
                    margin-top: 6px;
                "></div>
        </div>

        <script>
        const textToCopy = {repr(translated_text)};

        document.getElementById("copy-translation")
            .addEventListener("click", async function() {{
                const status = document.getElementById("copy-status");

                try {{
                    await navigator.clipboard.writeText(textToCopy);
                    status.textContent = "Copied to clipboard!";
                }} catch (error) {{
                    status.textContent =
                        "Clipboard unavailable. Please use Download Translation.";
                }}
            }});
        </script>
        """

        components.html(
            copy_html,
            height=85
        )

        if st.session_state.detected_language:
            st.caption(
                "Detected source language: "
                + st.session_state.detected_language
            )

    else:
        st.markdown(
            """
            <div class="output-box">
                <span class="output-placeholder">
                    Your translated text will appear here...
                    <br><br>
                    Select your languages, enter text,
                    and click Translate Text.
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================================
# ACTION BUTTONS
# ==========================================================

st.markdown("")

translate_col, clear_col = st.columns(
    [3, 1],
    gap="medium"
)

with translate_col:
    translate_clicked = st.button(
        "🌐  Translate Text",
        type="primary",
        use_container_width=True
    )

with clear_col:
    clear_clicked = st.button(
        "🗑️  Clear All",
        use_container_width=True
    )

if clear_clicked:
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.session_state.detected_language = ""
    st.session_state.last_translation_error = ""

    st.rerun()

# ==========================================================
# TRANSLATION LOGIC
# ==========================================================

if translate_clicked:

    source_language = st.session_state.source_language
    target_language = st.session_state.target_language
    input_text = st.session_state.input_text

    if not input_text.strip():
        st.warning(
            "Please enter some text before translating."
        )

    elif source_language == target_language:
        st.warning(
            "Please choose different source and target languages."
        )

    elif (
        source_language not in supported_languages
        or target_language not in supported_languages
    ):
        st.error(
            "The selected language is not supported "
            "by the current translation server."
        )

    else:
        source_code = supported_languages[source_language]
        target_code = supported_languages[target_language]

        try:
            with st.spinner(
                "Translating your text... Please wait."
            ):
                response = requests.post(
                    API_URL,
                    data={
                        "q": input_text,
                        "source": source_code,
                        "target": target_code,
                        "format": "text"
                    },
                    timeout=120
                )

                response.raise_for_status()
                result = response.json()

            translated_result = result.get(
                "translatedText",
                ""
            )

            if not translated_result:
                st.error(
                    "The translation service returned an empty result. "
                    "Please try again."
                )

            else:
                st.session_state.translated_text = translated_result
                st.session_state.last_translation_error = ""

                detected = result.get(
                    "detectedLanguage",
                    {}
                )

                if isinstance(detected, dict):
                    st.session_state.detected_language = (
                        detected.get("language", "")
                    )

                st.rerun()

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to LibreTranslate. "
                "Please start the server in your other terminal "
                "using: libretranslate --host 127.0.0.1 --port 5000"
            )

        except requests.exceptions.Timeout:
            st.error(
                "The translation request timed out. "
                "Please try again with shorter text."
            )

        except requests.exceptions.HTTPError as error:
            details = response.text[:500]

            st.error(
                f"Translation failed: {error}. Server details: {details}"
            )

        except (
            requests.exceptions.RequestException,
            ValueError,
            TypeError
        ) as error:
            st.error(
                f"An unexpected translation error occurred: {error}"
            )

# ==========================================================
# FEATURES SECTION
# ==========================================================

st.markdown(
    """
    <div class="features-heading">
        Why Use Our Translation Tool?
    </div>
    """,
    unsafe_allow_html=True
)

feature1, feature2, feature3 = st.columns(3, gap="medium")

with feature1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🌍</div>
            <div class="feature-title">Multiple Languages</div>
            <div class="feature-description">
                Translate between languages supported
                by the translation service.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with feature2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast Translation</div>
            <div class="feature-description">
                Translate your text with a simple,
                convenient interface.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with feature3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">✨</div>
            <div class="feature-title">Easy to Use</div>
            <div class="feature-description">
                A clean design with readable text
                and simple controls.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="footer-text">
        CodeAlpha Internship Project
        &nbsp; | &nbsp;
        Language Translation Tool
        <br><br>
        Built with Python, Streamlit and LibreTranslate
    </div>
    """,
    unsafe_allow_html=True
)
