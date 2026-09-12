# Student Management System

## Folder structure

```text
student-management-system/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── supabase.sql
├── render.yaml
└── README.md
```

## Supabase

Run `supabase.sql` in Supabase SQL Editor.

## Backend local setup

Open terminal inside `backend`:

```bash
pip install -r requirements.txt
```

Create `.env` inside `backend`:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_server_side_key
```

Run:

```bash
uvicorn main:app --reload
```

Backend:
`http://127.0.0.1:8000`

API docs:
`http://127.0.0.1:8000/docs`

## Frontend local setup

Open `frontend/index.html`.

For local browser testing, you may need to serve the frontend using a simple local server instead of opening the file directly.

The frontend API URL is in:

`frontend/script.js`

```javascript
const API_URL = "http://127.0.0.1:8000";
```

## GitHub

Upload the complete project folder to one GitHub repository.

Do not upload `.env`.

## Render

The included `render.yaml` deploys the backend.

After Render gives you a URL such as:

`https://student-management-backend.onrender.com`

change `frontend/script.js`:

```javascript
const API_URL = "https://student-management-backend.onrender.com";
```

For production, configure CORS on the backend for your frontend domain.
