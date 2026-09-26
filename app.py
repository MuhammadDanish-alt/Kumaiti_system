import io
import os
import re
import html
import hashlib
import sqlite3
import datetime
import difflib
import unicodedata
import warnings
from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

# Optional Tesseract OCR Support
try:
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

# Optional Plotly Support for Advanced Dashboarding
try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# ==========================================
# --- 1. PAGE CONFIGURATION & STYLING ------
# ==========================================
st.set_page_config(
    page_title="Muhammad Saleem Transaction Track Record",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* ============================================================
   KUMAITU PROFESSIONAL 3D THEME
   ============================================================ */

/* ---------- ROOT APPLICATION ---------- */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0, 200, 255, 0.08), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(120, 60, 255, 0.08), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(0, 255, 150, 0.06), transparent 30%),
        #080B12 !important;

    color: #FFFFFF !important;

    min-height: 100vh;

    animation: backgroundPulse 12s ease-in-out infinite alternate;
}


/* ---------- ANIMATED BACKGROUND ---------- */

[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(
            120deg,
            #080B12,
            #0D1620,
            #09131A,
            #0B0D18
        ) !important;

    background-size: 400% 400% !important;

    animation: gradientMove 18s ease infinite;

    color: #FFFFFF !important;
}

@keyframes gradientMove {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }

}

@keyframes backgroundPulse {

    from {
        filter: brightness(0.95);
    }

    to {
        filter: brightness(1.05);
    }

}


/* ---------- HEADER ---------- */

[data-testid="stHeader"] {
    background: rgba(8, 11, 18, 0.85) !important;

    backdrop-filter: blur(15px);

    border-bottom: 1px solid rgba(255,255,255,0.06);
}


/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #10141E,
            #0A0D14
        ) !important;

    border-right: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        8px 0 30px rgba(0,0,0,0.35);
}

[data-testid="stSidebar"] > div {

    background: transparent !important;

}


/* ---------- GENERAL TEXT ---------- */

body,
p,
label,
span,
.stMarkdown {

    color: #FFFFFF !important;

}


/* ============================================================
   MAIN TITLE
   ============================================================ */

.main-title-container {

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #071C26 0%,
            #103D4A 45%,
            #162B4A 100%
        );

    padding: 28px 32px;

    border-radius: 18px;

    margin-bottom: 28px;

    border: 1px solid rgba(255,255,255,0.12);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.45),
        inset 0 1px 0 rgba(255,255,255,0.12);

    transform-style: preserve-3d;

    transition:
        transform 0.4s ease,
        box-shadow 0.4s ease;

    animation: titleEntrance 0.8s ease-out;
}


.main-title-container:hover {

    transform:
        perspective(1000px)
        rotateX(2deg)
        rotateY(-2deg)
        translateY(-4px);

    box-shadow:
        0 25px 55px rgba(0,0,0,0.55),
        0 0 30px rgba(0,200,255,0.12);

}


/* Moving shine */

.main-title-container::before {

    content: "";

    position: absolute;

    top: 0;
    left: -120%;

    width: 70%;
    height: 100%;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.12),
            transparent
        );

    transform: skewX(-25deg);

    animation: shine 6s infinite;

}


@keyframes shine {

    0% {
        left: -120%;
    }

    45% {
        left: 130%;
    }

    100% {
        left: 130%;
    }

}


@keyframes titleEntrance {

    from {

        opacity: 0;

        transform:
            translateY(-20px)
            scale(0.98);

    }

    to {

        opacity: 1;

        transform:
            translateY(0)
            scale(1);

    }

}


.main-title-container h1 {

    position: relative;

    z-index: 2;

    color: #FFFFFF !important;

    font-family:
        "Times New Roman",
        Times,
        serif;

    font-size: 32px;

    font-weight: 700;

    margin: 0;

    text-shadow:
        0 2px 12px rgba(0,0,0,0.5);

}


/* ============================================================
   3D METRIC CARDS
   ============================================================ */

.metric-card-container {

    position: relative;

    overflow: hidden;

    min-height: 120px;

    padding: 22px;

    border-radius: 18px;

    color: #FFFFFF !important;

    border: 1px solid rgba(255,255,255,0.15);

    box-shadow:

        0 12px 25px rgba(0,0,0,0.35),

        inset 0 1px 0
        rgba(255,255,255,0.18);

    transform:

        perspective(1000px)
        translateZ(0);

    transition:

        transform 0.35s ease,
        box-shadow 0.35s ease;

    animation:
        cardEntrance 0.7s ease-out;

}


/* 3D hover */

.metric-card-container:hover {

    transform:

        perspective(1000px)
        rotateX(5deg)
        rotateY(-5deg)
        translateY(-8px)
        scale(1.02);

    box-shadow:

        0 25px 45px rgba(0,0,0,0.5),

        0 0 25px rgba(0,200,255,0.12);

}


/* Animated shine */

.metric-card-container::before {

    content: "";

    position: absolute;

    top: 0;

    left: -150%;

    width: 80%;

    height: 100%;

    background:

        linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.18),
            transparent
        );

    transform: skewX(-25deg);

    animation: cardShine 7s infinite;

}


@keyframes cardShine {

    0% {
        left: -150%;
    }

    35% {
        left: 150%;
    }

    100% {
        left: 150%;
    }

}


@keyframes cardEntrance {

    from {

        opacity: 0;

        transform:
            translateY(25px)
            scale(0.96);

    }

    to {

        opacity: 1;

        transform:
            translateY(0)
            scale(1);

    }

}


/* ---------- CARD COLORS ---------- */

.card-bg-1 {

    background:
        linear-gradient(
            135deg,
            #123A70,
            #1976D2
        );

}


.card-bg-2 {

    background:
        linear-gradient(
            135deg,
            #087F73,
            #18C78D
        );

}


.card-bg-3 {

    background:
        linear-gradient(
            135deg,
            #A51F47,
            #F0445F
        );

}


.card-bg-4 {

    background:
        linear-gradient(
            135deg,
            #5520A8,
            #8748E8
        );

}


.card-bg-5 {

    background:
        linear-gradient(
            135deg,
            #A95E18,
            #E4B83E
        );

}


.card-bg-6 {

    background:
        linear-gradient(
            135deg,
            #006A89,
            #00A9D6
        );

}


.card-bg-7 {

    background:
        linear-gradient(
            135deg,
            #16864B,
            #28D9A0
        );

}


.card-bg-8 {

    background:
        linear-gradient(
            135deg,
            #A93D76,
            #EBCB4D
        );

}


/* ---------- CARD TEXT ---------- */

.metric-card-title {

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1px;

    text-transform: uppercase;

    color: #FFFFFF !important;

    opacity: 0.9;

}


.metric-card-value {

    font-size: 28px;

    font-weight: 800;

    line-height: 1.2;

    color: #FFFFFF !important;

    text-shadow:
        0 2px 8px rgba(0,0,0,0.3);

}


.metric-card-sub {

    font-size: 11px;

    margin-top: 6px;

    color: #FFFFFF !important;

    opacity: 0.8;

}


/* ============================================================
   SIDEBAR NAVIGATION MENU
   ============================================================ */

[data-testid="stSidebar"] div[role="radiogroup"] {

    gap: 6px !important;

}

[data-testid="stSidebar"] div[role="radiogroup"] label {

    background: rgba(255,255,255,0.04) !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    border-radius: 10px !important;

    padding: 10px 14px !important;

    width: 100%;

    transition: all 0.2s ease;

}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {

    background:
        linear-gradient(
            135deg,
            rgba(0,200,83,0.18),
            rgba(0,200,83,0.06)
        ) !important;

    border-color: rgba(0,200,83,0.35) !important;

    transform: translateX(2px);

}

[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {

    background-color: #00C853 !important;

}

[data-testid="stSidebar"] div[role="radiogroup"] p {

    font-size: 14px !important;

    font-weight: 600 !important;

    color: #FFFFFF !important;

}


/* ============================================================
   TABS  (kept for the Excel multi-sheet sub-tabs)
   ============================================================ */

.stTabs [data-baseweb="tab-list"] {

    gap: 8px;

    background: transparent !important;

}


.stTabs [data-baseweb="tab"] {

    background:
        rgba(38,39,48,0.8) !important;

    color: #D9E1EA !important;

    border: 1px solid
        rgba(255,255,255,0.08);

    border-radius: 10px;

    padding: 10px 18px;

    transition:
        all 0.3s ease;

    box-shadow:
        0 5px 12px rgba(0,0,0,0.2);

}


.stTabs [data-baseweb="tab"]:hover {

    background:
        rgba(0,200,83,0.15) !important;

    color: #FFFFFF !important;

    transform:
        translateY(-2px);

}


.stTabs [aria-selected="true"] {

    background:
        linear-gradient(
            135deg,
            #116530,
            #00A86B
        ) !important;

    color: #FFFFFF !important;

    box-shadow:
        0 6px 18px
        rgba(0,200,83,0.25);

}


/* ============================================================
   INPUTS
   ============================================================ */

input,
textarea,
select {

    background-color:
        #171B25 !important;

    color:
        #FFFFFF !important;

    border:
        1px solid #343B49 !important;

    border-radius:
        8px !important;

    transition:
        all 0.25s ease;

}


input:focus,
textarea:focus {

    border-color:
        #00C853 !important;

    box-shadow:
        0 0 0 2px
        rgba(0,200,83,0.15) !important;

}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #17202B,
            #263342
        ) !important;

    color:
        #FFFFFF !important;

    border:
        1px solid
        rgba(255,255,255,0.12) !important;

    border-radius:
        9px !important;

    font-weight:
        600 !important;

    box-shadow:
        0 5px 15px
        rgba(0,0,0,0.25);

    transition:
        all 0.3s ease;

}


.stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            #00A84F,
            #00C853
        ) !important;

    transform:
        translateY(-3px);

    box-shadow:
        0 10px 25px
        rgba(0,200,83,0.25);

}


/* ============================================================
   DATAFRAME
   ============================================================ */

.stDataFrame {

    border-radius:
        12px;

    overflow:
        hidden;

    border:
        1px solid
        rgba(255,255,255,0.1);

    box-shadow:
        0 10px 25px
        rgba(0,0,0,0.25);

}


