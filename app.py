import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import emoji
from wordcloud import WordCloud
from collections import Counter
from io import StringIO
from datetime import datetime
import warnings
import hashlib
import json
import os

warnings.filterwarnings("ignore")

# ==================================================
# 🔐 LOGIN / AUTH SYSTEM
# ==================================================

USERS_FILE = "users.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    """Load users from the JSON file, creating a default admin on first run."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    default_users = {
        "z_c_hacker": {
            "password": hash_password("@zalak_1001"),
            "role": "admin",
            "created": str(datetime.now())
        }
    }
    save_users(default_users)
    return default_users


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def verify_login(username, password):
    users = load_users()
    if username in users and users[username]["password"] == hash_password(password):
        return True, users[username]["role"]
    return False, None


def register_user(username, password):
    if not username or not password:
        return False, "Username and password required"
    users = load_users()
    if username in users:
        return False, "Username already exists"
    users[username] = {
        "password": hash_password(password),
        "role": "user",
        "created": str(datetime.now())
    }
    save_users(users)
    return True, "Account created successfully. Please login."


def show_login_register_page():
    """Professional WhatsApp-style login/register screen shown before the app unlocks."""

    st.markdown("""
    <style>
    @keyframes bgDrift{
        0%{ background-position:20% 20%, 80% 10%, 50% 90%, 0% 0%; }
        50%{ background-position:60% 40%, 30% 60%, 20% 30%, 100% 100%; }
        100%{ background-position:20% 20%, 80% 10%, 50% 90%, 0% 0%; }
    }
    .stApp {
        background:
            radial-gradient(circle at 20% 20%, rgba(37,211,102,0.35) 0%, transparent 42%),
            radial-gradient(circle at 80% 15%, rgba(18,140,126,0.40) 0%, transparent 45%),
            radial-gradient(circle at 45% 90%, rgba(37,211,102,0.25) 0%, transparent 50%),
            linear-gradient(160deg, #04241f 0%, #075E54 50%, #052e29 100%);
        background-size:200% 200%, 200% 200%, 200% 200%, 100% 100%;
        animation:bgDrift 20s ease-in-out infinite;
    }
    .stApp::before{
        content:"";
        position:fixed;
        inset:0;
        background-image:radial-gradient(rgba(255,255,255,0.07) 1px, transparent 1px);
        background-size:28px 28px;
        pointer-events:none;
        z-index:0;
    }
    #MainMenu, header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    # ---- New background: glowing orbs + rising chat-icon particles (rendered directly, no iframe clipping) ---- #
    icon_pool = ["💬", "✅", "🔒", "📱", "😊", "📩", "🔐", "✨", "🟢"]
    particle_seeds = [
        (4, 18, 12.5, 0.0), (11, 22, 15.0, 1.2), (19, 16, 11.0, 2.4), (27, 26, 17.5, 0.6),
        (34, 20, 13.0, 3.1), (41, 15, 10.5, 1.8), (48, 24, 16.0, 0.3), (55, 19, 12.0, 2.9),
        (62, 28, 18.5, 1.5), (69, 17, 11.5, 3.6), (76, 23, 14.5, 0.9), (83, 21, 13.5, 2.1),
        (90, 27, 17.0, 1.0), (7, 25, 16.5, 4.2), (15, 18, 12.0, 3.4), (23, 20, 13.0, 0.4),
        (31, 16, 10.0, 2.7), (38, 24, 15.5, 1.1), (46, 19, 12.5, 3.9), (58, 22, 14.0, 0.7),
        (72, 17, 11.0, 2.0), (95, 26, 16.5, 1.6)
    ]

    particles_html = ""
    for i, (left, size, duration, delay) in enumerate(particle_seeds):
        icon = icon_pool[i % len(icon_pool)]
        particles_html += (
            f'<span class="chat-particle" style="left:{left}%; font-size:{size}px; '
            f'animation-duration:{duration}s; animation-delay:{delay}s;">{icon}</span>'
        )

    st.markdown(f"""
    <style>
    .bg-particles{{
        position:fixed; inset:0; width:100%; height:100%;
        overflow:hidden; pointer-events:none; z-index:0;
    }}
    .chat-particle{{
        position:absolute; bottom:-60px; opacity:0;
        animation-name:riseParticle; animation-timing-function:linear; animation-iteration-count:infinite;
        filter:drop-shadow(0 0 6px rgba(255,255,255,0.25));
    }}
    @keyframes riseParticle{{
        0%   {{ transform:translateY(0) rotate(0deg); opacity:0; }}
        8%   {{ opacity:0.85; }}
        90%  {{ opacity:0.45; }}
        100% {{ transform:translateY(-110vh) rotate(20deg); opacity:0; }}
    }}
    .glow-orb{{
        position:fixed; border-radius:50%; filter:blur(60px); opacity:0.45;
        pointer-events:none; z-index:0; animation:orbFloat ease-in-out infinite;
    }}
    @keyframes orbFloat{{
        0%,100% {{ transform:translate(0,0) scale(1); }}
        50%     {{ transform:translate(30px,-40px) scale(1.12); }}
    }}
    </style>
    <div class="glow-orb" style="width:260px;height:260px; left:8%;  top:12%; background:rgba(37,211,102,0.55); animation-duration:12s;"></div>
    <div class="glow-orb" style="width:320px;height:320px; left:70%; top:6%;  background:rgba(18,140,126,0.55); animation-duration:16s; animation-delay:1s;"></div>
    <div class="glow-orb" style="width:280px;height:280px; left:52%; top:72%; background:rgba(7,94,84,0.60);  animation-duration:14s; animation-delay:2s;"></div>
    <div class="glow-orb" style="width:200px;height:200px; left:20%; top:70%; background:rgba(37,211,102,0.40); animation-duration:18s; animation-delay:3s;"></div>
    <div class="bg-particles">{particles_html}</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    @keyframes cardPop{
        0%{ opacity:0; transform:translateY(35px) scale(0.96); }
        100%{ opacity:1; transform:translateY(0) scale(1); }
    }
    @keyframes logoFloat{
        0%,100%{ transform:translateY(0); }
        50%{ transform:translateY(-6px); }
    }
    @keyframes glowPulse{
        0%,100%{ box-shadow:0 0 0 rgba(37,211,102,0.0), 0 18px 40px rgba(0,0,0,0.30); }
        50%{ box-shadow:0 0 26px rgba(37,211,102,0.35), 0 18px 40px rgba(0,0,0,0.30); }
    }
    @keyframes fieldSlideIn{
        0%{ opacity:0; transform:translateX(-16px); }
        100%{ opacity:1; transform:translateX(0); }
    }
    div[data-testid="stForm"] div[data-testid="stTextInput"]{
        animation:fieldSlideIn .5s ease forwards;
        opacity:0;
    }
    div[data-testid="stForm"] div[data-testid="stTextInput"]:nth-of-type(1){ animation-delay:.12s; }
    div[data-testid="stForm"] div[data-testid="stTextInput"]:nth-of-type(2){ animation-delay:.24s; }
    div[data-testid="stForm"] div[data-testid="stTextInput"]:nth-of-type(3){ animation-delay:.36s; }

    .login-logo{
        text-align:center;
        font-size:3rem;
        margin-bottom:2px;
        animation:logoFloat 3s ease-in-out infinite;
    }
    .login-title{
        text-align:center;
        color:#ffffff;
        font-size:2.3rem;
        font-weight:800;
        margin-top:0px;
        margin-bottom:2px;
        letter-spacing:0.3px;
    }
    .login-sub{
        text-align:center;
        color:#dff9ee;
        margin-bottom:22px;
        font-size:0.95rem;
        opacity:0.9;
    }

    /* ---- Card ---- */
    div[data-testid="stForm"]{
        background:rgba(255,255,255,0.08);
        border:1px solid rgba(255,255,255,0.25);
        border-radius:22px;
        padding:34px 32px 18px 32px;
        backdrop-filter:blur(12px);
        animation:cardPop .55s cubic-bezier(.2,.8,.3,1) forwards, glowPulse 4s ease-in-out infinite 1s;
    }

    div[data-testid="stForm"] h3{
        color:#ffffff !important;
        text-align:center;
        font-weight:800;
        margin-bottom:18px;
        letter-spacing:0.4px;
    }

    /* ---- Labels ---- */
    div[data-testid="stForm"] label{
        color:#eafff5 !important;
        font-weight:600;
        font-size:0.88rem;
    }

    /* ---- Staggered field entrance ---- */
    @keyframes fieldSlideIn{
        0%{ opacity:0; transform:translateX(-16px); }
        100%{ opacity:1; transform:translateX(0); }
    }
    div[data-testid="stForm"] div[data-testid="stTextInput"]{
        animation:fieldSlideIn .45s ease forwards;
        opacity:0;
    }
    div[data-testid="stForm"] div[data-testid="stTextInput"]:nth-of-type(1){ animation-delay:.10s; }
    div[data-testid="stForm"] div[data-testid="stTextInput"]:nth-of-type(2){ animation-delay:.22s; }
    div[data-testid="stForm"] div[data-testid="stTextInput"]:nth-of-type(3){ animation-delay:.34s; }

    /* ---- Inputs ---- */
    div[data-testid="stForm"] div[data-baseweb="input"]{
        background:rgba(255,255,255,0.94) !important;
        border-radius:12px !important;
        border:2px solid transparent !important;
        transition:border-color .2s ease, box-shadow .2s ease;
        width:100% !important;
        box-sizing:border-box !important;
    }
    div[data-testid="stForm"] div[data-baseweb="input"]:focus-within{
        border-color:#25D366 !important;
        box-shadow:0 0 0 3px rgba(37,211,102,0.25);
    }
    div[data-testid="stForm"] input{
        border-radius:12px !important;
        padding:12px 14px !important;
        font-size:1rem !important;
        color:#075E54 !important;
        font-weight:600;
    }

    /* ---- Fix password show/hide eye icon: force it to the right, vertically centered ---- */
    div[data-testid="stForm"] div[data-baseweb="input"]{
        display:flex;
        align-items:center;
    }
    div[data-testid="stForm"] div[data-baseweb="input"] input{
        flex:1;
        padding-right:6px !important;
    }
    div[data-testid="stForm"] div[data-baseweb="input"] button{
        position:static !important;
        margin-right:8px;
        display:flex;
        align-items:center;
        justify-content:center;
        color:#128C7E !important;
        opacity:0.85;
        transition:opacity .15s ease, transform .15s ease;
    }
    div[data-testid="stForm"] div[data-baseweb="input"] button:hover{
        opacity:1;
        transform:scale(1.15);
    }
    div[data-testid="stForm"] div[data-baseweb="input"] button svg{
        fill:#128C7E !important;
    }

    /* ---- Big professional submit buttons, centered ---- */
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"]{
        width:100% !important;
        display:flex !important;
        justify-content:center !important;
        box-sizing:border-box;
    }
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] [data-testid^="stBaseButton"]{
        position:relative;
        overflow:hidden;
        display:block !important;
        width:70% !important;
        max-width:280px !important;
        min-width:200px !important;
        height:56px !important;
        min-height:56px !important;
        box-sizing:border-box !important;
        background:linear-gradient(90deg,#128C7E,#25D366) !important;
        color:#ffffff !important;
        font-weight:800 !important;
        font-size:1.3rem !important;
        border-radius:14px !important;
        border:none !important;
        padding:0 !important;
        margin-top:14px !important;
        letter-spacing:0.5px;
        box-shadow:0 10px 24px rgba(18,140,126,0.50) !important;
        transition:transform .18s ease, box-shadow .18s ease, background .2s ease;
    }
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button::before,
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] [data-testid^="stBaseButton"]::before{
        content:"";
        position:absolute;
        top:0; left:-120%;
        width:60%; height:100%;
        background:linear-gradient(120deg, transparent, rgba(255,255,255,0.45), transparent);
        transform:skewX(-25deg);
        animation:btnShine 2.6s ease-in-out infinite;
    }
    @keyframes btnShine{
        0%{ left:-120%; }
        45%{ left:130%; }
        100%{ left:130%; }
    }
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button:hover,
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] [data-testid^="stBaseButton"]:hover{
        transform:translateY(-3px) scale(1.02);
        box-shadow:0 14px 30px rgba(37,211,102,0.60) !important;
        background:linear-gradient(90deg,#0e6e63,#1eb356) !important;
    }
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button:active,
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] [data-testid^="stBaseButton"]:active{
        transform:translateY(0) scale(0.98);
    }

    /* ---- Secondary (switch mode) button, centered ---- */
    div[data-testid="stButton"]{
        width:100% !important;
        display:flex !important;
        justify-content:center !important;
    }
    .stButton>button{
        width:70% !important;
        max-width:260px !important;
        min-width:190px !important;
        background:rgba(255,255,255,0.12) !important;
        color:#ffffff !important;
        font-weight:700 !important;
        font-size:1rem !important;
        border-radius:14px !important;
        border:2px solid rgba(255,255,255,0.55) !important;
        padding:13px 0 !important;
        transition:all .2s ease !important;
    }
    .stButton>button:hover{
        background:rgba(255,255,255,0.25) !important;
        border-color:#ffffff !important;
        transform:translateY(-2px);
    }

    .switch-text{
        text-align:center;
        color:#dff9ee;
        margin:16px 0 8px 0;
        font-size:0.9rem;
    }

    .hint-box{
        text-align:center;
        color:#cdeee2;
        font-size:0.78rem;
        margin-top:16px;
        padding:10px;
        border-top:1px solid rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-logo">💬</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">WhatsApp Chat Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Secure login to access your dashboard</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.25, 1])

    with col2:

        if "auth_mode" not in st.session_state:
            st.session_state["auth_mode"] = "login"

        if st.session_state["auth_mode"] == "login":

            with st.form("login_form", clear_on_submit=False):
                st.markdown("### 🔐 Login to your account")
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("🚀 Login")

                if submitted:
                    ok, role = verify_login(username.strip(), password)
                    if ok:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username.strip()
                        st.session_state["role"] = role
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")

            st.markdown('<div class="switch-text">Don\'t have an account yet?</div>', unsafe_allow_html=True)
            if st.button("📝 Create New Account", use_container_width=True):
                st.session_state["auth_mode"] = "register"
                st.rerun()

        else:

            with st.form("register_form", clear_on_submit=False):
                st.markdown("### 📝 Create a new account")
                new_user = st.text_input("👤 Choose a Username", placeholder="Pick a unique username")
                new_pass = st.text_input("🔒 Choose a Password", type="password", placeholder="At least 6 characters")
                confirm_pass = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter your password")
                submitted = st.form_submit_button("✅ Create Account")

                if submitted:
                    if new_pass != confirm_pass:
                        st.error("❌ Passwords do not match")
                    elif len(new_pass) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        ok, msg = register_user(new_user.strip(), new_pass)
                        if ok:
                            st.success(f"✅ {msg}")
                            st.session_state["auth_mode"] = "login"
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

            st.markdown('<div class="switch-text">Already have an account?</div>', unsafe_allow_html=True)
            if st.button("🔐 Back to Login", use_container_width=True):
                st.session_state["auth_mode"] = "login"
                st.rerun()




