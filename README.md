# family-sun
This repo generates a Plotly sunburst graph from a GEDCOM file (I really like genealogy and wanted to be able to generate pretty sunburst chart to display my lineage).

## How-to use
This project uses FastAPI with python 3.10 for the backend and Vite + React for the frontend.

```
docker-compose up
```
The front is then accessible at `http://localhost:3000`.

## Caveat
It does _not_ handle homonyms, so if you happen to have some in your GEDCOM file, I advise you to add Jr. or Sr. so that each individual's name can be truly unique.