/* ============================================================
   EXPANDERS
   ============================================================ */

[data-testid="stExpander"] {

    background:
        rgba(20,24,34,0.8) !important;

    border:
        1px solid
        rgba(255,255,255,0.1) !important;

    border-radius:
        12px !important;

    box-shadow:
        0 8px 20px
        rgba(0,0,0,0.2);

    transition:
        all 0.3s ease;

}


[data-testid="stExpander"]:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 12px 28px
        rgba(0,0,0,0.35);

}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {

    background:
        rgba(20,24,34,0.85) !important;

    border:
        1px dashed
        #465061 !important;

    border-radius:
        14px !important;

    padding:
        10px;

    transition:
        all 0.3s ease;

}


[data-testid="stFileUploader"]:hover {

    border-color:
        #00C853 !important;

    box-shadow:
        0 0 20px
        rgba(0,200,83,0.12);

}


/* ============================================================
   ALERTS
   ============================================================ */

[data-testid="stAlert"] {

    border-radius:
        10px !important;

    box-shadow:
        0 6px 18px
        rgba(0,0,0,0.2);

}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {

    border:
        none !important;

    height:
        1px !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            #34404F,
            transparent
        ) !important;

    margin:
        28px 0 !important;

}


/* ============================================================
   URDU + ENGLISH
   ============================================================ */

input,
textarea {

    unicode-bidi:
        plaintext;

    font-family:
        "Segoe UI",
        "Noto Nastaliq Urdu",
        "Jameel Noori Nastaleeq",
        sans-serif;

}


/* ============================================================
   SCROLLBAR
   ============================================================ */

::-webkit-scrollbar {

    width:
        9px;

    height:
        9px;

}


::-webkit-scrollbar-track {

    background:
        #080B12;

}


::-webkit-scrollbar-thumb {

    background:
        #374151;

    border-radius:
        10px;

}


::-webkit-scrollbar-thumb:hover {

    background:
        #00C853;

}


/* ============================================================
   PAGE SPACING
   ============================================================ */

.block-container {

    padding-top:
        2rem;

    padding-bottom:
        4rem;

}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .main-title-container {

        padding:
            20px;

        border-radius:
            14px;

    }

    .main-title-container h1 {

        font-size:
            23px;

    }

    .metric-card-container {

        min-height:
            100px;

        padding:
            18px;

    }

    .metric-card-value {

        font-size:
            23px;

    }

}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="main-title-container">
    <h1>
        Muhammad Saleem Transaction Track Record
    </h1>