# ==================================================
# 🔐 CYBERSECURITY HELPER FUNCTIONS
# ==================================================

import difflib

# ---------- PII PATTERNS ---------- #

PII_PATTERNS = {
    "Phone Number": r'(?<!\d)(?:\+91[\-\s]?)?[6-9]\d{9}(?!\d)',
    "Email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    "PAN Card": r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
    "Aadhar Number": r'\b\d{4}\s?\d{4}\s?\d{4}\b',
    "Card Number": r'\b(?:\d[ -]?){13,16}\b'
}

def extract_pii(df):
    """Scan every message for PII patterns. Returns a DataFrame of findings."""
    findings = []
    for _, row in df.iterrows():
        msg = str(row["Message"])
        for label, pattern in PII_PATTERNS.items():
            for match in re.findall(pattern, msg):
                findings.append({
                    "User": row["User"],
                    "Type": label,
                    "Match": match if isinstance(match, str) else "".join(match),
                    "Message": msg
                })
    return pd.DataFrame(findings)


# ---------- PASSWORD / OTP PATTERNS ---------- #

CRED_PATTERNS = {
    "Password": r'(?i)\b(password|pwd|pass)\b\s*[:\-]?\s*\S{3,}',
    "OTP": r'(?i)\botp\b\s*[:\-is]{0,4}\s*\d{4,8}',
    "PIN": r'(?i)\bpin\b\s*[:\-is]{0,4}\s*\d{4,6}',
    "CVV": r'(?i)\bcvv\b\s*[:\-is]{0,4}\s*\d{3,4}'
}

def detect_credentials(df):
    """Flag messages that appear to leak passwords / OTPs / PINs / CVVs."""
    findings = []
    for _, row in df.iterrows():
        msg = str(row["Message"])
        for label, pattern in CRED_PATTERNS.items():
            if re.search(pattern, msg):
                findings.append({
                    "User": row["User"],
                    "Type": label,
                    "Message": msg
                })
    return pd.DataFrame(findings)


# ---------- PHISHING URL ANALYSIS ---------- #

URL_SHORTENERS = [
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd",
    "buff.ly", "adf.ly", "shorturl.at", "cutt.ly", "rebrand.ly",
    "rb.gy", "tiny.cc", "s.id", "v.gd", "lnkd.in"
]

SUSPICIOUS_TLDS = [
    ".xyz", ".top", ".club", ".info", ".work", ".click",
    ".loan", ".win", ".gq", ".tk", ".ml", ".cf", ".ga", ".rest", ".zip"
]

KNOWN_BRANDS = [
    "google", "paypal", "amazon", "facebook", "instagram", "whatsapp",
    "netflix", "apple", "microsoft", "bank", "flipkart", "icici",
    "hdfc", "sbi", "paytm", "gpay", "phonepe", "linkedin", "twitter"
]

def extract_urls(text):
    return re.findall(r'(?:https?://\S+|www\.\S+)', str(text))

def get_domain(url):
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'^www\.', '', url)
    return url.split('/')[0].lower()

def is_typosquat(domain):
    """Very small heuristic: domain looks close to (but not equal to) a known brand."""
    core = domain.split('.')[0]
    for brand in KNOWN_BRANDS:
        if core == brand:
            return False
        ratio = difflib.SequenceMatcher(None, core, brand).ratio()
        if ratio >= 0.75 and core != brand:
            return True
    return False

def analyze_url(url):
    """Return (risk_label, list_of_reasons) for a single URL."""
    reasons = []
    domain = get_domain(url)

    if re.search(r'https?://(\d{1,3}\.){3}\d{1,3}', url):
        reasons.append("IP-based URL")

    if any(short in domain for short in URL_SHORTENERS):
        reasons.append("URL shortener")

    if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS):
        reasons.append("Suspicious TLD")

    if "@" in url:
        reasons.append("'@' used to mask real destination")

    if domain.count('-') >= 3:
        reasons.append("Excessive hyphens in domain")

    if is_typosquat(domain):
        reasons.append("Possible typosquatting (brand look-alike)")

    if len(domain) > 40:
        reasons.append("Unusually long domain")

    if len(reasons) >= 3:
        risk = "🚨 Phishing-Likely"
    elif len(reasons) >= 1:
        risk = "⚠ Suspicious"
    else:
        risk = "✅ Safe"

    return risk, reasons

def analyze_phishing_links(df):
    """Scan all messages, extract URLs, and analyze each one."""
    findings = []
    for _, row in df.iterrows():
        for url in extract_urls(row["Message"]):
            risk, reasons = analyze_url(url)
            findings.append({
                "User": row["User"],
                "URL": url,
                "Risk": risk,
                "Reasons": ", ".join(reasons) if reasons else "-"
            })
    return pd.DataFrame(findings)


