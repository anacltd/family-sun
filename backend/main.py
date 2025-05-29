from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from utils.process_gedcom import parse_gedcom_to_sunburst

app = FastAPI()

origins = [
    "http://localhost",  # Allow requests from host machine's localhost (any port)
    "http://localhost:3000",  # Explicitly for the React app dev server or mapped Docker port
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_gedcom(
    file: UploadFile = File(...),
    nb_of_generations: int = Form(3),
    color_by: str = Form("generation"),
    palette: str = Form("moss"),
):
    try:
        file_bytes = await file.read()
        sunburst_data = parse_gedcom_to_sunburst(
            file_bytes, nb_of_generations, color_by, palette
        )
        return JSONResponse(content={"data": sunburst_data})

    except Exception as e:
        logger.error(f"Error during upload: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/")
def read_root():
    return {"message": "Hello World!"}