</div>
""", unsafe_allow_html=True)

# ==========================================

# --- 2. TEXT / NUMBER HELPERS -------------
# ==========================================
URDU_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
_URDU_MAP = str.maketrans({"ي": "ی", "ى": "ی", "ې": "ی", "ك": "ک", "ه": "ہ", "ۃ": "ہ", "ة": "ہ", "ۀ": "ہ"})
_DIACRITICS = re.compile("[\u064B-\u065F\u0670\u06D6-\u06ED\u0640]")

# Column-name words that mean "identifier / code / date" -> never summed in dashboard totals
ID_TOKENS = {
    "id", "sr", "serial", "sno", "code", "no", "number", "num", "phone", "ph", "mobile", "cnic",
    "acct", "account", "date", "month", "unnamed", "created", "تاریخ", "نمبر", "فون", "موبائل", "کوڈ", "شناختی",
}


def normalize_digits(s):
    return str(s).translate(URDU_DIGITS)


def normalize_text(s):
    """Lower-case + unify Urdu/Arabic letter variants, digits and diacritics (for searching)."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", str(s))
    s = s.translate(_URDU_MAP).translate(URDU_DIGITS)
    s = _DIACRITICS.sub("", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def is_id_like(name):
    tokens = re.findall(r"[a-z0-9\u0600-\u06FF]+", normalize_text(name))
    return any(t in ID_TOKENS for t in tokens)


def is_serial_col(name):
    key = re.sub(r"[^a-z0-9]", "", str(name).lower())
    return key.startswith("sr") or key.startswith("serial") or key in {"sno", "no", "num", "number"}


def to_num(v):
    """Parse a value like '1,500', '$20', '۱۵۰۰' -> float, or None if not numeric."""
    if v is None:
        return None
    s = normalize_digits(str(v)).replace("٫", ".").replace("٬", "").replace(",", "")
    s = s.replace("$", "").replace("Rs.", "").replace("Rs", "").strip()
    if not s:
        return None
    try:
        f = float(s)
        return None if np.isnan(f) else f
    except ValueError:
        return None


def fmt_num(f):
    if f is None:
        return ""
    if float(f).is_integer():
        return str(int(f))
    return f"{f:.2f}".rstrip("0").rstrip(".")


def cell_to_str(v):
    if v is None:
        return ""
    try:
        if pd.isna(v):
            return ""
    except (TypeError, ValueError):
        pass
    if isinstance(v, (pd.Timestamp, datetime.datetime)):
        if v.hour == 0 and v.minute == 0 and v.second == 0:
            return v.strftime("%Y-%m-%d")
        return v.strftime("%Y-%m-%d %H:%M")
    if isinstance(v, datetime.date):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else ("%.10g" % v)
    return str(v).strip()


def is_number_like(v):
    s = normalize_digits(v).replace(",", "").replace(" ", "")
    if not s:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return bool(re.fullmatch(r"\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}", s))


def find_col(cols, keyword):
    for c in cols:
        if keyword in str(c).lower():
            return c
    return None


# ==========================================
# CASH IN HAND + EMAIL NOTIFICATION HELPERS
# ==========================================

def find_financial_column(columns, column_types):
    """
    Finds the most suitable financial column.

    Example:
    receipt -> Cash Receipt / Receipt / Income / Credit
    payment -> Cash Payment / Payment / Expense / Debit
    balance -> Balance / Cash in Hand / Remaining Balance
    """
    priority = {
        "receipt": ["cash receipt", "cash_received", "receipt", "receipts", "income", "credit", "cash in"],
        "payment": ["cash payment", "cash_paid", "payment", "payments", "expense", "expenses", "debit", "cash out"],
        "balance": ["cash in hand", "cash_in_hand", "balance", "remaining balance", "remaining_balance",
                    "closing balance", "closing_balance"],
    }

    candidates = priority.get(column_types, [])

    # 1. Exact match
    for candidate in candidates:
        for col in columns:
            if normalize_text(col) == normalize_text(candidate):
                return col

    # 2. Substring match
    for candidate in candidates:
        for col in columns:
            if normalize_text(candidate) in normalize_text(col):
                return col

    # 3. Fuzzy match - catches typos in the header, e.g. "Cash Recepit" for "Cash Receipt"
    best_col, best_score = None, 0.0
    for col in columns:
        col_norm = normalize_text(col)
        for candidate in candidates:
            score = difflib.SequenceMatcher(None, col_norm, normalize_text(candidate)).ratio()
            if score > best_score:
                best_score, best_col = score, col
    if best_score >= 0.72:
        return best_col

    return None


def calculate_cash_in_hand(df):
    """
    Recalculate running Cash in Hand for the COMPLETE sheet.

        Current Cash In Hand = Previous Cash In Hand + Cash Receipt - Cash Payment

    The calculation starts from zero for every individual sheet.
    """
    if df is None or df.empty:
        return df.copy()

    result = tidy_df(df)

    receipt_col = find_financial_column(result.columns, "receipt")
    payment_col = find_financial_column(result.columns, "payment")
    balance_col = find_financial_column(result.columns, "balance")

    if receipt_col is None and payment_col is None:
        return result

    if balance_col is None:
        balance_col = "Cash in Hand"
        result[balance_col] = ""

    running_balance = 0.0
    for idx in result.index:
        receipt = to_num(result.at[idx, receipt_col]) if receipt_col is not None else None
        payment = to_num(result.at[idx, payment_col]) if payment_col is not None else None
        running_balance += (receipt or 0.0) - (payment or 0.0)
        result.at[idx, balance_col] = fmt_num(running_balance)

    return tidy_df(result)


def get_cash_columns(df):
    """Returns the receipt, payment and balance columns detected in a sheet."""
    if df is None or df.empty:
        return None, None, None
    return (
        find_financial_column(df.columns, "receipt"),
        find_financial_column(df.columns, "payment"),
        find_financial_column(df.columns, "balance"),
    )


def get_active_notification_emails():
    """Get all active email addresses from the saved User Directory."""
    users_df = get_users_df()
    if users_df.empty:
        return []

    emails = []
    for _, row in users_df.iterrows():
        if not bool(row.get("active", 0)):
            continue
        email = str(row.get("email", "")).strip()
        email = re.sub(r"\[([^\]]+)\]\(mailto:[^)]+\)", r"\1", email)
        if email and "@" in email:
            emails.append(email)

    return list(dict.fromkeys(emails))


def send_email_notification(subject, body, to_list=None, cc_list=None):
    """
    Send a real email using SMTP, with explicit To and Cc recipient lists.
    SMTP settings are read ONLY from environment variables - no credentials
    are hardcoded in this file:

        KUMAITU_SMTP_HOST      (default: smtp.gmail.com)
        KUMAITU_SMTP_PORT      (default: 587)
        KUMAITU_SMTP_USER      (required)
        KUMAITU_SMTP_PASSWORD  (required - use a Gmail "App Password", not your login password)
        KUMAITU_FROM_EMAIL     (default: same as KUMAITU_SMTP_USER)
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    to_list = [str(e).strip() for e in (to_list or []) if str(e).strip() and "@" in str(e)]
    cc_list = [str(e).strip() for e in (cc_list or []) if str(e).strip() and "@" in str(e) and e not in to_list]

    if not to_list and not cc_list:
        return False, "No recipients specified."

    smtp_host = os.getenv("KUMAITU_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("KUMAITU_SMTP_PORT", "587"))
    smtp_user = os.getenv("KUMAITU_SMTP_USER", "").strip()
    smtp_password = os.getenv("KUMAITU_SMTP_PASSWORD", "").strip()
    from_email = os.getenv("KUMAITU_FROM_EMAIL", smtp_user).strip()

    if not smtp_user or not smtp_password:
        return False, (
            "SMTP credentials are not configured. Set the KUMAITU_SMTP_USER and "
            "KUMAITU_SMTP_PASSWORD environment variables (see .env) before sending email."
        )

    # A message needs a valid To header even in "send to all, everyone in Cc" mode.
    if not to_list:
        to_list = [from_email] if from_email else []

    all_recipients = list(dict.fromkeys(to_list + cc_list))
    if not all_recipients:
        return False, "No valid recipients specified."

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = ", ".join(to_list)
    if cc_list:
        message["Cc"] = ", ".join(cc_list)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, all_recipients, message.as_string())
        log_system_event("EMAIL_SENT", f"Subject={subject}; To={len(to_list)}; Cc={len(cc_list)}")
        return True, f"Email sent - To: {len(to_list)}, Cc: {len(cc_list)}."
    except Exception as ex:
        log_system_event("EMAIL_ERROR", str(ex))
        return False, str(ex)


def build_cash_notification(sheet_name, row_data, receipt_col, payment_col, balance_col):
    """Build the email content for a receipt/payment transaction."""
    receipt = to_num(row_data.get(receipt_col, "")) if receipt_col else 0
    payment = to_num(row_data.get(payment_col, "")) if payment_col else 0
    balance = to_num(row_data.get(balance_col, "")) if balance_col else 0
    receipt, payment, balance = receipt or 0, payment or 0, balance or 0

    particular_col = (find_col(row_data.keys(), "particular")
                      or find_col(row_data.keys(), "name")
                      or find_col(row_data.keys(), "description"))
    date_col = find_col(row_data.keys(), "date") or find_col(row_data.keys(), "entry_date")

    particular = cell_to_str(row_data.get(particular_col, "")) if particular_col else ""
    entry_date = (cell_to_str(row_data.get(date_col, "")) if date_col
                 else datetime.date.today().strftime("%Y-%m-%d"))

    subject = f"Kumaitu Cash Update - {sheet_name}"
    body = f"""KUMAITU SYSTEM - CASH TRANSACTION UPDATE
==========================================

Sheet:
{sheet_name}

Date:
{entry_date}

Particular / Name:
{particular}

Cash Receipt:
{receipt:,.2f}

Cash Payment:
{payment:,.2f}

Cash in Hand / Remaining Balance:
{balance:,.2f}

------------------------------------------
Calculation:

Previous Cash in Hand
+ Cash Receipt
- Cash Payment
= Current Cash in Hand

This notification was generated automatically by the Kumaitu System.
Please do not reply to this automated notification.
"""
    return subject, body


def build_batch_notification(pending):
    """Combine every pending change into a single email body, listed one after another."""
    subject = f"Kumaitu Cash Update - {len(pending)} change(s)"
    lines = ["KUMAITU SYSTEM - CASH TRANSACTION UPDATE", "=" * 42, ""]
    for i, item in enumerate(pending, 1):
        row = item["row_dict"]
        receipt_col, payment_col, balance_col = item.get("receipt_col"), item.get("payment_col"), item.get("balance_col")
        receipt = (to_num(row.get(receipt_col, "")) or 0) if receipt_col else 0
        payment = (to_num(row.get(payment_col, "")) or 0) if payment_col else 0
        balance = (to_num(row.get(balance_col, "")) or 0) if balance_col else 0

        particular_col = (find_col(row.keys(), "particular") or find_col(row.keys(), "name")
                          or find_col(row.keys(), "description"))
        date_col = find_col(row.keys(), "date") or find_col(row.keys(), "entry_date")
        particular = cell_to_str(row.get(particular_col, "")) if particular_col else ""
        entry_date = (cell_to_str(row.get(date_col, "")) if date_col
                     else datetime.date.today().strftime("%Y-%m-%d"))

        lines.append(f"{i}. Sheet / source: {item['source_name']}")
        lines.append(f"   Date: {entry_date}")
        lines.append(f"   Particular / name: {particular}")
        lines.append(f"   Cash receipt: {receipt:,.2f}")
        lines.append(f"   Cash payment: {payment:,.2f}")
        if balance_col:
            lines.append(f"   Cash in hand: {balance:,.2f}")
        lines.append("")

    lines.append("This notification was generated automatically by the Kumaitu System.")
    lines.append("Please do not reply to this automated notification.")
    return subject, "\n".join(lines)


def auto_notify_new_row(source_name, row_dict):
    """
    Queue a financial change for notification - it is NOT emailed immediately.
    A popup appears asking whether to send to all registered users (everyone in
    Cc) or to specific users (selected as To, everyone else as Cc); nothing is
    emailed until that popup is answered. Called from every place a row is
    added or changed: the Append Row form, the SQLite Commit form, the OCR
    push, and the Excel/SQLite grid saves. Silently does nothing if the row
    has no receipt/payment amount at all.
    """
    columns = list(row_dict.keys())
    receipt_col = find_financial_column(columns, "receipt")
    payment_col = find_financial_column(columns, "payment")
    balance_col = find_financial_column(columns, "balance")

    if receipt_col is None and payment_col is None:
        return  # not a financial row - nothing to notify about

    receipt = to_num(row_dict.get(receipt_col, "")) if receipt_col else 0
    payment = to_num(row_dict.get(payment_col, "")) if payment_col else 0
    if not receipt and not payment:
        return  # amounts are blank/zero - nothing changed financially

    st.session_state.pending_notifications.append({
        "source_name": source_name,
        "row_dict": row_dict,
        "receipt_col": receipt_col,
        "payment_col": payment_col,
        "balance_col": balance_col,
    })


def col_is_numeric(series):
    s = series.astype(str).str.strip()
    nonempty = s[s != ""]
    if nonempty.empty:
        return False
    valid = nonempty.map(to_num).notna().sum()
    return valid > 0 and valid / len(nonempty) >= 0.6


def tidy_df(df):
    """Everything as clean strings: no NaN/None, no hidden spaces in headers."""
    out = df.copy()
    out.columns = [str(c).strip() or "Unnamed" for c in out.columns]
    for c in out.columns:
        out[c] = out[c].map(cell_to_str)
    return out.reset_index(drop=True)


def frames_equal(a, b):
    if list(a.columns) != list(b.columns) or len(a) != len(b):
        return False
    return a.reset_index(drop=True).equals(b.reset_index(drop=True))


def sanitize_dataframe_columns(df):
    df.columns = [str(c).strip() or "Unnamed" for c in df.columns]
    return df


# ------------------ Excel loading with header detection ------------------
def detect_header_row(raw, max_scan=15):
    best_i, best_score = 0, -1e9
    n = min(max_scan, len(raw))
    for i in range(n):
        vals = [cell_to_str(v) for v in raw.iloc[i].tolist()]
        filled = [v for v in vals if v]
        if not filled:
            continue
        if len(filled) < 2 and raw.shape[1] > 1:
            continue
        text_like = [v for v in filled if not is_number_like(v)]
        uniq = len({normalize_text(v) for v in filled}) / len(filled)
        score = len(filled) * (len(text_like) / len(filled)) * uniq
        if i + 1 < len(raw):
            nxt = [cell_to_str(v) for v in raw.iloc[i + 1].tolist() if cell_to_str(v)]
            if nxt and sum(is_number_like(v) for v in nxt) / len(nxt) > 1 - len(text_like) / len(filled):
                score += 0.5
        score -= i * 0.01
        if score > best_score:
            best_i, best_score = i, score
    return best_i


def build_table(raw, header_idx):
    hdr = [cell_to_str(v) for v in raw.iloc[header_idx].tolist()]
    names, seen, generated = [], {}, set()
    for j, h in enumerate(hdr):
        h = re.sub(r"\s+", " ", h).strip()
        if not h:
            h = f"Column {j + 1}"
            generated.add(h)
        base = h
        k = seen.get(base, 0)
        seen[base] = k + 1
        if k:
            h = f"{base} ({k + 1})"
        names.append(h)
    body = raw.iloc[header_idx + 1:].copy()
    body.columns = names
    body = body.apply(lambda col: col.map(cell_to_str))
    body = body[~(body == "").all(axis=1)]
    drop = [c for c in body.columns if c in generated and (body[c] == "").all()]
    body = body.drop(columns=drop)
    return body.reset_index(drop=True)


def read_excel_bytes(data):
    """
    Detect the REAL file format from its first bytes (the extension can lie):
      PK..        -> modern .xlsx / .xlsm   (openpyxl)
      D0 CF 11 E0 -> old .xls (BIFF)        (xlrd)
      '<' text    -> HTML/XML table saved as .xls by some software
    Returns {sheet_name: raw DataFrame (header=None)}.
    """
    head = data[:8]

    if head.startswith(b"PK"):
        try:
            xls = pd.ExcelFile(io.BytesIO(data), engine="openpyxl")
        except ImportError:
            raise RuntimeError("Missing package 'openpyxl'. Run:  pip install openpyxl")
        return {sn: xls.parse(sn, header=None, dtype=object) for sn in xls.sheet_names}

    if head.startswith(b"\xd0\xcf\x11\xe0"):
        try:
            xls = pd.ExcelFile(io.BytesIO(data), engine="xlrd")
        except ImportError:
            raise RuntimeError(
                "This file is an OLD-format Excel file (.xls), even if its name ends in .xlsx. "
                "Run:  pip install xlrd   (then restart the app), or open it in Excel and 'Save As' .xlsx."
            )
        return {sn: xls.parse(sn, header=None, dtype=object) for sn in xls.sheet_names}

    if head.lstrip()[:1] == b"<":  # HTML / XML disguised as Excel
        text = None
        for enc in ("utf-8-sig", "cp1256", "latin-1"):
            try:
                text = data.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        try:
            tables = pd.read_html(io.StringIO(text), header=None)
        except Exception as e:
            raise RuntimeError(f"This looks like an HTML export, but no tables could be read ({e}). "
                               "Try: pip install lxml beautifulsoup4 html5lib")
        return {f"Table {i}": t.astype(object) for i, t in enumerate(tables, 1)}

    raise RuntimeError("Unrecognised file format. Please upload a real .xlsx / .xls / .csv file.")


def load_workbook_sheets(data, filename):
    """Read EVERY sheet (incl. hidden). Header row is auto-detected. Values become clean text."""
    sheets = {}
    if filename.lower().endswith(".csv"):
        raw_map = {}
        for enc in ("utf-8-sig", "utf-16", "cp1256", "latin-1"):
            try:
                raw_map["CSV"] = pd.read_csv(io.BytesIO(data), header=None, dtype=object, encoding=enc,
                                             engine="python", sep=None)
                break
            except Exception:
                continue
        if not raw_map:
            raise RuntimeError("Could not read this CSV file.")
    else:
        raw_map = read_excel_bytes(data)

    for sn, raw in raw_map.items():
        raw = raw.dropna(how="all").dropna(axis=1, how="all").reset_index(drop=True)
        if raw.empty:
            sheets[str(sn)] = pd.DataFrame()
            continue
        sheets[str(sn)] = build_table(raw, detect_header_row(raw))
    return sheets


# ------------------ Excel export (real numbers / real dates) ------------------
def safe_sheet_name(name, used):
    base = re.sub(r"[\[\]\:\*\?\/\\]", "_", str(name))[:31] or "Sheet"
    cand, i = base, 1
    while cand.lower() in used:
        suffix = f"_{i}"
        cand = base[:31 - len(suffix)] + suffix
        i += 1
    used.add(cand.lower())
    return cand


def export_ready(df):
    out = df[[c for c in df.columns if not str(c).startswith("_")]].copy().fillna("")
    out = out[~(out.astype(str).apply(lambda col: col.str.strip()) == "").all(axis=1)]
    for c in out.columns:
        key = str(c).lower()
        if any(k in key for k in ("date", "month", "تاریخ")):
            parsed = out[c].map(lambda v: pd.to_datetime(v, errors="coerce") if str(v).strip() else pd.NaT)
            nonempty = (out[c].astype(str).str.strip() != "").sum()
            if nonempty and parsed.notna().sum() / nonempty >= 0.8:
                out[c] = parsed.map(lambda d: d.date() if pd.notna(d) else None)
            continue
        if (not is_id_like(c) or is_serial_col(c)) and col_is_numeric(out[c]):
            out[c] = out[c].map(lambda v: (to_num(v) if to_num(v) is not None else v))
            out[c] = out[c].map(lambda v: int(v) if isinstance(v, float) and v.is_integer() else v)
    return out


def generate_excel_bytes(sheets_dict):
    output = io.BytesIO()
    used = set()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in sheets_dict.items():
            export_ready(df).to_excel(writer, sheet_name=safe_sheet_name(sheet_name, used), index=False)
    output.seek(0)
    return output.getvalue()


# ==========================================
# --- 3. DATABASE SCHEMAS & HELPERS --------
# ==========================================
DB_NAME = "kumaitu_enterprise_v2.db"
DB_COLUMNS = ["sr_no", "entry_date", "particular", "cash_receipt", "cash_payment", "balance", "remarks"]


def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cash_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sr_no TEXT,
            entry_date TEXT,
            particular TEXT,
            cash_receipt REAL DEFAULT 0.0,
            cash_payment REAL DEFAULT 0.0,
            balance REAL DEFAULT 0.0,
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notification_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'User',
            active INTEGER DEFAULT 1
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM notification_users")
    if cursor.fetchone()[0] == 0:
        # Only one real, working address is seeded by default. The two placeholder
        # @kumaitu.com addresses previously seeded here always bounce (that domain
        # does not exist), and on Streamlit Cloud this table resets on every
        # restart - so they kept silently reappearing and causing failed sends.
        # Add any additional real users yourself in the User Directory tab.
        cursor.execute(
            "INSERT INTO notification_users (name, email, role, active) VALUES (?, ?, ?, ?)",
            ("Muhammad DANISH", "danishzamord@gmail.com", "Administrator", 1),
        )
    conn.commit()
    conn.close()


def log_system_event(action: str, details: str = ""):
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO system_logs (action, details) VALUES (?, ?)", (action, details))
        conn.commit()
        conn.close()
    except Exception:
        pass


def get_entries_df():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(
            "SELECT id, sr_no, entry_date, particular, cash_receipt, cash_payment, balance, remarks "
            "FROM cash_entries ORDER BY id ASC", conn)
    except Exception:
        df = pd.DataFrame(columns=["id"] + DB_COLUMNS)
    finally:
        conn.close()
    return df


def add_db_entry(entry_dict: dict):
    conn = get_db_connection()
    keys = list(entry_dict.keys())
    placeholders = ", ".join(["?"] * len(keys))
    conn.execute(f"INSERT INTO cash_entries ({', '.join(keys)}) VALUES ({placeholders})", list(entry_dict.values()))
    conn.commit()
    conn.close()
    log_system_event("INSERT_DB_ROW", f"Inserted record: {entry_dict.get('particular', 'N/A')}")


def replace_db_entries(df: pd.DataFrame):
    """
    Persist CRUD changes made in the SQLite grid without deleting/recreating the whole
    table. Existing record IDs are preserved, edited records are updated, rows marked
    with ``_delete`` are deleted, and rows without an ID are inserted.

    This is transactional: either the complete Save Changes operation succeeds, or the
    database is rolled back, preventing a partial update if one row has invalid data.
    """
    conn = get_db_connection()
    inserted = updated = deleted = 0
    try:
        conn.execute("BEGIN")
        for _, row in df.iterrows():
            raw_id = row.get("id", "")
            delete_flag = bool(row.get("_delete", False))
            try:
                record_id = int(float(raw_id)) if cell_to_str(raw_id) else None
            except (TypeError, ValueError):
                record_id = None

            if delete_flag and record_id is not None:
                conn.execute("DELETE FROM cash_entries WHERE id = ?", (record_id,))
                deleted += 1
                continue

            vals = {c: row.get(c, "") for c in DB_COLUMNS}
            if record_id is None and all(cell_to_str(v) in ("", "0", "0.0") for v in vals.values()):
                continue

            for c in ("cash_receipt", "cash_payment", "balance"):
                vals[c] = to_num(vals[c]) or 0.0
            for c in ("sr_no", "entry_date", "particular", "remarks"):
                vals[c] = cell_to_str(vals[c])

            if record_id is not None:
                exists = conn.execute("SELECT 1 FROM cash_entries WHERE id = ?", (record_id,)).fetchone()
                if exists:
                    conn.execute(
                        "UPDATE cash_entries SET sr_no=?, entry_date=?, particular=?, cash_receipt=?, "
                        "cash_payment=?, balance=?, remarks=? WHERE id=?",
                        (vals["sr_no"], vals["entry_date"], vals["particular"],
                         vals["cash_receipt"], vals["cash_payment"], vals["balance"],
                         vals["remarks"], record_id)
                    )
                    updated += 1
                else:
                    conn.execute(
                        "INSERT INTO cash_entries (sr_no, entry_date, particular, cash_receipt, cash_payment, balance, remarks) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (vals["sr_no"], vals["entry_date"], vals["particular"], vals["cash_receipt"],
                         vals["cash_payment"], vals["balance"], vals["remarks"])
                    )
                    inserted += 1
            else:
                conn.execute(
                    "INSERT INTO cash_entries (sr_no, entry_date, particular, cash_receipt, cash_payment, balance, remarks) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (vals["sr_no"], vals["entry_date"], vals["particular"], vals["cash_receipt"],
                     vals["cash_payment"], vals["balance"], vals["remarks"])
                )
                inserted += 1

        conn.commit()
        result = {"inserted": inserted, "updated": updated, "deleted": deleted, "total": inserted + updated + deleted}
        log_system_event("CRUD_SAVE_DB_TABLE", f"Inserted={inserted}, Updated={updated}, Deleted={deleted}")
        return result
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def save_workbook_permanently(sheets_dict, original_name=""):
    """Save the current in-memory workbook as a durable XLSX copy on disk."""
    base = Path(original_name).stem if original_name else "Kumaitu_Workbook"
    base = re.sub(r"[^A-Za-z0-9_ -]+", "_", base).strip() or "Kumaitu_Workbook"
    path = os.path.abspath(f"{base}_Kumaitu_Saved.xlsx")
    with open(path, "wb") as fh:
        fh.write(generate_excel_bytes(sheets_dict))
    log_system_event("SAVE_WORKBOOK_PERMANENT", f"Saved workbook permanently: {path}")
    return path


def get_users_df():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT id, name, email, role, active FROM notification_users", conn)
    except Exception:
        df = pd.DataFrame(columns=["id", "name", "email", "role", "active"])
    finally:
        conn.close()
    return df


def update_users_table(users_df: pd.DataFrame):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notification_users")
    for _, row in users_df.iterrows():
        cursor.execute(
            "INSERT INTO notification_users (name, email, role, active) VALUES (?, ?, ?, ?)",
            (str(row.get("name", "")), str(row.get("email", "")), str(row.get("role", "User")), 1 if row.get("active") else 0)
        )
    conn.commit()
    conn.close()
    log_system_event("UPDATE_USERS", f"Updated {len(users_df)} user records.")


def get_logs_df():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM system_logs ORDER BY id DESC LIMIT 200", conn)
    except Exception:
        df = pd.DataFrame(columns=["id", "action", "details", "timestamp"])
    finally:
        conn.close()
    return df


def parse_ocr_text_to_row(ocr_text: str, column_names: list) -> dict:
    """Parses extracted OCR text into matching columns using regex patterns."""
    extracted = {col: "" for col in column_names}
    lines = [line.strip() for line in ocr_text.split("\n") if line.strip()]

    date_pattern = r'\b(\d{1,4}[-/\.]\d{1,2}[-/\.]\d{1,4})\b'
    amount_pattern = r'(\$?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d+)?)'

    found_amounts = []
    for line in lines:
        date_match = re.search(date_pattern, normalize_digits(line))
        if date_match and not any(extracted[c] for c in column_names if "date" in str(c).lower()):
            for c in column_names:
                if "date" in str(c).lower():
                    extracted[c] = date_match.group(1)
                    break
        for amt in re.findall(amount_pattern, normalize_digits(line)):
            val = to_num(amt)
            if val and val > 0 and not re.search(date_pattern, amt):
                found_amounts.append(val)

    if found_amounts:
        max_val = max(found_amounts)
        for c in column_names:
            c_low = str(c).lower()
            if any(term in c_low for term in ["receipt", "income", "credit", "amount", "payment", "expense", "debit"]):
                extracted[c] = fmt_num(max_val)
                break

    for c in column_names:
        c_low = str(c).lower()
        if any(term in c_low for term in ["particular", "description", "details", "item", "name"]):
            for line in lines:
                if not re.search(date_pattern, normalize_digits(line)) and not any(fmt_num(a) in normalize_digits(line) for a in found_amounts):
                    extracted[c] = line[:80]
                    break
            break
    return extracted


init_db()

# ==========================================
# --- 4. SESSION STATE (single source of truth)
# ==========================================
_defaults = {
    "loaded_sheets": {},       # {sheet_name: DataFrame of clean strings}  <- the ONE source of truth
    "sheet_versions": {},      # {sheet_name: int} bumps widget keys so editors reload fresh data
    "file_name": "",
    "loaded_sig": "",          # hash of the uploaded file already loaded (prevents re-loading on every rerun)
    "uploader_version": 0,
    "ocr_extracted_text": "",
    "editor_key_version": 0,
    "recent_added_flag": False,
    "flash": [],
    "pending_db_crud": False,
    "last_db_crud_summary": {},
    "workbook_save_path": "",
    "pending_notifications": [],
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


def bump_editor_key():
    st.session_state.editor_key_version += 1


def sheet_ver(sname):
    return st.session_state.sheet_versions.get(sname, 0)


def commit_sheet(sname, df):
    """Commit sheet data and automatically recalculate Cash in Hand for the complete sheet."""
    cleaned = calculate_cash_in_hand(tidy_df(df))
    st.session_state.loaded_sheets[sname] = cleaned
    st.session_state.sheet_versions[sname] = sheet_ver(sname) + 1


def flash(msg):
    st.session_state.flash.append(msg)


def show_flash():
    msgs, st.session_state.flash = st.session_state.flash, []
    for m in msgs:
        st.success(m)


def next_serial(df):
    sr_cols = [c for c in df.columns if is_serial_col(c)]
    if not sr_cols:
        return ""
    nums = df[sr_cols[0]].map(to_num).dropna()
    return int(nums.max()) + 1 if not nums.empty else len(df) + 1


def build_new_row(df, inputs):
    """Build a new row. Cash in Hand is recalculated for the whole sheet by commit_sheet()."""
    row = {c: str(inputs.get(c, "")).strip() for c in df.columns}
    for c in df.columns:
        if row[c] != "":
            numeric_value = to_num(row[c])
            if numeric_value is not None and not is_id_like(c):
                row[c] = fmt_num(numeric_value)
    return row


def render_add_row_form(sname, prefix):
    df = st.session_state.loaded_sheets[sname]
    cols = list(df.columns)
    if not cols:
        st.info("This sheet has no columns.")
        return
    ver = sheet_ver(sname)
    nxt = next_serial(df)
    today = datetime.date.today()

    with st.form(f"{prefix}_form_{sname}_{ver}", clear_on_submit=True):
        grid = st.columns(min(len(cols), 4))
        inputs, defaults = {}, {}
        for i, c in enumerate(cols):
            low = str(c).lower()
            default = ""
            if is_serial_col(c) and nxt != "":
                default = str(nxt)
            elif "date" in low:
                default = today.strftime("%Y-%m-%d")
            elif "month" in low:
                default = today.replace(day=1).strftime("%Y-%m-%d")
            defaults[c] = default
            inputs[c] = grid[i % 4].text_input(c, value=default, key=f"{prefix}_{sname}_{ver}_{i}")
        submitted = st.form_submit_button(f"💾 Append Row into '{sname}' Tab", use_container_width=True)

    if submitted:
        if not any(str(v).strip() and str(v).strip() != defaults[c] for c, v in inputs.items()):
            st.warning("Please enter data in at least one field before submitting.")
            return
        new_row = build_new_row(df, inputs)
        updated = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        commit_sheet(sname, updated)
        log_system_event("EXCEL_ROW_ADD", f"Added row to sheet '{sname}'")
        flash(f"✅ Row added to '{sname}'. It now has {len(updated)} rows — table, sidebar and dashboard are updated.")
        # Auto-email all active users if this row has a receipt/payment amount.
        # Read the row back from the committed sheet so it includes the recalculated Cash in Hand.
        final_row = st.session_state.loaded_sheets[sname].iloc[-1].to_dict()
        auto_notify_new_row(sname, final_row)
        st.rerun()


def render_sheet_grid(sname, prefix):
    """Excel-like staged CRUD editor for uploaded workbook sheets: edit, add, delete, then save."""
    base = st.session_state.loaded_sheets[sname].copy()
    work = base.copy()
    work.insert(0, "_delete", False)

    edited = st.data_editor(
        work,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key=f"{prefix}_grid_{sname}_v{sheet_ver(sname)}",
        column_config={
            "_delete": st.column_config.CheckboxColumn(
                "🗑️ Delete",
                help="Tick this row and then press Save Changes Permanently."
            )
        },
    )

    clean = tidy_df(edited.drop(columns=["_delete"], errors="ignore"))
    delete_mask = (
        edited["_delete"].fillna(False).astype(bool)
        if "_delete" in edited.columns
        else pd.Series(False, index=edited.index)
    )
    changed = not frames_equal(clean, base) or bool(delete_mask.any()) or len(clean) != len(base)

    if not changed:
        return

    st.warning("⚠️ Unsaved changes detected. Review them and press **Save Changes Permanently**.")
    save_col, cancel_col = st.columns([3, 1])

    with save_col:
        save_clicked = st.button(
            "💾 Save Changes Permanently",
            key=f"save_excel_crud_{prefix}_{sname}_{sheet_ver(sname)}",
            use_container_width=True,
            type="primary",
        )
    with cancel_col:
        cancel_clicked = st.button(
            "↩️ Cancel",
            key=f"cancel_excel_crud_{prefix}_{sname}_{sheet_ver(sname)}",
            use_container_width=True,
        )

    if cancel_clicked:
        bump_editor_key()
        st.rerun()

    if not save_clicked:
        return

    try:
        original_df = base.copy()

        deleted_count = int(delete_mask.sum())
        if delete_mask.any():
            clean = clean.loc[~delete_mask].reset_index(drop=True)

        receipt_col, payment_col, balance_col = get_cash_columns(clean)

        financial_changes = []
        if receipt_col or payment_col:
            max_rows = max(len(original_df), len(clean))
            for row_idx in range(max_rows):
                old_row = original_df.iloc[row_idx] if row_idx < len(original_df) else None
                new_row = clean.iloc[row_idx] if row_idx < len(clean) else None

                old_receipt = (to_num(old_row[receipt_col]) or 0
                              if old_row is not None and receipt_col and receipt_col in old_row else 0)
                old_payment = (to_num(old_row[payment_col]) or 0
                              if old_row is not None and payment_col and payment_col in old_row else 0)
                new_receipt = (to_num(new_row[receipt_col]) or 0
                              if new_row is not None and receipt_col and receipt_col in new_row else 0)
                new_payment = (to_num(new_row[payment_col]) or 0
                              if new_row is not None and payment_col and payment_col in new_row else 0)

                if old_receipt != new_receipt or old_payment != new_payment:
                    financial_changes.append({
                        "row_index": row_idx,
                        "old_receipt": old_receipt, "new_receipt": new_receipt,
                        "old_payment": old_payment, "new_payment": new_payment,
                    })

        clean = calculate_cash_in_hand(clean)
        commit_sheet(sname, clean)

        path = save_workbook_permanently(st.session_state.loaded_sheets, st.session_state.file_name)
        st.session_state.workbook_save_path = path

        if financial_changes:
            for change in financial_changes:
                row_idx = change["row_index"]
                if row_idx >= len(clean):
                    continue
                row_data = clean.iloc[row_idx].to_dict()
                auto_notify_new_row(sname, row_data)

        flash(
            f"✅ Changes to '{sname}' saved permanently. Deleted {deleted_count} row(s). "
            "Cash in Hand recalculated for the complete sheet."
        )
        if financial_changes:
            flash(f"📧 {len(financial_changes)} financial change(s) detected — choose who to notify in the popup.")

        st.rerun()

    except Exception as ex:
        st.error(f"Could not save workbook changes: {ex}")


# ==========================================
# --- 5. FILE UPLOAD (loads ONLY when the file is new)
# ==========================================
def handle_workbook_upload(uploaded):
    data = uploaded.getvalue()
    sig = hashlib.md5(data).hexdigest()
    if sig == st.session_state.loaded_sig:
        return  # already loaded -> do NOT overwrite user's added/edited rows
    try:
        sheets = load_workbook_sheets(data, uploaded.name)
    except Exception as e:
        st.error(f"Error parsing uploaded file: {e}")
        return
    st.session_state.loaded_sheets = {
        k: calculate_cash_in_hand(tidy_df(v)) if not v.empty else v
        for k, v in sheets.items()
    }
    st.session_state.sheet_versions = {k: 0 for k in sheets}
    st.session_state.file_name = uploaded.name
    st.session_state.loaded_sig = sig
    bump_editor_key()
    log_system_event("EXCEL_UPLOAD", f"Uploaded file: {uploaded.name}")
    flash(f"Workbook '{uploaded.name}' loaded successfully! Total Sheet Tabs Detected: {len(sheets)}")
    st.rerun()


# ==========================================
# --- 6. SIDEBAR ---------------------------
# ==========================================
with st.sidebar:
    # --- CSS for identical box sizes and rounded edges ---
    st.markdown(
        """
        <style>
        /* Force container and labels to span full sidebar width */
        div[data-testid="stRadio"] {
            width: 100% !important;
        }
        div[data-testid="stRadio"] > div {
            width: 100% !important;
        }
        
        /* Style individual radio option cards */
        div[data-testid="stRadio"] label[data-baseweb="radio"] {
            width: 100% !important;
            height: 60px !important;            /* Equal fixed height for all boxes */
            border-radius: 12px !important;     /* Smooth rounded corners */
            border: 1px solid #374151 !important;/* Subtle border */
            background-color: #1F2937 !important;/* Matching box background */
            padding: 10px 14px !important;
            margin-bottom: 8px !important;
            display: flex !important;
            align-items: center !important;
            box-sizing: border-box !important;
            transition: all 0.2s ease-in-out;
        }

        /* Hover effect for interactive feedback */
        div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
            border-color: #4B5563 !important;
            background-color: #374151 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown("## ⚙️ Workspace Control")
    st.markdown("## 🧭 Navigate")
    
    st.radio(
        "Navigate",
        [
            "📋 Data Sheet Manager",
            "📈 Interactive Dashboard",
            "📂 Excel Workbooks & OCR Scanner",
            "👥 User Directory",
            "⚙️ System Preferences & Audit Logs",
        ],
        key="main_nav_choice",
        label_visibility="collapsed",
    )
    st.markdown("---")

    if st.session_state.loaded_sheets:
        st.success(f"📂 Active Excel File:\n`{st.session_state.file_name}`")
        st.info(f"📊 Sheets Loaded: **{len(st.session_state.loaded_sheets)}**")

        st.markdown("### 📄 Sheet Summary")
        for sname, sdf in st.session_state.loaded_sheets.items():
            st.markdown(f"- **{sname}**: `{len(sdf)}` rows")

        st.markdown("---")
        st.markdown("### 💾 Export & Download")
        st.download_button(
            label="📥 Save & Download Full Excel",
            data=generate_excel_bytes(st.session_state.loaded_sheets),
            file_name=(st.session_state.file_name.rsplit(".", 1)[0] + ".xlsx") if st.session_state.file_name else "Updated_Kumaitu_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="sb_download_excel_btn"
        )
        if st.session_state.get("workbook_save_path"):
            st.success(f"💾 Permanently saved: `{os.path.basename(st.session_state.workbook_save_path)}`")
    else:
        st.warning("No Excel workbook loaded. Working with local SQLite Database.")


    
    if st.button(" Reload Local DB Data", use_container_width=True):
        bump_editor_key()
        st.rerun()

    if st.session_state.loaded_sheets:
        if st.button(" Clear Uploaded Workbook", use_container_width=True):
            st.session_state.loaded_sheets = {}
            st.session_state.sheet_versions = {}
            st.session_state.file_name = ""
            st.session_state.loaded_sig = ""
            st.session_state.uploader_version += 1
            bump_editor_key()
            flash("Workbook cleared from session.")
            st.rerun()

    st.markdown("---")
    st.caption("Kumaitu System v3.4 • High-Performance Framework")

show_flash()

# ==========================================
# --- 6.5 NOTIFICATION CHOICE POPUP --------
# ==========================================
def render_notification_prompt():
    """Shared UI for choosing recipients before any pending change is emailed."""
    pending = st.session_state.pending_notifications
    st.write(f"**{len(pending)} financial change(s)** are ready to notify:")
    for item in pending[:8]:
        row = item["row_dict"]
        particular_col = find_col(row.keys(), "particular") or find_col(row.keys(), "name")
        particular = cell_to_str(row.get(particular_col, "")) if particular_col else ""
        receipt = (to_num(row.get(item.get("receipt_col"), "")) or 0) if item.get("receipt_col") else 0
        payment = (to_num(row.get(item.get("payment_col"), "")) or 0) if item.get("payment_col") else 0
        st.caption(f"• {item['source_name']} — {particular or '(no name)'} — Receipt {receipt:,.2f} / Payment {payment:,.2f}")
    if len(pending) > 8:
        st.caption(f"...and {len(pending) - 8} more.")

    users_df = get_users_df()
    active_users = users_df[users_df["active"] == 1] if not users_df.empty else users_df
    active_users = active_users[active_users["email"].astype(str).str.contains("@")] if not active_users.empty else active_users

    if active_users.empty:
        st.warning("No active users with an email are configured in the User Directory. Add one there first, or discard this notification.")
        if st.button("Close without sending", use_container_width=True, key="notify_close_no_users"):
            st.session_state.pending_notifications = []
            st.rerun()
        return

    mode = st.radio(
        "Who should receive this notification?",
        ["Send to all registered users (everyone in Cc)", "Choose specific user(s) (selected as To, others as Cc)"],
        key="notify_mode_choice",
    )

    all_emails = active_users["email"].tolist()
    labels = [f'{(r["name"] or "(no name)")} <{r["email"]}>' for _, r in active_users.iterrows()]
    label_to_email = dict(zip(labels, all_emails))

    to_emails, cc_emails = [], list(all_emails)
    if mode.startswith("Choose specific"):
        chosen_labels = st.multiselect("Select recipient(s) to put in To:", labels, key="notify_specific_users")
        to_emails = [label_to_email[l] for l in chosen_labels]
        cc_emails = [e for e in all_emails if e not in to_emails]

    col_send, col_discard = st.columns(2)
    with col_send:
        send_disabled = mode.startswith("Choose specific") and not to_emails
        if st.button("📤 Send notification", type="primary", use_container_width=True, disabled=send_disabled):
            subject, body = build_batch_notification(pending)
            success, message = send_email_notification(subject, body, to_list=to_emails, cc_list=cc_emails)
            st.session_state.pending_notifications = []
            flash(f"📧 {message}" if success else f"⚠️ Notification failed: {message}")
            st.rerun()
        if send_disabled:
            st.caption("Select at least one recipient for To.")
    with col_discard:
        if st.button("🚫 Don't send", use_container_width=True, key="notify_discard"):
            st.session_state.pending_notifications = []
            flash("Notification discarded — no email was sent.")
            st.rerun()


if st.session_state.get("pending_notifications"):
    if hasattr(st, "dialog"):
        @st.dialog("📧 Send notification for recent changes?")
        def _pending_notification_dialog():
            render_notification_prompt()
        _pending_notification_dialog()
    else:
        # Fallback for Streamlit versions without st.dialog: an inline prompt instead of a popup.
        with st.container(border=True):
            st.markdown("### 📧 Send notification for recent changes?")
            render_notification_prompt()

# ==========================================
# --- 7. MAIN NAVIGATION (SIDEBAR MENU) ----
# ==========================================
NAV_SECTIONS = [
    "📋 Data Sheet Manager",
    "📈 Interactive Dashboard",
    "📂 Excel Workbooks & OCR Scanner",
    "👥 User Directory",
    "⚙️ System Preferences & Audit Logs",
]
nav_choice = st.session_state.get("main_nav_choice", NAV_SECTIONS[0])

# ==============================================================================
# --- SECTION 1: DATA SHEET & ENTRY MANAGEMENT --------------------------------
# ==============================================================================
if nav_choice == NAV_SECTIONS[0]:
    st.subheader("📋 Data Sheet & Entry Management Engine")

    has_excel = len(st.session_state.loaded_sheets) > 0
    working_modes = ["SQLite Local Database"]
    if has_excel:
        working_modes = ["Uploaded Excel Workbook", "SQLite Local Database"]

    ds_mode = st.radio("Select Active Data Workspace Mode:", working_modes, horizontal=True, key="ds_working_mode_radio")
    st.markdown("---")

    if ds_mode == "SQLite Local Database":
        st.markdown("### ➕ Append Entry to SQLite Local Database")
        display_cols = DB_COLUMNS

        with st.form("add_db_entry_form", clear_on_submit=True):
            form_cols = st.columns(4)
            inputs = {}
            for idx, col_name in enumerate(display_cols):
                with form_cols[idx % 4]:
                    label = col_name.replace("_", " ").title()
                    if col_name == "entry_date":
                        inputs[col_name] = st.date_input("Entry Date", datetime.date.today(), key=f"db_in_{col_name}")
                    else:
                        inputs[col_name] = st.text_input(label, key=f"db_in_{col_name}")
            submit_db_btn = st.form_submit_button("💾 Commit New Record to Database", use_container_width=True)

            if submit_db_btn:
                formatted = {}
                for k, v in inputs.items():
                    if k == "entry_date":
                        formatted[k] = str(v)
                    elif k in ("cash_receipt", "cash_payment", "balance"):
                        formatted[k] = to_num(v) or 0.0
                    else:
                        formatted[k] = str(v).strip() if v else ""
                add_db_entry(formatted)
                bump_editor_key()
                flash("Record written to SQLite Database.")
                auto_notify_new_row("SQLite Database", formatted)
                st.rerun()

        st.markdown("---")
        st.markdown("Active Database Records")
        st.caption(
            "Edit any existing cell, add a new row at the bottom, or tick 🗑️ Delete. "
            "Nothing is permanently changed until you press Save Changes Permanently."
        )
        db_records = get_entries_df().fillna("")
        db_edit_df = db_records.copy()
        db_edit_df.insert(0, "_delete", False)

        edited_db_df = st.data_editor(
            db_edit_df,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key=f"sqlite_editor_v{st.session_state.editor_key_version}",
            column_config={
                "id": st.column_config.NumberColumn("Record ID", disabled=True),
                "_delete": st.column_config.CheckboxColumn(
                    "🗑️ Delete",
                    help="Tick this row, then press Save Changes Permanently."
                ),
                "sr_no": st.column_config.TextColumn("SR. #"),
                "entry_date": st.column_config.TextColumn("Date"),
                "particular": st.column_config.TextColumn("Particular / Name"),
                "cash_receipt": st.column_config.NumberColumn("Cash Receipt", format="%.2f"),
                "cash_payment": st.column_config.NumberColumn("Cash Payment", format="%.2f"),
                "balance": st.column_config.NumberColumn("Balance", format="%.2f"),
                "remarks": st.column_config.TextColumn("Remarks"),
            },
        )

        pending_delete = int(
            edited_db_df.get("_delete", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()
        )
        st.caption(f"Current records: {len(db_records)} | Rows marked for deletion: {pending_delete}")

        save_db_col, cancel_db_col = st.columns([3, 1])
        with save_db_col:
            if st.button(
                "💾 Save Changes Permanently",
                key="save_db_grid_btn",
                use_container_width=True,
                type="primary"
            ):
                try:
                    # Snapshot old receipt/payment per record ID so we can tell which
                    # rows are genuinely new or financially changed after saving.
                    old_by_id = {}
                    for _, r in db_records.iterrows():
                        old_by_id[int(r["id"])] = (to_num(r.get("cash_receipt")) or 0, to_num(r.get("cash_payment")) or 0)

                    result = replace_db_entries(edited_db_df)
                    st.session_state.last_db_crud_summary = result
                    st.session_state.pending_db_crud = False
                    bump_editor_key()
                    flash(
                        "✅ Database CRUD saved permanently. "
                        f"Inserted: {result['inserted']} | Updated: {result['updated']} | Deleted: {result['deleted']}. "
                        "Dashboard filters and totals have been refreshed."
                    )

                    # Auto-email for every row that is brand new or whose receipt/payment changed.
                    refreshed = get_entries_df()
                    for _, r in refreshed.iterrows():
                        rid = int(r["id"])
                        new_receipt, new_payment = to_num(r.get("cash_receipt")) or 0, to_num(r.get("cash_payment")) or 0
                        old_receipt, old_payment = old_by_id.get(rid, (0, 0))
                        if new_receipt != old_receipt or new_payment != old_payment:
                            auto_notify_new_row("SQLite Database", r.to_dict())

                    st.rerun()
                except Exception as ex:
                    st.error(f"Database CRUD save failed. No partial changes were saved: {ex}")
        with cancel_db_col:
            if st.button("↩️ Cancel Changes", key="cancel_db_grid_btn", use_container_width=True):
                bump_editor_key()
                st.rerun()

        if st.session_state.last_db_crud_summary:
            r = st.session_state.last_db_crud_summary
            st.success(
                f"Last permanent save → Added: {r.get('inserted', 0)}, "
                f"Updated: {r.get('updated', 0)}, Deleted: {r.get('deleted', 0)}"
            )

    else:
        sheets_dict = st.session_state.loaded_sheets
        sheet_list = list(sheets_dict.keys())

        col_select, col_dl = st.columns([3, 1])
        with col_select:
            active_sheet_name = st.selectbox("🎯 Choose Active Excel Sheet Tab to Edit / Add Data:", sheet_list, key="ds_excel_sheet_select")
        with col_dl:
            st.write(" ")
            st.write(" ")
            st.download_button(
                label="📥 Export Updated Excel",
                data=generate_excel_bytes(sheets_dict),
                file_name=(st.session_state.file_name.rsplit(".", 1)[0] + ".xlsx") if st.session_state.file_name else "Updated_Workbook.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="ds_tab1_download_excel"
            )

        if sheets_dict[active_sheet_name].empty:
            st.info("This sheet is empty.")
        else:
            st.markdown(f"### ➕ Append Entry Row directly to Sheet: `{active_sheet_name}`")
            render_add_row_form(active_sheet_name, "t1")

            st.markdown("---")
            st.markdown(f"### 📄 Live Editable View: `{active_sheet_name}` ({len(sheets_dict[active_sheet_name])} Rows)")
            st.caption("Edit existing cells, add rows, or mark rows for deletion. Changes remain staged until you press Save Changes Permanently.")
            render_sheet_grid(active_sheet_name, "t1")

# ==============================================================================
# --- SECTION 2: INTERACTIVE DASHBOARD ----------------------------------------
# ==============================================================================
elif nav_choice == NAV_SECTIONS[1]:
    st.subheader("📈 Interactive Dashboard & Financial Analytics")

    db_df = get_entries_df()
    has_excel = len(st.session_state.loaded_sheets) > 0
    sources = ["SQLite Local Database"]
    if has_excel:
        sources = [f"Uploaded Excel Workbook ({st.session_state.get('file_name', '')})", "SQLite Local Database"]

    selected_source = st.radio("Select Active Data Source for Dashboard Analytics:", sources, horizontal=True, key="dash_data_source_radio")
    target_df = pd.DataFrame()

    if selected_source.startswith("Uploaded Excel"):
        sheets_dict = st.session_state.loaded_sheets
        options = list(sheets_dict.keys()) + ["(All Sheets Combined)"]
        sheet_selection = st.selectbox("🔎 Select Specific Excel Sheet or Consolidated View:", options, key="dash_sheet_selectbox")

        if sheet_selection == "(All Sheets Combined)":
            st.caption("⚠️ Combined view adds all sheets together — summary sheets may double-count transactions.")
            combined = []
            for sname, sdf in sheets_dict.items():
                if sdf.empty:
                    continue
                temp = sdf.copy()
                temp["_Sheet_Tab"] = sname
                combined.append(temp)
            target_df = pd.concat(combined, ignore_index=True) if combined else pd.DataFrame()
        else:
            target_df = sheets_dict[sheet_selection].copy()
    else:
        target_df = db_df.copy()

    if not target_df.empty:
        target_df = tidy_df(target_df)
        target_df = target_df[~(target_df.drop(columns=[c for c in target_df.columns if str(c).startswith("_")], errors="ignore")
                                .apply(lambda col: col.str.strip()) == "").all(axis=1)].reset_index(drop=True)

    st.markdown("---")
    st.markdown("### 🔎 Dynamic Filter & Search Engine")

    if target_df.empty:
        st.info("No records present in the selected dataset to display metrics.")
    else:
        col_search, col_ms = st.columns([1, 1])
        available_cols = [c for c in target_df.columns if not str(c).startswith("_")]

        with col_search:
            search_term = st.text_input("Global Search Keyword across all fields (English / Urdu):",
                                        placeholder="e.g. Office Supplies, Danish, محمد, 2026...", key="dash_search_keyword")
        with col_ms:
            st.markdown("**Specific / Group-wise Filters**")
            filterable_cols = [c for c in available_cols if not str(c).startswith("_")]
            default_filters = []
            for candidate in (
                find_col(filterable_cols, "type"),
                find_col(filterable_cols, "name"),
                find_col(filterable_cols, "particular"),
                find_col(filterable_cols, "date")
            ):
                if candidate and candidate not in default_filters:
                    default_filters.append(candidate)
                if len(default_filters) >= 2:
                    break
            if len(default_filters) < 2:
                default_filters = filterable_cols[:2]
            selected_filter_cols = st.multiselect(
                "Select filter columns (minimum 2 available):",
                filterable_cols,
                default=default_filters,
                key="dash_filter_columns_ms"
            )

        st.caption(
            "The dashboard is calculated ONLY from the records matching the search and selected filters. "
            "English and Urdu text are supported."
        )
        filtered_df = target_df.copy()

        if search_term and search_term.strip():
            terms = normalize_text(search_term).split()
            norm = filtered_df[filterable_cols].apply(lambda col: col.map(normalize_text))
            mask = pd.Series(True, index=filtered_df.index)
            for t in terms:
                mask &= norm.apply(lambda col: col.str.contains(t, regex=False)).any(axis=1)
            filtered_df = filtered_df[mask]

        if selected_filter_cols:
            filter_grid = st.columns(min(max(len(selected_filter_cols), 2), 4))
            for idx, fc in enumerate(selected_filter_cols):
                unique_vals = sorted([
                    str(x) for x in target_df[fc].dropna().unique()
                    if str(x).strip() != "" and str(x).lower() != "none"
                ])
                if unique_vals:
                    with filter_grid[idx % len(filter_grid)]:
                        chosen = st.multiselect(
                            f"Filter {idx + 1}: `{fc}`",
                            unique_vals,
                            key=f"df_filter_val_{fc}"
                        )
                        if chosen:
                            filtered_df = filtered_df[filtered_df[fc].astype(str).isin(chosen)]

        st.info(f"🔎 Filtered result: {len(filtered_df)} of {len(target_df)} records")

        st.markdown("---")
        st.markdown("### 📊 Dynamic Metric Cards Summary")

        # Cash in Hand / Balance columns are intentionally excluded from the cards
        # below - permanently. The Net (Receipt - Payment) card already represents
        # this figure, so neither a "Total Cash in Hand" nor a "Closing Cash in
        # Hand" card is ever generated.
        totals = {}
        for col in available_cols:
            if is_id_like(col) or not col_is_numeric(filtered_df[col]):
                continue
            col_norm = normalize_text(col)
            if "balance" in col_norm or "cash in hand" in col_norm:
                continue
            nums = filtered_df[col].map(to_num)
            if nums.sum() != 0:
                totals[col] = float(nums.sum())

        rec_c = find_col(totals.keys(), "receipt") or find_col(totals.keys(), "income") or find_col(totals.keys(), "credit")
        pay_c = find_col(totals.keys(), "payment") or find_col(totals.keys(), "expense") or find_col(totals.keys(), "debit")

        cards = [(f"Total {k}", v, f"Aggregated across {len(filtered_df)} filtered rows") for k, v in totals.items()]
        if rec_c and pay_c:
            cards.append(("Net (Receipt − Payment)", totals[rec_c] - totals[pay_c], "Receipts minus payments"))

        if cards:
            card_styles = ["card-bg-1", "card-bg-2", "card-bg-3", "card-bg-4", "card-bg-5", "card-bg-6", "card-bg-7", "card-bg-8"]
            per_row = 4
            for i in range(0, len(cards), per_row):
                grid = st.columns(per_row)
                for j, (title, val, sub) in enumerate(cards[i:i + per_row]):
                    grid[j].markdown(
                        f"""
                        <div class="metric-card-container {card_styles[(i + j) % len(card_styles)]}">
                            <div class="metric-card-title">{html.escape(title)}</div>
                            <div class="metric-card-value">{val:,.2f}</div>
                            <div class="metric-card-sub">{html.escape(sub)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.info("No numeric columns auto-detected for total calculation.")

        if HAS_PLOTLY and totals:
            st.markdown("---")
            st.markdown("### 📉 Visual Trend Analysis")
            c1, c2 = st.columns(2)
            chart_df = pd.DataFrame(list(totals.items()), columns=["Metric Column", "Calculated Total"])
            with c1:
                fig_bar = px.bar(chart_df, x="Metric Column", y="Calculated Total", color="Metric Column",
                                 title="Financial Totals Comparison", template="plotly_white")
                fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_bar, use_container_width=True)
            with c2:
                fig_pie = px.pie(chart_df, names="Metric Column", values="Calculated Total", hole=0.4,
                                 title="Proportional Metric Distribution", template="plotly_white")
                fig_pie.update_layout(margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_pie, use_container_width=True)

            date_c = find_col(available_cols, "date")
            money_cols = [c for c in (rec_c, pay_c) if c]
            if date_c and money_cols:
                tmp = filtered_df[[date_c] + money_cols].copy()
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    tmp["_d"] = pd.to_datetime(tmp[date_c].map(normalize_digits), errors="coerce")
                tmp = tmp.dropna(subset=["_d"])
                if not tmp.empty:
                    tmp["Month"] = tmp["_d"].dt.to_period("M").astype(str)
                    for c in money_cols:
                        tmp[c] = tmp[c].map(to_num).fillna(0)
                    monthly = tmp.groupby("Month")[money_cols].sum().reset_index()
                    fig_m = px.bar(monthly, x="Month", y=money_cols, barmode="group",
                                   title="Monthly Receipts vs Payments", template="plotly_white")
                    fig_m.update_layout(margin=dict(l=20, r=20, t=40, b=20), legend_title_text="")
                    st.plotly_chart(fig_m, use_container_width=True)

        st.markdown("---")
        st.markdown(f"### 📄 Filtered Data Output ({len(filtered_df)} of {len(target_df)} rows displayed)")
        st.dataframe(filtered_df[available_cols], use_container_width=True, hide_index=True)

# ==============================================================================
# --- SECTION 3: MULTI-SHEET EXCEL LOADER & OCR SCANNER -----------------------
# ==============================================================================
elif nav_choice == NAV_SECTIONS[2]:
    st.subheader("📂 Multi-Sheet Excel Manager & OCR Scanner")
    st.caption("Import complex Excel files with multiple tabs or scan receipt images to extract data directly.")

    st.markdown("### 📤 Upload Multi-Sheet Excel Workbook")
    uploaded_excel = st.file_uploader(
        "Choose an Excel Workbook (.xlsx, .xlsm, .xls) or CSV:",
        type=["xlsx", "xlsm", "xls", "csv"],
        key=f"ocr_excel_uploader_{st.session_state.uploader_version}"
    )
    if uploaded_excel:
        handle_workbook_upload(uploaded_excel)

    if st.session_state.loaded_sheets:
        st.markdown("---")
        sheet_tab_names = list(st.session_state.loaded_sheets.keys())
        sub_tabs = st.tabs([f"📄 {sname}" for sname in sheet_tab_names])

        for idx, sname in enumerate(sheet_tab_names):
            with sub_tabs[idx]:
                df = st.session_state.loaded_sheets[sname]
                st.markdown(f"**Sheet Name:** `{sname}` | **Total Rows:** `{len(df)}` | **Columns:** `{len(df.columns)}`")
                if df.empty:
                    st.info("This sheet is empty.")
                    continue

                st.caption("Detected columns: " + " • ".join(f"`{c}`" for c in df.columns))
                render_sheet_grid(sname, "t3")

                b1, b2 = st.columns([1, 3])
                if b1.button("🧹 Remove empty rows", key=f"btn_clean_{sname}", use_container_width=True):
                    keep = df[~(df.apply(lambda col: col.str.strip()) == "").all(axis=1)]
                    commit_sheet(sname, keep)
                    flash(f"Removed {len(df) - len(keep)} empty row(s) from '{sname}'.")
                    st.rerun()

                with st.expander(f"➕ Quick Add Row to Tab `{sname}`"):
                    render_add_row_form(sname, "t3")

    st.markdown("---")
    st.markdown("### 📷 OCR Invoice & Receipt Document Scanner")
    st.caption("Upload document photos or bill receipts to extract text (English + اردو) and generate entries.")

    uploaded_img = st.file_uploader("Upload Receipt Image for OCR Scanning:", type=["png", "jpg", "jpeg", "bmp"], key="ocr_image_uploader")

    if uploaded_img:
        col_img, col_txt = st.columns([1, 1])
        img = Image.open(uploaded_img)

        with col_img:
            st.image(img, caption="Uploaded Document Preview", use_container_width=True)

        with col_txt:
            if st.button("🔍 Execute OCR Text Extraction", key="extract_ocr_btn", use_container_width=True):
                if not HAS_OCR:
                    st.error("OCR is not available: run `pip install pytesseract` and install the Tesseract program "
                             "(with Urdu language data 'urd'). No data was created.")
                else:
                    try:
                        cmd = os.getenv("TESSERACT_CMD")
                        if cmd:
                            pytesseract.pytesseract.tesseract_cmd = cmd
                        avail = set(pytesseract.get_languages(config=""))
                        langs = "+".join([l for l in ("urd", "eng") if l in avail]) or "eng"
                        st.session_state.ocr_extracted_text = pytesseract.image_to_string(img, lang=langs)
                        st.success(f"OCR Text Extraction Complete! (language: {langs})")
                        if "urd" not in avail:
                            st.warning("Urdu language data ('urd') is not installed, so Urdu text will not be read.")
                    except Exception as ex:
                        st.error(f"OCR Execution Error: {ex}")

            if st.session_state.ocr_extracted_text:
                ocr_text = st.text_area("OCR Extracted Raw Text (you can correct it)", st.session_state.ocr_extracted_text, height=180, key="ocr_text_area")

                st.markdown("#### ⚡ Auto-Convert OCR Output into Table Entry")
                dest_options = ["SQLite Database"] + list(st.session_state.loaded_sheets.keys())
                target_dest = st.selectbox("Select Target Table for OCR Entry:", dest_options, key="ocr_target_dest_select")

                if st.button("🚀 Push OCR Data to Selected Table", use_container_width=True):
                    if target_dest == "SQLite Database":
                        parsed = parse_ocr_text_to_row(ocr_text, DB_COLUMNS)
                        for c in ("cash_receipt", "cash_payment", "balance"):
                            parsed[c] = to_num(parsed[c]) or 0.0
                        add_db_entry(parsed)
                        bump_editor_key()
                        flash("OCR entry written to SQLite Database!")
                        auto_notify_new_row("SQLite Database (OCR)", parsed)
                        st.rerun()
                    else:
                        target_df_ocr = st.session_state.loaded_sheets[target_dest]
                        if target_df_ocr.empty:
                            st.warning("Selected sheet has no columns.")
                        else:
                            parsed = parse_ocr_text_to_row(ocr_text, list(target_df_ocr.columns))
                            new_row = build_new_row(target_df_ocr, parsed)
                            commit_sheet(target_dest, pd.concat([target_df_ocr, pd.DataFrame([new_row])], ignore_index=True))
                            flash(f"OCR entry appended to Excel sheet '{target_dest}'!")
                            final_row = st.session_state.loaded_sheets[target_dest].iloc[-1].to_dict()
                            auto_notify_new_row(target_dest, final_row)
                            st.rerun()

# ==============================================================================
# --- SECTION 4: USER DIRECTORY & NOTIFICATIONS -------------------------------
# ==============================================================================
elif nav_choice == NAV_SECTIONS[3]:
    st.subheader("👥 User Notification Directory & Roles")
    st.caption("Manage system users, email addresses for notification alerts, and access roles.")

    users_df = get_users_df()
    st.markdown("### 📄 Registered User Directory")

    edited_users_df = st.data_editor(
        users_df, num_rows="dynamic", use_container_width=True, hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("User ID", disabled=True),
            "name": st.column_config.TextColumn("Full Name", required=True),
            "email": st.column_config.TextColumn("Email Address", required=True),
            "role": st.column_config.SelectboxColumn("User Role", options=["Administrator", "Finance Manager", "Auditor", "User"]),
            "active": st.column_config.CheckboxColumn("Active Alert Status")
        },
        key="users_data_editor"
    )

    if st.button("💾 Save Directory Changes", key="save_users_btn", use_container_width=True):
        update_users_table(edited_users_df)
        flash("✅ User directory updated successfully!")
        st.rerun()

    st.markdown("---")
    st.markdown("### 📧 Send Direct Notification Alert")

    with st.form("send_email_alert_form", clear_on_submit=True):
        active_users = users_df[users_df["active"] == 1]["email"].tolist() if not users_df.empty else []
        selected_recipients = st.multiselect("Select Email Recipients:", active_users, default=active_users[:1] if active_users else None)
        subject = st.text_input("Notification Subject:", value="Kumaitu System Financial Update")
        body = st.text_area("Message Content:", value="Please review the latest entries and financial updates committed to the Kumaitu system.")

        send_btn = st.form_submit_button("📤 Send Alert Notification", use_container_width=True)
        if send_btn:
            if selected_recipients:
                success, message = send_email_notification(subject, body, to_list=selected_recipients)
                if success:
                    st.success(message)
                else:
                    st.warning(f"Not sent: {message}")
            else:
                st.warning("Please select at least one recipient.")

# ==============================================================================
# --- SECTION 5: SYSTEM PREFERENCES & AUDIT LOGS ------------------------------
# ==============================================================================
elif nav_choice == NAV_SECTIONS[4]:
    st.subheader("⚙️ System Preferences & Audit Log Trail")
    st.caption("Configure environment rules and monitor operational activity logs.")

    col_set1, col_set2 = st.columns(2)
    with col_set1:
        st.markdown("### 🛠 Header Preset Mapping")
        st.text_input("Date Field Variant Names:", value="date, entry_date, transaction_date", key="cfg_col_date")
        st.text_input("Income/Receipt Variant Names:", value="cash receipt, receipt, income, credit", key="cfg_col_rec")
        st.text_input("Expense/Payment Variant Names:", value="cash payment, payment, expense, debit", key="cfg_col_exp")
        st.text_input("Balance Variant Names:", value="balance, net_balance, total", key="cfg_col_bal")

    with col_set2:
        st.markdown("### 🔔 Workspace Operational Rules")
        st.checkbox("Auto-format financial numbers with thousands separator", value=True, key="cfg_auto_format")
        st.checkbox("Enable real-time metric updates on table cell edit", value=True, key="cfg_live_calc")
        st.number_input("Default Data Table Rows Per View:", min_value=10, max_value=1000, value=100, key="cfg_page_rows")

    if st.button("💾 Save System Preferences", key="save_settings_btn", use_container_width=True):
        log_system_event("UPDATE_PREFERENCES", "System configurations updated")
        st.success("System configurations saved successfully!")

    st.markdown("---")
    st.markdown("### 📜 System Activity Audit Trail")
    logs_df = get_logs_df()
    if not logs_df.empty:
        st.dataframe(logs_df, use_container_width=True, hide_index=True)
    else:
        st.info("No audit logs recorded yet.")