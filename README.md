# Kumaitu System

A ready-to-run Python/Streamlit system for:

- Excel-style manual data entry
- Dynamic columns
- Dashboard that automatically expands when a column is added
- Multiple filters (including at least 2 filter fields)
- English + Urdu search
- Urdu data entry in any text field/column
- Language selector for English / اردو interface hints
- Monthly received-money totals
- Expense totals
- Remaining balance = total received - total expenses
- Automatic email to the person when a "Received" entry is saved
- Automatic expense email to all active notification users
- SQLite database (no separate database server required)
- Excel export-ready data structure

## 1. Install Python

Install Python 3.11+ on Windows.

Check:

```powershell
python --version
```

## 2. Open the project folder

```powershell
cd kumaitu_system
```

## 3. Create a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

## 4. Install packages

```powershell
pip install -r requirements.txt
```

## 5. Configure email

Copy:

`.env.example` → `.env`

For Gmail, use a Google App Password. Do not put your normal Gmail password in the file.

Example:

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=your_email@gmail.com
SMTP_USE_TLS=true
```

## 6. Run

```powershell
streamlit run app.py
```

The browser will open the Kumaitu System.

## How to use

### Data Sheet

Enter rows like:

| Date | Type | Person | Email | Amount | Purpose |
|---|---|---|---|---:|---|
| 2026-09-20 | Received | Ali | ali@example.com | 50000 | Monthly payment |
| 2026-09-20 | Expense | Office | | 10000 | Electricity |

When a Received row is saved, an email is sent to the Email in that row.

When an Expense row is saved, an email is sent to every active user under Users.

### Dashboard

The dashboard calculates:

- Total Received
- Total Expense
- Remaining Balance
- Monthly summary

Search works across all columns, including Urdu text.

Choose multiple filter columns and filter values to get specific/group-wise records.

### Dynamic columns

Go to:

`Columns & Settings → Add Column`

For example:

- Department
- Month
- CNIC
- Project
- Urdu Name
- Payment Method
- Reference No.

The new column automatically appears in the data-entry sheet and dashboard.

## Important production note

The included app is a working local/internal version. Before putting it on a public hospital/company server, add:

- Login/authentication
- User roles
- Audit log
- Backup/restore
- HTTPS
- Permission control
- Email queue/retry
- Database server such as PostgreSQL
- Protection against duplicate notifications
- Data validation and approval workflow

## Database

The SQLite database is automatically created here:

`data/kumaitu.db`

Back up this file regularly.


## Urdu support

The system supports Unicode Urdu data. You can type Urdu directly into the Excel-style grid, for example:

- Person: محمد علی
- Purpose: ماہانہ رقم وصول ہوئی
- Notes: ستمبر کی ادائیگی

The Dashboard search searches Urdu and English text across all columns. The search is case-insensitive for English and Unicode-compatible for Urdu.
