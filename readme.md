# Outline Resume Parser

A small full-stack app to **upload a resume PDF**, **parse it**, optionally **match it against a job description**, and **view structured JSON output**.

- Backend: **FastAPI**
- Frontend: **React (Vite) + Tailwind CSS + Ant Design**
- Transport: **multipart/form-data**
- Output: **JSON**

---

## Features

- Upload resume PDF
- Parse resume into structured JSON (`/parse`)
- Match resume against job description (`/match`)
- Debug mode for extra output
- Dark mode UI
- Copy / download JSON output
- Health check (`/health`)

---

## Project Structure

```text
outline-resume-parser/
│
├── app/                     # FastAPI app
│   ├── api/
│   │   ├── app.py
│   │   └── routes.py
│   └── ...
│
├── frontend/                # React frontend
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── .venv/                   # Python virtual environment
├── README.md
└── requirements.txt
```

Backend Setup (FastAPI)
1. Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate
2. Install dependencies
pip install -r requirements.txt
3. Run backend
python -m uvicorn app.api.app:app --reload --host 127.0.0.1 --port 8000
4. Verify backend
Health check:
http://127.0.0.1:8000/health

Swagger UI:
http://127.0.0.1:8000/docs

Frontend Setup (React + Tailwind + AntD)
Requirements
Node.js 20.19+ or 22+ (Node 24 LTS works)

npm

Verify:

bash
Copy code
node -v
1. Install frontend dependencies
bash
Copy code
cd frontend
npm install
2. Run frontend dev server
bash
Copy code
npm run dev
Open:

arduino
Copy code
http://localhost:5173
Frontend ↔ Backend Communication
Vite dev proxy forwards:

/health

/parse

/match

No CORS issues in development

Axios timeout set to 5 minutes for long parsing jobs

js
Copy code
timeout: 300000 // 5 minutes
API Endpoints
GET /health
Returns backend status.

json
Copy code
{ "status": "ok" }
POST /parse
Request

file (PDF, required)

debug (boolean, optional)

Response

Parsed resume JSON

POST /match
Request

file (PDF, required)

jd_text (string, optional)

debug (boolean, optional)

Response

Resume + job description matching output

Dark Mode
Ant Design dark algorithm via ConfigProvider

Tailwind-based dark layout

Global dark canvas applied to html, body, and #root

css
Copy code
html,
body,
#root {
  background: #09090b;
  color: #f4f4f5;
}
Notes / Gotchas
Remove default Vite App.css styles (#root { max-width... })
They interfere with full-width dark layouts.

Python venv and Node/npm are completely separate.

Large PDFs or LLM parsing may take time → frontend timeout already increased.

Development Tips
Backend logs show all requests:

text
Copy code
POST /parse 200 OK
POST /match 200 OK
Frontend errors are displayed inline in the UI.

JSON output can be copied or downloaded directly.


## Contributions

Contributions are welcome! Here’s how you can help:

```bash
feat: The new feature youre proposing
fix: A bug fix in the project
style: Feature and updates related to UI improvements and styling
test: Everything related to testing
docs: Everything related to documentation
refactor: Regular code refactoring and maintenance
```