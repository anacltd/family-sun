# family-sun
This repo generates a Plotly sunburst graph from a GEDCOM file (I really like genealogy and wanted to be able to generate pretty sunburst chart to display my lineage).

## Setup
This project uses FastAPI with python 3.10 for the backend and Vite + React for the frontend.

### 1. Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```

### 2. Frontend (Vite + React)
```bash
cd frontend
npm install
npm run dev
```

## Caveat
It does _not_ handle homonyms, so if you happen to have some in your GEDCOM file, I advise you to add Jr. or Sr. so that each individual's name can be truly unique.