# ==================================================
# 🎬 ANIMATED UI HELPER FUNCTIONS (JS Powered)
# ==================================================

def animated_metric_row(metrics, height=150):
    """
    metrics: list of tuples (icon, label, value, color)
    Renders a row of glass cards with JS count-up number animation.
    """
    cards_html = ""
    for icon, label, value, color in metrics:
        try:
            target = float(value)
        except (ValueError, TypeError):
            target = 0
        cards_html += f"""
        <div class="am-card" style="border-top-color:{color};">
            <div class="am-icon">{icon}</div>
            <div class="am-value" data-target="{target}">0</div>
            <div class="am-label">{label}</div>
        </div>
        """

    html = f"""
    <style>
        * {{ box-sizing:border-box; font-family:'Segoe UI',sans-serif; }}
        body {{ margin:0; background:transparent; }}
        .am-row {{
            display:flex;
            gap:14px;
            flex-wrap:wrap;
            justify-content:space-between;
        }}
        .am-card {{
            flex:1;
            min-width:120px;
            background:linear-gradient(160deg,#ffffff,#f2f9f6);
            border-radius:16px;
            border-top:4px solid #25D366;
            padding:16px 12px;
            text-align:center;
            box-shadow:0 6px 16px rgba(7,94,84,0.10);
            opacity:0;
            transform:translateY(18px);
            animation:am-in .6s ease forwards;
        }}
        .am-card:hover{{
            transform:translateY(-4px) scale(1.03);
            box-shadow:0 10px 24px rgba(7,94,84,0.18);
            transition:all .25s ease;
        }}
        @keyframes am-in {{
            to {{ opacity:1; transform:translateY(0); }}
        }}
        .am-icon{{ font-size:1.6rem; margin-bottom:4px; }}
        .am-value{{
            font-size:1.9rem;
            font-weight:800;
            color:#075E54;
        }}
        .am-label{{
            font-size:0.82rem;
            color:#557b74;
            font-weight:600;
            margin-top:2px;
        }}
    </style>
    <div class="am-row">
        {cards_html}
    </div>
    <script>
        const els = document.querySelectorAll('.am-value');
        els.forEach((el, i) => {{
            const target = parseFloat(el.getAttribute('data-target'));
            const isFloat = !Number.isInteger(target);
            let current = 0;
            const steps = 40;
            const inc = target / steps;
            let count = 0;
            const timer = setInterval(() => {{
                count++;
                current += inc;
                if (count >= steps) {{
                    current = target;
                    clearInterval(timer);
                }}
                el.textContent = isFloat ? current.toFixed(2) : Math.round(current).toLocaleString();
            }}, 18);
        }});
    </script>
    """
    components.html(html, height=height)


def animated_gauge(score, label="Risk Score", height=300):
    """
    Renders an animated circular gauge (0-100) using SVG + JS.
    Lower score = greener, higher score = redder.
    """
    if score < 15:
        color = "#25D366"
    elif score < 40:
        color = "#f1c40f"
    elif score < 70:
        color = "#e67e22"
    else:
        color = "#e74c3c"

    radius = 80
    circumference = 2 * 3.14159265 * radius

    html = f"""
    <style>
        body {{ margin:0; background:transparent; font-family:'Segoe UI',sans-serif; }}
        .gauge-wrap {{
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
        }}
        .gauge-value {{
            font-size:2.4rem;
            font-weight:800;
            fill:{color};
        }}
        .gauge-label {{
            margin-top:6px;
            font-size:1rem;
            font-weight:600;
            color:#075E54;
        }}
        circle.bg {{
            fill:none;
            stroke:#e8f3ef;
            stroke-width:14;
        }}
        circle.fg {{
            fill:none;
            stroke:{color};
            stroke-width:14;
            stroke-linecap:round;
            stroke-dasharray:{circumference};
            stroke-dashoffset:{circumference};
            transform:rotate(-90deg);
            transform-origin:100px 100px;
            transition:stroke-dashoffset 1.4s cubic-bezier(.25,1,.35,1);
        }}
    </style>
    <div class="gauge-wrap">
        <svg width="200" height="200" viewBox="0 0 200 200">
            <circle class="bg" cx="100" cy="100" r="{radius}"></circle>
            <circle class="fg" id="fgCircle" cx="100" cy="100" r="{radius}"></circle>
            <text x="100" y="108" text-anchor="middle" class="gauge-value" id="gaugeText">0</text>
        </svg>
        <div class="gauge-label">{label}</div>
    </div>
    <script>
        const circumference = {circumference};
        const target = {score};
        const circle = document.getElementById('fgCircle');
        const text = document.getElementById('gaugeText');
        setTimeout(() => {{
            const offset = circumference - (target / 100) * circumference;
            circle.style.strokeDashoffset = offset;
        }}, 100);

        let current = 0;
        const steps = 45;
        const inc = target / steps;
        let count = 0;
        const timer = setInterval(() => {{
            count++;
            current += inc;
            if (count >= steps) {{
                current = target;
                clearInterval(timer);
            }}
            text.textContent = Math.round(current);
        }}, 22);
    </script>
    """
    components.html(html, height=height)


def typewriter_hero(title, subtitle, height=170):
    """Animated gradient-wave hero banner with a JS typewriter subtitle."""
    html = f"""
    <style>
        body {{ margin:0; background:transparent; font-family:'Segoe UI',sans-serif; overflow:hidden; }}
        .hero {{
            position:relative;
            border-radius:18px;
            padding:28px 20px;
            text-align:center;
            background:linear-gradient(120deg,#075E54,#128C7E,#25D366,#128C7E,#075E54);
            background-size:300% 300%;
            animation:gradientMove 8s ease infinite;
            box-shadow:0 10px 26px rgba(7,94,84,0.30);
            overflow:hidden;
        }}
        @keyframes gradientMove {{
            0% {{ background-position:0% 50%; }}
            50% {{ background-position:100% 50%; }}
            100% {{ background-position:0% 50%; }}
        }}
        .hero h1 {{
            color:#ffffff;
            margin:0;
            font-size:2.2rem;
            font-weight:800;
            letter-spacing:0.5px;
            text-shadow:0 2px 8px rgba(0,0,0,0.15);
        }}
        .hero p#typed {{
            color:#e8fff5;
            margin-top:10px;
            font-size:1rem;
            min-height:22px;
            font-weight:500;
        }}
        .cursor {{
            display:inline-block;
            width:2px;
            background:#e8fff5;
            margin-left:2px;
            animation:blink 0.8s steps(2) infinite;
        }}
        @keyframes blink {{ 50% {{ opacity:0; }} }}
        .bubble {{
            position:absolute;
            bottom:-40px;
            border-radius:50%;
            background:rgba(255,255,255,0.15);
            animation:rise linear infinite;
        }}
        @keyframes rise {{
            0% {{ transform:translateY(0) scale(1); opacity:0.6; }}
            100% {{ transform:translateY(-180px) scale(1.4); opacity:0; }}
        }}
    </style>
    <div class="hero" id="heroBox">
        <h1>{title}</h1>
        <p id="typed"><span id="typedText"></span><span class="cursor">&nbsp;</span></p>
    </div>
    <script>
        const text = {subtitle!r};
        const el = document.getElementById('typedText');
        let idx = 0;
        function type() {{
            if (idx <= text.length) {{
                el.textContent = text.slice(0, idx);
                idx++;
                setTimeout(type, 35);
            }} else {{
                setTimeout(() => {{ idx = 0; type(); }}, 2200);
            }}
        }}
        type();

        const hero = document.getElementById('heroBox');
        for (let i=0; i<10; i++) {{
            const b = document.createElement('div');
            b.className = 'bubble';
            const size = 6 + Math.random()*14;
            b.style.width = size+'px';
            b.style.height = size+'px';
            b.style.left = (Math.random()*100)+'%';
            b.style.animationDuration = (4 + Math.random()*5)+'s';
            b.style.animationDelay = (Math.random()*5)+'s';
            hero.appendChild(b);
        }}
    </script>
    """
    components.html(html, height=height)


def speech_widget(default_text="", key="tts", height=185):
    """
    Multilingual text-to-speech helper (English / Gujarati / Hindi).

    Uses gTTS (Google Text-to-Speech) to generate real, natural-sounding
    speech server-side instead of relying on the browser's built-in voice
    engine — most browsers/OSes don't ship a proper Gujarati voice, so this
    gives accurate pronunciation for Gujarati and Hindi too. Requires
    internet access on the machine running this app.
    """

    from gtts import gTTS
    from io import BytesIO

    LANG_MAP = {
        "🇬🇧 English": "en",
        "🇮🇳 ગુજરાતી (Gujarati)": "gu",
        "🇮🇳 हिन्दी (Hindi)": "hi",
    }

    st.markdown("#### 🔊 Voice Assistant — Listen in your language")

    text = st.text_area(
        "Text to read aloud",
        value=default_text,
        height=90,
        key=f"{key}_text",
        placeholder="Type or paste anything here — a message, a summary, an explanation..."
    )

    lang_choice = st.selectbox(
        "🌐 Choose language",
        list(LANG_MAP.keys()),
        key=f"{key}_lang"
    )
    lang_code = LANG_MAP[lang_choice]

    if st.button("🔊 Generate & Speak", key=f"{key}_btn", use_container_width=True):

        if not text or not text.strip():
            st.warning("⚠ Please type some text first.")
        else:
            try:
                with st.spinner("🎙 Generating natural voice..."):
                    tts = gTTS(text=text.strip(), lang=lang_code, slow=False)
                    audio_buffer = BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    audio_bytes = audio_buffer.getvalue()

                st.audio(audio_bytes, format="audio/mp3")
                st.success(f"✅ Ready — spoken in {lang_choice}")

                st.download_button(
                    "⬇ Download Audio (MP3)",
                    audio_bytes,
                    file_name=f"voice_{lang_code}.mp3",
                    mime="audio/mp3",
                    key=f"{key}_download"
                )

            except Exception as e:
                st.error(
                    "⚠ Couldn't generate speech. This feature needs an active internet "
                    f"connection on the machine running the app. ({e})"
                )


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOGIN GATE ---------------- #
# The whole app below only renders once the user is authenticated.

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    show_login_register_page()
    st.stop()

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

/* ---------- Global ---------- */

.main{
    background:linear-gradient(180deg,#f4f7f6 0%,#eef2f1 100%);
}

.block-container{
    padding-top:1.5rem;
    padding-bottom:3rem;
}

h1{
    background:linear-gradient(90deg,#128C7E,#25D366);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    text-align:center;
    font-weight:800;
    font-size:2.6rem;
}

h2, h3{
    color:#075E54;
}

/* ---------- Header banner ---------- */

.app-banner{
    background:linear-gradient(90deg,#075E54,#128C7E,#25D366);
    padding:22px 28px;
    border-radius:16px;
    margin-bottom:18px;
    box-shadow:0 6px 18px rgba(7,94,84,0.25);
}

.app-banner h1{
    -webkit-text-fill-color:#ffffff !important;
    background:none !important;
    margin:0;
    font-size:2.1rem;
}

.app-banner p{
    color:#e8fff5;
    text-align:center;
    margin:4px 0 0 0;
    font-size:0.95rem;
}

/* ---------- Cards ---------- */

@keyframes cardFadeInUp{
    from{ opacity:0; transform:translateY(22px); }
    to{ opacity:1; transform:translateY(0); }
}

.feature-card{
    background:#ffffff;
    border-radius:14px;
    padding:18px 20px;
    box-shadow:0 4px 14px rgba(0,0,0,0.06);
    border-left:5px solid #25D366;
    margin-bottom:14px;
    opacity:0;
    animation:cardFadeInUp .55s ease forwards;
    transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}

.feature-card:hover{
    transform:translateY(-5px) scale(1.015);
    box-shadow:0 12px 26px rgba(7,94,84,0.15);
    border-left:5px solid #075E54;
}

.feature-card h4{
    margin:0 0 6px 0;
    color:#075E54;
    transition:color .2s ease;
}

.feature-card:hover h4{
    color:#25D366;
}

.feature-card p{
    margin:0;
    color:#4a4a4a;
    font-size:0.9rem;
}

/* ---------- Metric containers ---------- */

div[data-testid="stMetric"]{
    background:#ffffff;
    border-radius:14px;
    padding:16px 10px;
    box-shadow:0 4px 12px rgba(0,0,0,0.06);
    border-top:4px solid #25D366;
}

div[data-testid="stMetricLabel"]{
    font-weight:600;
    color:#075E54;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#075E54 0%,#128C7E 100%);
}

section[data-testid="stSidebar"] *{
    color:#ffffff !important;
}

section[data-testid="stSidebar"] .stRadio > label{
    font-weight:600;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label{
    background:rgba(255,255,255,0.08);
    border-radius:10px;
    padding:8px 10px;
    margin-bottom:6px;
    transition:background .15s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
    background:rgba(255,255,255,0.20);
}

/* ---------- Dataframe / table polish ---------- */

.stDataFrame{
    border-radius:12px;
    overflow:hidden;
}

/* ---------- Buttons ---------- */

.stButton>button, .stDownloadButton>button{
    background:linear-gradient(90deg,#128C7E,#25D366);
    color:white;
    border:none;
    border-radius:10px;
    padding:8px 18px;
    font-weight:600;
}

.stButton>button:hover, .stDownloadButton>button:hover{
    background:linear-gradient(90deg,#0e6e63,#1eb356);
    color:white;
}

/* ---------- Footer ---------- */

.app-footer{
    text-align:center;
    color:#888;
    padding-top:20px;
    font-size:0.85rem;
}

</style>
""",unsafe_allow_html=True)

# ---------------- HEADER BANNER (animated) ---------------- #

typewriter_hero(
    "💬 WhatsApp Chat Analyzer",
    "AI, ML & Cybersecurity powered chat insights — upload and explore instantly",
    height=175
)

# ---------------- SIDEBAR ---------------- #

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg",
    width=70
)

st.sidebar.title("📌 Navigation")

menu_options = [
    "🏠 Home",
    "📂 Upload Chat",
    "📊 Dashboard",
    "👥 Active Users",
    "📅 Timeline",
    "☁️ WordCloud",
    "😊 Emoji Analysis",
    "😊 Emotion Detection",
    "🚨 Spam Detection",
    "🔗 Link Analysis",
    "❤️ Sentiment Analysis",
    "🛡 Fake Link Detection",
    "🕵️ PII Leak Detector",
    "🔑 Password/OTP Leak Detector",
    "🎣 Phishing URL Analyzer",
    "⚠️ Chat Risk Score",
    "🤖 AI Chat Summary",
    "📄 Export Report",
    "🌐 Language Detection",
    "🔍 Search",
    "🔊 Voice Assistant",
    "🤖 AI Chat Assistant",
    "ℹ About"
]

if st.session_state.get("role") == "admin":
    menu_options.insert(1, "🛠 Admin Panel")

menu = st.sidebar.radio(
    "",
    menu_options
)

st.sidebar.markdown("---")
if "chat" in st.session_state:
    st.sidebar.success("✅ Chat file loaded")
else:
    st.sidebar.warning("⚠ No chat uploaded yet")

st.sidebar.markdown("---")
role_badge = "👑 Admin" if st.session_state.get("role") == "admin" else "👤 User"
st.sidebar.markdown(f"**{role_badge}**")
st.sidebar.markdown(f"Logged in as: **{st.session_state.get('username','')}**")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    for key in ["logged_in", "username", "role", "auth_mode"]:
        st.session_state.pop(key, None)
    st.rerun()

# ---------------- HOME ---------------- #

if menu=="🏠 Home":

    st.header("Welcome 👋")

    st.write("Analyze your exported WhatsApp chat with a complete set of AI-powered tools. Explore the full feature set below:")

    st.markdown("<br>", unsafe_allow_html=True)

    features = [
        ("📂", "Upload Chat File", "Upload your exported .txt WhatsApp chat and parse it instantly."),
        ("📊", "Dashboard", "Overview of messages, users, words, media and links at a glance."),
        ("👥", "Active Users", "See who talks the most with charts and rankings."),
        ("📅", "Timeline", "Daily, weekly, monthly trends plus an activity heatmap."),
        ("☁️", "WordCloud", "Visualize the most frequently used words in the chat."),
        ("😊", "Emoji Analysis", "Top emojis used, with counts and distribution charts."),
        ("😊", "Emotion Detection", "Detect Happy, Sad, Angry, Surprise & Fear tones in messages."),
        ("🚨", "Spam Detection", "Flag spam and suspicious messages using keyword scoring."),
        ("🔗", "Link Analysis", "List and count all links shared in the chat."),
        ("❤️", "Sentiment Analysis", "Classify messages as Positive, Negative or Neutral."),
        ("🛡", "Fake Link Detection", "Detect dangerous / suspicious links shared in chat."),
        ("🕵️", "PII Leak Detector", "Scan chat for exposed phone numbers, emails, PAN, Aadhar & card numbers."),
        ("🔑", "Password/OTP Leak Detector", "Catch passwords, PINs and OTPs shared in plain text before it's a breach."),
        ("🎣", "Phishing URL Analyzer", "Deep-scan links for shorteners, IP-based URLs, typosquatting & suspicious TLDs."),
        ("⚠️", "Chat Risk Score", "One combined cybersecurity risk score for the whole chat, with a breakdown."),
        ("🤖", "AI Chat Summary", "Auto-generated summary: most active user, ghost user, busiest day & more."),
        ("📄", "Export Report", "Download the analyzed chat as CSV or Excel."),
        ("🌐", "Language Detection", "Detect the language used in each message."),
        ("🔍", "Search", "Search messages by keyword instantly."),
        ("🔊", "Voice Assistant", "Listen to any text aloud in English, Gujarati or Hindi with a real natural voice."),
        ("🤖", "AI Chat Assistant", "Chat with your uploaded report — ask questions in plain English and get instant answers."),
    ]

    cols = st.columns(2)

    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 2]:
            delay = (i % 8) * 0.06
            st.markdown(f"""
            <div class="feature-card" style="animation-delay:{delay}s;">
                <h4>{icon} {title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.success("Developed by Zalak Chudasama")

# ==============================
# ADMIN PANEL
# ==============================

elif menu == "🛠 Admin Panel":

    if st.session_state.get("role") != "admin":
        st.error("🚫 You are not authorized to view this page.")
    else:

        st.header("🛠 Admin Panel")
        st.caption("Manage registered users of this application.")

        users = load_users()

        total_users = len(users)
        admin_count = sum(1 for u in users.values() if u.get("role") == "admin")
        normal_count = total_users - admin_count

        animated_metric_row([
            ("👥", "Total Users", total_users, "#25D366"),
            ("👑", "Admins", admin_count, "#128C7E"),
            ("🙋", "Regular Users", normal_count, "#075E54"),
        ])

        st.markdown("---")

        st.subheader("📋 Registered Users")

        users_df = pd.DataFrame([
            {
                "Username": uname,
                "Role": info.get("role", "user"),
                "Created": info.get("created", "-")
            }
            for uname, info in users.items()
        ])

        st.dataframe(users_df, use_container_width=True)

        st.markdown("---")

        st.subheader("➕ Create a New User")

        with st.form("admin_create_user"):
            c1, c2, c3 = st.columns([1, 1, 0.6])
            new_username = c1.text_input("Username")
            new_password = c2.text_input("Password", type="password")
            new_role = c3.selectbox("Role", ["user", "admin"])
            create_submit = st.form_submit_button("Create User")

            if create_submit:
                if new_username.strip() in users:
                    st.error("❌ Username already exists")
                elif not new_username.strip() or not new_password:
                    st.error("❌ Username and password are required")
                else:
                    users[new_username.strip()] = {
                        "password": hash_password(new_password),
                        "role": new_role,
                        "created": str(datetime.now())
                    }
                    save_users(users)
                    st.success(f"✅ User '{new_username.strip()}' created")
                    st.rerun()

        st.markdown("---")

        st.subheader("🗑 Remove a User")

        removable_users = [u for u in users.keys() if u != st.session_state.get("username")]

        if len(removable_users) == 0:
            st.info("No other users to remove.")
        else:
            col1, col2 = st.columns([2, 1])
            with col1:
                user_to_remove = st.selectbox("Select user to remove", removable_users)
            with col2:
                st.write("")
                st.write("")
                if st.button("🗑 Delete User", use_container_width=True):
                    users.pop(user_to_remove, None)
                    save_users(users)
                    st.success(f"✅ User '{user_to_remove}' removed")
                    st.rerun()

# ==============================
# UPLOAD CHAT
# ==============================

elif menu == "📂 Upload Chat":

    st.header("📂 Upload WhatsApp Chat")

    uploaded_file = st.file_uploader(
        "Choose exported WhatsApp .txt file",
        type=["txt"]
    )

    if uploaded_file is not None:

        raw_data = uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

        # ---------------- REGEX ---------------- #

        pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}(?:\s?[APap][Mm])?)\s-\s([^:]+):\s(.*)"

        messages = []

        for line in raw_data.split("\n"):

            match = re.match(pattern, line)

            if match:

                date = match.group(1)
                time = match.group(2)
                user = match.group(3)
                message = match.group(4)

                messages.append(
                    [date, time, user, message]
                )

        if len(messages) == 0:

            st.error(
                "No messages found.\n\nPlease export WhatsApp chat WITHOUT MEDIA."
            )

        else:

            df = pd.DataFrame(
                messages,
                columns=[
                    "Date",
                    "Time",
                    "User",
                    "Message"
                ]
            )

            # ---------------- DATE ---------------- #

            df["Date"] = pd.to_datetime(
                df["Date"],
                dayfirst=True,
                errors="coerce"
            )

            df.dropna(inplace=True)

            df["Year"] = df["Date"].dt.year
            df["Month"] = df["Date"].dt.month_name()
            df["Day"] = df["Date"].dt.day_name()
            df["Month_num"] = df["Date"].dt.month
            df["Hour"] = df["Time"].astype(str).str[:2]

            # ---------------- MESSAGE LENGTH ---------------- #

            df["Characters"] = df["Message"].apply(len)

            df["Words"] = df["Message"].apply(
                lambda x: len(str(x).split())
            )

            # ---------------- MEDIA ---------------- #

            df["Media"] = df["Message"].str.contains(
                "<Media omitted>",
                case=False,
                na=False
            )

            # ---------------- LINKS ---------------- #

            df["Has_Link"] = df["Message"].str.contains(
                r"http|https|www",
                regex=True,
                case=False,
                na=False
            )

            st.session_state["chat"] = df

            st.success("✅ Chat Loaded Successfully")

            st.subheader("Preview")

            st.dataframe(df.head(20), use_container_width=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("Rows", len(df))
            c2.metric("Users", df["User"].nunique())
            c3.metric("Messages", len(df))
            # ==============================
# DASHBOARD
# ==============================

elif menu == "📊 Dashboard":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload WhatsApp chat first.")
    else:

        df = st.session_state["chat"]

        total_messages = len(df)
        total_users = df["User"].nunique()
        total_words = df["Words"].sum()
        total_characters = df["Characters"].sum()
        media_count = df["Media"].sum()
        link_count = df["Has_Link"].sum()

        avg_words = round(total_words / total_messages, 2)
        avg_characters = round(total_characters / total_messages, 2)

        st.header("📊 Dashboard")

        animated_metric_row([
            ("💬", "Messages", total_messages, "#25D366"),
            ("👥", "Users", total_users, "#128C7E"),
            ("📝", "Words", total_words, "#075E54"),
            ("📷", "Media", media_count, "#34b7a4"),
        ])

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        animated_metric_row([
            ("🔗", "Links", link_count, "#25D366"),
            ("📖", "Avg Words", avg_words, "#128C7E"),
            ("🔤", "Avg Characters", avg_characters, "#075E54"),
        ])

        st.markdown("---")

        st.subheader("👥 Top Active Users")

        user_count = df["User"].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(10,5))

        ax.bar(user_count.index,
               user_count.values,
               color="#25D366")

        plt.xticks(rotation=30)
        plt.ylabel("Messages")
        plt.xlabel("Users")

        st.pyplot(fig)

        st.markdown("---")

        st.subheader("📅 Monthly Messages")

        monthly = df.groupby("Month_num").size()

        fig2, ax2 = plt.subplots(figsize=(10,5))

        ax2.plot(
            monthly.index,
            monthly.values,
            marker="o",
            linewidth=3,
            color="#128C7E"
        )

        plt.xlabel("Month")
        plt.ylabel("Messages")

        st.pyplot(fig2)

        st.markdown("---")

        st.subheader("📜 Recent Messages")

        st.dataframe(
            df.tail(20),
            use_container_width=True
        )
        # ==============================
# ACTIVE USERS
# ==============================

elif menu == "👥 Active Users":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload WhatsApp chat first.")
    else:

        df = st.session_state["chat"]

        st.header("👥 Active Users Analysis")

        user_count = df["User"].value_counts()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Top 10 Users")

            st.dataframe(
                user_count.head(10).reset_index().rename(
                    columns={
                        "index":"User",
                        "User":"Messages"
                    }
                ),
                use_container_width=True
            )

        with col2:

            fig, ax = plt.subplots(figsize=(6,6))

            ax.pie(
                user_count.head(10),
                labels=user_count.head(10).index,
                autopct="%1.1f%%",
                startangle=90
            )

            plt.title("Top Active Users")

            st.pyplot(fig)

        st.markdown("---")

        fig2, ax2 = plt.subplots(figsize=(10,5))

        ax2.bar(
            user_count.head(10).index,
            user_count.head(10).values,
            color="#128C7E"
        )

        plt.xticks(rotation=25)
        plt.xlabel("Users")
        plt.ylabel("Messages")

        st.pyplot(fig2)


# ==============================
# TIMELINE
# ==============================

elif menu == "📅 Timeline":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload WhatsApp chat first.")
    else:

        df = st.session_state["chat"]

        st.header("📅 Timeline Analysis")

        st.subheader("Daily Timeline")

        daily = df.groupby("Date").size()

        fig, ax = plt.subplots(figsize=(12,5))

        ax.plot(
            daily.index,
            daily.values,
            marker="o",
            linewidth=2,
            color="#25D366"
        )

        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Messages")

        st.pyplot(fig)

        st.markdown("---")

        st.subheader("Weekly Activity")

        week = df["Day"].value_counts()

        fig2, ax2 = plt.subplots(figsize=(10,5))

        ax2.bar(
            week.index,
            week.values,
            color="#128C7E"
        )

        plt.xticks(rotation=30)

        st.pyplot(fig2)

        st.markdown("---")

        st.subheader("Monthly Activity")

        month = df["Month"].value_counts()

        fig3, ax3 = plt.subplots(figsize=(10,5))

        ax3.bar(
            month.index,
            month.values,
            color="#075E54"
        )

        plt.xticks(rotation=45)

        st.pyplot(fig3)

        st.markdown("---")

        st.subheader("Activity Heatmap")

        heatmap = pd.crosstab(
            df["Day"],
            df["Hour"]
        )

        fig4, ax4 = plt.subplots(figsize=(14,5))

        sns.heatmap(
            heatmap,
            cmap="YlGnBu",
            ax=ax4
        )

        st.pyplot(fig4)
        # ==============================
# WORD CLOUD
# ==============================

elif menu == "☁️ WordCloud":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload WhatsApp chat first.")
    else:

        df = st.session_state["chat"]

        st.header("☁️ Word Cloud")

        text = " ".join(df["Message"].astype(str))

        wc = WordCloud(
            width=1200,
            height=600,
            background_color="white",
            colormap="viridis"
        ).generate(text)

        fig, ax = plt.subplots(figsize=(14,7))

        ax.imshow(wc)
        ax.axis("off")

        st.pyplot(fig)

        st.markdown("---")

        st.subheader("Top 20 Most Used Words")

        words = Counter(text.lower().split()).most_common(20)

        word_df = pd.DataFrame(
            words,
            columns=["Word","Count"]
        )

        st.dataframe(
            word_df,
            use_container_width=True
        )

        fig2, ax2 = plt.subplots(figsize=(10,5))

        ax2.bar(
            word_df["Word"],
            word_df["Count"],
            color="#25D366"
        )

        plt.xticks(rotation=45)

        st.pyplot(fig2)


# ==============================
# EMOJI ANALYSIS
# ==============================

elif menu == "😊 Emoji Analysis":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload WhatsApp chat first.")
    else:

        df = st.session_state["chat"]

        st.header("😊 Emoji Analysis")

        emojis = []

        for msg in df["Message"]:

            for ch in str(msg):

                if ch in emoji.EMOJI_DATA:
                    emojis.append(ch)

        if len(emojis)==0:

            st.info("No emojis found.")

        else:

            emoji_count = Counter(emojis).most_common(15)

            emoji_df = pd.DataFrame(
                emoji_count,
                columns=[
                    "Emoji",
                    "Count"
                ]
            )

            st.dataframe(
                emoji_df,
                use_container_width=True
            )

            fig, ax = plt.subplots(figsize=(8,5))

            ax.bar(
                emoji_df["Emoji"],
                emoji_df["Count"],
                color="#128C7E"
            )

            plt.title("Top Emojis")

            st.pyplot(fig)

            fig2, ax2 = plt.subplots(figsize=(6,6))

            ax2.pie(
                emoji_df["Count"],
                labels=emoji_df["Emoji"],
                autopct="%1.1f%%"
            )

            st.pyplot(fig2)
            # ==============================
# LINK ANALYSIS
# ==============================
# ==============================
# SPAM DETECTION
# ==============================
# ==============================
# EMOTION DETECTION
# ==============================

elif menu == "😊 Emotion Detection":

    if "chat" not in st.session_state:
        st.warning("Please upload chat first.")

    else:

        df = st.session_state["chat"]

        happy = [
            "happy","great","good","awesome","love",
            "excellent","nice","wow","super","😊","😁","😂","😍","🥳","❤️"
        ]

        sad = [
            "sad","cry","miss","alone","hurt",
            "pain","😭","😢","☹","😔"
        ]

        angry = [
            "angry","hate","idiot","stupid",
            "worst","bad","😡","🤬","👿"
        ]

        surprise = [
            "wow","omg","really","seriously",
            "😲","😮","😱"
        ]

        fear = [
            "fear","afraid","danger","scared",
            "😨","😰"
        ]

        def detect_emotion(msg):

            msg = str(msg).lower()

            if any(word in msg for word in happy):
                return "😊 Happy"

            elif any(word in msg for word in sad):
                return "😢 Sad"

            elif any(word in msg for word in angry):
                return "😡 Angry"

            elif any(word in msg for word in surprise):
                return "😲 Surprise"

            elif any(word in msg for word in fear):
                return "😨 Fear"

            else:
                return "😐 Neutral"

        df["Emotion"] = df["Message"].apply(detect_emotion)

        st.header("😊 Emotion Detection")

        st.dataframe(
            df[
                ["User","Message","Emotion"]
            ],
            use_container_width=True
        )

        emotion = df["Emotion"].value_counts()

        st.subheader("Emotion Summary")

        col1,col2 = st.columns(2)

        with col1:

            st.dataframe(
                emotion.reset_index().rename(
                    columns={
                        "index":"Emotion",
                        "Emotion":"Count"
                    }
                )
            )

        with col2:

            fig,ax=plt.subplots(figsize=(6,6))

            ax.pie(
                emotion.values,
                labels=emotion.index,
                autopct="%1.1f%%",
                startangle=90
            )

            plt.title("Emotion Distribution")

            st.pyplot(fig)

elif menu == "🚨 Spam Detection":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload WhatsApp chat first.")
    else:

        df = st.session_state["chat"]

        st.header("🚨 AI Spam Message Detection")

        spam_keywords = [
            "win","winner","lottery","free","click",
            "offer","prize","gift","urgent","otp",
            "verify","password","bank","credit card",
            "loan","investment","bitcoin","earn money",
            "limited offer","congratulations",
            "cash","reward","bonus","claim now"
        ]

        def detect_spam(message):

            message = str(message).lower()

            score = 0

            for word in spam_keywords:
                if word in message:
                    score += 1

            if score >= 2:
                return "🚨 Spam"

            elif score == 1:
                return "⚠ Suspicious"

            else:
                return "✅ Safe"

        df["Spam Status"] = df["Message"].apply(detect_spam)

        st.subheader("Spam Detection Result")

        st.dataframe(
            df[["User","Message","Spam Status"]],
            use_container_width=True
        )

        st.markdown("---")

        spam = df["Spam Status"].value_counts()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Spam Summary")

            st.write(spam)

        with col2:

            fig, ax = plt.subplots(figsize=(6,6))

            ax.pie(
                spam.values,
                labels=spam.index,
                autopct="%1.1f%%",
                startangle=90
            )

            plt.title("Spam Distribution")

            st.pyplot(fig)

        st.markdown("---")

        st.subheader("Only Spam Messages")

        spam_df = df[df["Spam Status"]=="🚨 Spam"]

        if len(spam_df)==0:

            st.success("🎉 No Spam Messages Found")

        else:

            st.dataframe(
                spam_df,
                use_container_width=True
            )

elif menu == "🔗 Link Analysis":

    if "chat" not in st.session_state:
        st.warning("Please upload chat first.")
    else:

        df = st.session_state["chat"]

        st.header("🔗 Link Analysis")

        links = df[df["Has_Link"] == True]

        st.metric("Total Links Shared", len(links))

        if len(links) > 0:

            st.dataframe(
                links[
                    ["User", "Message"]
                ],
                use_container_width=True
            )

        else:

            st.info("No links found.")


# ==============================
# SENTIMENT ANALYSIS
# ==============================

elif menu == "❤️ Sentiment Analysis":

    from textblob import TextBlob

    if "chat" not in st.session_state:
        st.warning("Please upload chat first.")
    else:

        df = st.session_state["chat"]

        st.header("❤️ Sentiment Analysis")

        def sentiment(text):

            score = TextBlob(str(text)).sentiment.polarity

            if score > 0:
                return "Positive"

            elif score < 0:
                return "Negative"

            else:
                return "Neutral"

        df["Sentiment"] = df["Message"].apply(sentiment)

        st.dataframe(
            df[
                ["User", "Message", "Sentiment"]
            ].head(25),
            use_container_width=True
        )

        sentiment_count = df["Sentiment"].value_counts()

        fig, ax = plt.subplots(figsize=(6,6))

        ax.pie(
            sentiment_count,
            labels=sentiment_count.index,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Sentiment Distribution")

        st.pyplot(fig)
        # ==============================
# FAKE LINK DETECTION
# ==============================

elif menu == "🛡 Fake Link Detection":

    if "chat" not in st.session_state:
        st.warning("Please upload chat first.")

    else:

        df = st.session_state["chat"]

        suspicious_keywords = [
            "bit.ly",
            "tinyurl",
            "shorturl",
            "rebrand.ly",
            "grabify",
            "freegift",
            "claim",
            "verify",
            "otp",
            "bank",
            "password",
            "click",
            "login",
            "update account",
            "gift",
            "winner",
            "lottery",
            "bonus",
            "reward",
            "bitcoin"
        ]

        def check_link(msg):

            msg = str(msg).lower()

            if "http" not in msg and "www" not in msg:
                return "No Link"

            score = 0

            for word in suspicious_keywords:

                if word in msg:
                    score += 1

            if score >= 3:
                return "🚨 Dangerous"

            elif score >= 1:
                return "⚠ Suspicious"

            else:
                return "✅ Safe Link"

        df["Link Status"] = df["Message"].apply(check_link)

        st.header("🛡 Fake Link Detection")

        st.dataframe(
            df[
                ["User",
                 "Message",
                 "Link Status"]
            ],
            use_container_width=True
        )

        st.markdown("---")

        status = df["Link Status"].value_counts()

        col1,col2 = st.columns(2)

        with col1:

            st.subheader("Summary")

            st.dataframe(
                status.reset_index().rename(
                    columns={
                        "index":"Status",
                        "Link Status":"Count"
                    }
                )
            )

        with col2:

            fig,ax=plt.subplots(figsize=(6,6))

            ax.pie(
                status.values,
                labels=status.index,
                autopct="%1.1f%%",
                startangle=90
            )

            plt.title("Link Analysis")

            st.pyplot(fig)

        st.markdown("---")

        st.subheader("Dangerous Links")

        danger = df[df["Link Status"]=="🚨 Dangerous"]

        if len(danger)==0:

            st.success("No dangerous links found.")

        else:

            st.dataframe(
                danger,
                use_container_width=True
            )
            # ==============================
# PII LEAK DETECTOR
# ==============================

elif menu == "🕵️ PII Leak Detector":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload WhatsApp chat first.")

    else:

        df = st.session_state["chat"]

        st.header("🕵️ PII (Personal Data) Leak Detector")

        st.caption(
            "Scans every message for phone numbers, emails, PAN, Aadhar and "
            "card-like numbers that were shared in plain text."
        )

        pii_df = extract_pii(df)

        if len(pii_df) == 0:

            st.success("🎉 No obvious PII leaks found in this chat.")

        else:

            c1, c2, c3 = st.columns(3)

            c1.metric("Total PII Hits", len(pii_df))
            c2.metric("Users Affected", pii_df["User"].nunique())
            c3.metric("PII Types Found", pii_df["Type"].nunique())

            st.markdown("---")

            st.subheader("Breakdown by Type")

            type_count = pii_df["Type"].value_counts()

            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(
                    type_count.reset_index().rename(
                        columns={"index": "Type", "Type": "Count"}
                    ),
                    use_container_width=True
                )

            with col2:
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie(
                    type_count.values,
                    labels=type_count.index,
                    autopct="%1.1f%%",
                    startangle=90
                )
                plt.title("PII Type Distribution")
                st.pyplot(fig)

            st.markdown("---")

            st.subheader("Detected PII (masked preview)")

            preview = pii_df.copy()

            def mask(val):
                val = str(val)
                if len(val) <= 4:
                    return "*" * len(val)
                return val[:2] + "*" * (len(val) - 4) + val[-2:]

            preview["Match"] = preview["Match"].apply(mask)

            st.dataframe(
                preview[["User", "Type", "Match", "Message"]],
                use_container_width=True
            )

            st.warning(
                "⚠ Avoid sharing phone numbers, card numbers, PAN or Aadhar "
                "details over chat. This data can be misused if the chat export leaks."
            )


# ==============================
# PASSWORD / OTP LEAK DETECTOR
# ==============================

elif menu == "🔑 Password/OTP Leak Detector":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload WhatsApp chat first.")

    else:

        df = st.session_state["chat"]

        st.header("🔑 Password / OTP / PIN Leak Detector")

        st.caption(
            "Flags messages that mention passwords, OTPs, PINs or CVVs in plain text — "
            "a common cause of account takeovers."
        )

        cred_df = detect_credentials(df)

        if len(cred_df) == 0:

            st.success("🎉 No password/OTP/PIN/CVV leaks detected.")

        else:

            c1, c2 = st.columns(2)

            c1.metric("Total Leaks Found", len(cred_df))
            c2.metric("Users Involved", cred_df["User"].nunique())

            st.markdown("---")

            type_count = cred_df["Type"].value_counts()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Summary")
                st.dataframe(
                    type_count.reset_index().rename(
                        columns={"index": "Type", "Type": "Count"}
                    ),
                    use_container_width=True
                )

            with col2:
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie(
                    type_count.values,
                    labels=type_count.index,
                    autopct="%1.1f%%",
                    startangle=90
                )
                plt.title("Leak Type Distribution")
                st.pyplot(fig)

            st.markdown("---")

            st.subheader("Flagged Messages")

            st.dataframe(
                cred_df,
                use_container_width=True
            )

            st.error(
                "🚨 Never share OTPs, passwords, PINs or CVVs over chat — "
                "no genuine bank or service will ever ask for these."
            )


# ==============================
# PHISHING URL ANALYZER
# ==============================

elif menu == "🎣 Phishing URL Analyzer":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload WhatsApp chat first.")

    else:

        df = st.session_state["chat"]

        st.header("🎣 Advanced Phishing URL Analyzer")

        st.caption(
            "Goes beyond keyword matching: checks for URL shorteners, IP-based links, "
            "suspicious TLDs, '@' obfuscation, excessive hyphens and brand typosquatting."
        )

        link_df = analyze_phishing_links(df)

        if len(link_df) == 0:

            st.info("No links found in this chat.")

        else:

            c1, c2, c3 = st.columns(3)

            c1.metric("Total Links", len(link_df))
            c2.metric(
                "Phishing-Likely",
                int((link_df["Risk"] == "🚨 Phishing-Likely").sum())
            )
            c3.metric(
                "Suspicious",
                int((link_df["Risk"] == "⚠ Suspicious").sum())
            )

            st.markdown("---")

            risk_count = link_df["Risk"].value_counts()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Risk Summary")
                st.dataframe(
                    risk_count.reset_index().rename(
                        columns={"index": "Risk", "Risk": "Count"}
                    ),
                    use_container_width=True
                )

            with col2:
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie(
                    risk_count.values,
                    labels=risk_count.index,
                    autopct="%1.1f%%",
                    startangle=90
                )
                plt.title("Link Risk Distribution")
                st.pyplot(fig)

            st.markdown("---")

            st.subheader("All Links Analyzed")

            st.dataframe(
                link_df,
                use_container_width=True
            )

            st.markdown("---")

            st.subheader("🚨 Phishing-Likely Links")

            danger_links = link_df[link_df["Risk"] == "🚨 Phishing-Likely"]

            if len(danger_links) == 0:
                st.success("No high-risk phishing links found.")
            else:
                st.dataframe(danger_links, use_container_width=True)
                st.error("⚠ Do not click these links. Verify the sender before opening any URL.")


# ==============================
# CHAT RISK SCORE
# ==============================

elif menu == "⚠️ Chat Risk Score":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload WhatsApp chat first.")

    else:

        df = st.session_state["chat"]

        st.header("⚠️ Overall Chat Cybersecurity Risk Score")

        st.caption(
            "Combines PII leaks, credential leaks and phishing links into a single "
            "risk score for the whole chat."
        )

        pii_df = extract_pii(df)
        cred_df = detect_credentials(df)
        link_df = analyze_phishing_links(df)

        pii_hits = len(pii_df)
        cred_hits = len(cred_df)
        phishing_hits = int((link_df["Risk"] == "🚨 Phishing-Likely").sum()) if len(link_df) else 0
        suspicious_hits = int((link_df["Risk"] == "⚠ Suspicious").sum()) if len(link_df) else 0

        # ---- Simple weighted risk score (0 = safest, 100 = riskiest) ---- #

        raw_score = (
            pii_hits * 4 +
            cred_hits * 8 +
            phishing_hits * 10 +
            suspicious_hits * 4
        )

        risk_score = min(raw_score, 100)
        safety_score = 100 - risk_score

        if risk_score >= 70:
            level = "🔴 Critical Risk"
        elif risk_score >= 40:
            level = "🟠 High Risk"
        elif risk_score >= 15:
            level = "🟡 Moderate Risk"
        else:
            level = "🟢 Low Risk"

        animated_metric_row([
            ("🕵️", "PII Leaks", pii_hits, "#f1c40f"),
            ("🔑", "Credential Leaks", cred_hits, "#e67e22"),
            ("🎣", "Phishing Links", phishing_hits, "#e74c3c"),
            ("⚠️", "Suspicious Links", suspicious_hits, "#e74c3c"),
        ])

        st.markdown("---")

        st.subheader("🛡 Overall Safety Gauge")

        gcol1, gcol2 = st.columns([1, 1.3])

        with gcol1:
            animated_gauge(risk_score, label="Risk Score / 100", height=300)

        with gcol2:
            st.markdown(f"### Risk Level : {level}")
            st.markdown(f"**Risk Score : {risk_score}/100**  (higher = riskier)")
            st.markdown(f"**Safety Score : {safety_score}/100**")
            st.progress(safety_score)

        st.markdown("---")

        st.subheader("Risk Contribution Breakdown")

        breakdown = pd.DataFrame({
            "Category": ["PII Leaks", "Credential Leaks", "Phishing Links", "Suspicious Links"],
            "Weighted Score": [
                pii_hits * 4,
                cred_hits * 8,
                phishing_hits * 10,
                suspicious_hits * 4
            ]
        })

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(
            breakdown["Category"],
            breakdown["Weighted Score"],
            color=["#f1c40f", "#e67e22", "#c0392b", "#e74c3c"]
        )
        plt.ylabel("Weighted Risk Points")
        plt.xticks(rotation=15)
        st.pyplot(fig)

        st.markdown("---")

        if risk_score >= 40:
            st.error(
                "🚨 This chat contains significant exposed personal/credential data "
                "or phishing links. Review flagged messages and avoid resharing this export."
            )
        elif risk_score >= 15:
            st.warning(
                "⚠ Some risky content found. Check the PII / Password / Phishing pages for details."
            )
        else:
            st.success("✅ This chat looks reasonably safe from a data-leak perspective.")


# ==============================
# AI CHAT SUMMARY
# ==============================

elif menu == "🤖 AI Chat Summary":

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload chat first.")

    else:

        df = st.session_state["chat"]

        st.header("🤖 AI Chat Summary")

        total_messages = len(df)
        total_users = df["User"].nunique()

        most_active = df["User"].value_counts().idxmax()
        most_messages = df["User"].value_counts().max()

        ghost = df["User"].value_counts().idxmin()
        ghost_messages = df["User"].value_counts().min()

        longest = df.loc[df["Characters"].idxmax()]

        busiest_day = df["Day"].value_counts().idxmax()
        busiest_month = df["Month"].value_counts().idxmax()

        st.success("📋 AI Generated Summary")

        st.markdown(f"""
### 📊 Chat Overview

- 💬 Total Messages : **{total_messages}**
- 👥 Total Users : **{total_users}**
- 🏆 Most Active User : **{most_active}**
- 📨 Messages Sent : **{most_messages}**
- 👻 Least Active User : **{ghost}**
- 📩 Messages Sent : **{ghost_messages}**
- 📅 Busiest Day : **{busiest_day}**
- 🗓 Busiest Month : **{busiest_month}**

""")

        st.markdown("---")

        st.subheader("🏆 Most Talkative User")

        st.metric(
            label=most_active,
            value=f"{most_messages} Messages"
        )

        st.markdown("---")

        st.subheader("👻 Ghost User")

        st.metric(
            label=ghost,
            value=f"{ghost_messages} Messages"
        )

        st.markdown("---")

        st.subheader("📝 Longest Message")

        st.write("**User:**", longest["User"])
        st.write("**Characters:**", longest["Characters"])

        st.text_area(
            "Message",
            longest["Message"],
            height=180
        )

        st.markdown("---")

        st.subheader("📊 User Activity")

        activity = df["User"].value_counts()

        fig, ax = plt.subplots(figsize=(10,5))

        ax.bar(
            activity.index,
            activity.values,
            color="#25D366"
        )

        plt.xticks(rotation=35)
        plt.xlabel("Users")
        plt.ylabel("Messages")
        plt.title("User Activity")

        st.pyplot(fig)

        st.markdown("---")

        st.subheader("⭐ Chat Score")

        score = 0

        if total_messages > 100:
            score += 20

        if total_users > 5:
            score += 20

        if df["Media"].sum() > 20:
            score += 20

        if df["Has_Link"].sum() > 10:
            score += 20

        if df["Words"].sum() > 500:
            score += 20

        st.progress(score)

        st.success(f"Overall Chat Activity Score : {score}/100")
        # ==============================
# EXPORT REPORT
# ==============================

elif menu=="📄 Export Report":

    if "chat" not in st.session_state:
        st.warning("Upload chat first")

    else:

        from io import BytesIO

        df=st.session_state["chat"]

        st.header("📄 Export Report")

        csv=df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download CSV",
            csv,
            "WhatsApp_Report.csv",
            "text/csv"
        )

        excel=BytesIO()

        with pd.ExcelWriter(
            excel,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False
            )

        st.download_button(

            "⬇ Download Excel",

            excel.getvalue(),

            "WhatsApp_Report.xlsx",

            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )
        # ==============================
# LANGUAGE DETECTION
# ==============================

elif menu == "🌐 Language Detection":

    from langdetect import detect

    if "chat" not in st.session_state:
        st.warning("Upload chat first")

    else:

        df = st.session_state["chat"]

        st.header("🌐 Language Detection")

        def language(msg):

            try:
                return detect(str(msg))
            except:
                return "unknown"

        df["Language"] = df["Message"].apply(language)

        st.dataframe(
            df[
                ["User","Message","Language"]
            ],
            use_container_width=True
        )

        lang=df["Language"].value_counts()

        fig,ax=plt.subplots(figsize=(7,7))

        ax.pie(
            lang.values,
            labels=lang.index,
            autopct="%1.1f%%"
        )

        plt.title("Languages Used")

        st.pyplot(fig)


# ==============================
# SEARCH
# ==============================

elif menu == "🔍 Search":

    if "chat" not in st.session_state:
        st.warning("Please upload chat first.")
    else:

        df = st.session_state["chat"]

        st.header("🔍 Search Messages")

        keyword = st.text_input("Enter keyword")

        if keyword:

            result = df[
                df["Message"].str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            ]

            st.success(f"{len(result)} Messages Found")

            st.dataframe(
                result,
                use_container_width=True
            )


# ==============================
# VOICE ASSISTANT (TEXT-TO-SPEECH)
# ==============================

elif menu == "🔊 Voice Assistant":

    st.header("🔊 Voice Assistant")

    st.caption(
        "For anyone who finds it easier to listen than to read — type or paste any text "
        "(a message, a summary, an explanation) and have it read aloud in English, "
        "Gujarati or Hindi."
    )

    default_msg = "Welcome to WhatsApp Chat Analyzer. Upload your chat and explore AI powered insights."

    if "chat" in st.session_state:
        df = st.session_state["chat"]
        most_active = df["User"].value_counts().idxmax()
        default_msg = (
            f"This chat has {len(df)} messages from {df['User'].nunique()} users. "
            f"The most active user is {most_active}."
        )

    speech_widget(default_text=default_msg, key="voice_main", height=190)

    st.markdown("---")
    st.info(
        "💡 This generates real natural speech (via Google's TTS engine) for accurate "
        "Gujarati and Hindi pronunciation — not just your browser's built-in voice. "
        "It needs an internet connection on the machine running this app."
    )


# ==============================
# AI CHAT ASSISTANT
# ==============================

elif menu == "🤖 AI Chat Assistant":

    st.header("🤖 AI Chat Assistant")

    st.caption(
        "Ask questions about the chat report you uploaded — in plain English — "
        "and get an instant answer, calculated live from your data."
    )

    if "chat" not in st.session_state:
        st.warning("⚠ Please upload a WhatsApp chat first (see '📂 Upload Chat').")

    else:

        df = st.session_state["chat"]

        if "ai_chat_history" not in st.session_state:
            st.session_state["ai_chat_history"] = []

        def _answer_report_question(q, df):

            ql = q.lower().strip()

            total_messages = len(df)
            total_users = df["User"].nunique()
            user_counts = df["User"].value_counts()

            # ---- most / least active ---- #
            if any(p in ql for p in ["most active", "top user", "talks most", "talkative", "who talks"]):
                return f"🏆 The most active user is **{user_counts.idxmax()}** with **{int(user_counts.max())}** messages."

            if any(p in ql for p in ["least active", "ghost", "quietest"]):
                return f"👻 The least active user is **{user_counts.idxmin()}** with only **{int(user_counts.min())}** messages."

            # ---- basic counts ---- #
            if any(p in ql for p in ["how many message", "total message", "number of message"]):
                return f"💬 This chat has a total of **{total_messages}** messages."

            if any(p in ql for p in ["how many user", "total user", "number of user", "how many member", "members"]):
                return f"👥 There are **{total_users}** unique users in this chat."

            if any(p in ql for p in ["how many word", "total word"]):
                return f"📝 A total of **{int(df['Words'].sum())}** words were sent in this chat."

            if any(p in ql for p in ["how many media", "total media", "photo", "video"]):
                return f"📷 **{int(df['Media'].sum())}** media messages were shared."

            # ---- links / phishing ---- #
            if "phishing" in ql:
                link_df = analyze_phishing_links(df)
                risky = int((link_df["Risk"] == "🚨 Phishing-Likely").sum()) if len(link_df) else 0
                return f"🎣 Found **{risky}** phishing-likely links out of **{len(link_df)}** total links analyzed."

            if "link" in ql:
                return f"🔗 There are **{int(df['Has_Link'].sum())}** messages containing links."

            # ---- spam ---- #
            if "spam" in ql:
                spam_keywords = [
                    "win", "winner", "lottery", "free", "click", "offer", "prize", "gift",
                    "urgent", "otp", "verify", "password", "bank", "credit card", "loan",
                    "investment", "bitcoin", "earn money", "limited offer", "congratulations",
                    "cash", "reward", "bonus", "claim now"
                ]

                def _spam_score(msg):
                    msg = str(msg).lower()
                    return sum(1 for w in spam_keywords if w in msg)

                scores = df["Message"].apply(_spam_score)
                spam_count = int((scores >= 2).sum())
                return f"🚨 Detected **{spam_count}** spam-like messages out of {total_messages}."

            # ---- risk score ---- #
            if any(p in ql for p in ["risk", "safe", "danger", "security"]):
                pii_hits = len(extract_pii(df))
                cred_hits = len(detect_credentials(df))
                link_df = analyze_phishing_links(df)
                phishing_hits = int((link_df["Risk"] == "🚨 Phishing-Likely").sum()) if len(link_df) else 0
                suspicious_hits = int((link_df["Risk"] == "⚠ Suspicious").sum()) if len(link_df) else 0
                raw_score = pii_hits * 4 + cred_hits * 8 + phishing_hits * 10 + suspicious_hits * 4
                risk_score = min(raw_score, 100)
                if risk_score >= 70:
                    level = "🔴 Critical Risk"
                elif risk_score >= 40:
                    level = "🟠 High Risk"
                elif risk_score >= 15:
                    level = "🟡 Moderate Risk"
                else:
                    level = "🟢 Low Risk"
                return f"⚠ Overall chat risk score is **{risk_score}/100** — **{level}**."

            # ---- PII / credentials ---- #
            if any(p in ql for p in ["pii", "personal data", "aadhar", "pan card"]):
                pii_df = extract_pii(df)
                return f"🕵️ Found **{len(pii_df)}** potential PII leaks (phone numbers, emails, PAN, Aadhar, card numbers)."

            if any(p in ql for p in ["password", "otp", "credential", "pin", "cvv"]):
                cred_df = detect_credentials(df)
                return f"🔑 Found **{len(cred_df)}** possible password / OTP / PIN / CVV leaks in plain text."

            # ---- sentiment ---- #
            if any(p in ql for p in ["sentiment", "positive", "negative", "mood", "tone"]):
                from textblob import TextBlob

                def _sent(text):
                    score = TextBlob(str(text)).sentiment.polarity
                    if score > 0:
                        return "Positive"
                    elif score < 0:
                        return "Negative"
                    return "Neutral"

                sample = df["Message"].sample(min(200, len(df)), random_state=1).apply(_sent)
                counts = sample.value_counts()
                parts = ", ".join(f"{k}: {v}" for k, v in counts.items())
                return f"❤️ Sentiment snapshot (sampled) → {parts}."

            # ---- emoji ---- #
            if "emoji" in ql:
                emojis = [ch for msg in df["Message"] for ch in str(msg) if ch in emoji.EMOJI_DATA]
                if not emojis:
                    return "😐 No emojis were found in this chat."
                top = Counter(emojis).most_common(1)[0]
                return f"😊 The most used emoji is **{top[0]}**, used **{top[1]}** times."

            # ---- busiest day / month ---- #
            if "busiest day" in ql or ("busiest" in ql and "day" in ql):
                return f"📅 The busiest day is **{df['Day'].value_counts().idxmax()}**."

            if "busiest month" in ql or ("busiest" in ql and "month" in ql):
                return f"🗓 The busiest month is **{df['Month'].value_counts().idxmax()}**."

            # ---- search / find keyword ---- #
            if ql.startswith("search ") or ql.startswith("find "):
                keyword = q.split(" ", 1)[1].strip()
                if keyword:
                    result = df[df["Message"].str.contains(keyword, case=False, na=False)]
                    return f"🔍 Found **{len(result)}** messages containing '{keyword}'."

            # ---- longest message ---- #
            if "longest message" in ql:
                longest = df.loc[df["Characters"].idxmax()]
                return f"📝 The longest message was sent by **{longest['User']}** ({int(longest['Characters'])} characters)."

            # ---- fallback ---- #
            return (
                "🤔 I couldn't quite understand that. Try asking things like:\n\n"
                "- who is the most active user\n"
                "- how many messages / users are there\n"
                "- how many spam messages are there\n"
                "- what's the risk score\n"
                "- how many links / phishing links\n"
                "- sentiment breakdown\n"
                "- most used emoji\n"
                "- busiest day / busiest month\n"
                "- search <keyword>"
            )

        # ---- render chat history ---- #
        for role, msg in st.session_state["ai_chat_history"]:
            with st.chat_message("user" if role == "user" else "assistant"):
                st.markdown(msg)

        user_q = st.chat_input("Ask something about your uploaded chat report...")

        if user_q:
            st.session_state["ai_chat_history"].append(("user", user_q))
            answer = _answer_report_question(user_q, df)
            st.session_state["ai_chat_history"].append(("assistant", answer))
            st.rerun()

        if st.session_state["ai_chat_history"]:
            if st.button("🗑 Clear Chat"):
                st.session_state["ai_chat_history"] = []
                st.rerun()


# ==============================
# ABOUT
# ==============================

elif menu == "ℹ About":

    st.header("About Project")

    st.markdown("""
# WhatsApp Chat Analyzer

### AI & Machine Learning Internship Project

### Features

- Upload WhatsApp Chat
- Dashboard
- Active Users
- Timeline
- Heatmap
- WordCloud
- Emoji Analysis
- Emotion Detection
- Spam Detection
- Link Analysis
- Sentiment Analysis
- Fake Link Detection
- PII Leak Detector
- Password/OTP Leak Detector
- Phishing URL Analyzer
- Chat Risk Score
- AI Chat Summary
- Export Report (CSV / Excel)
- Language Detection
- Search Messages

### Tools Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- WordCloud
- TextBlob
- langdetect

Developed By

**Zalak Chudasama**
""")

# ---------------- FOOTER ---------------- #

st.markdown("""
<style>
.footer-line{
    height:3px;
    border-radius:3px;
    margin:24px 0 10px 0;
    background:linear-gradient(90deg,#075E54,#25D366,#128C7E,#25D366,#075E54);
    background-size:300% 100%;
    animation:gradientMove 6s ease infinite;
}
@keyframes gradientMove{
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}
</style>
<div class="footer-line"></div>
<div class="app-footer">
    🔒 Made with ❤️ using Streamlit &nbsp;|&nbsp; WhatsApp Chat Analyzer © 2026
</div>
""", unsafe_allow_html=True)