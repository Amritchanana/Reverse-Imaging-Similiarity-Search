import os
import sys
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Ensure root path is included
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from scripts.query_embedding import get_query_embedding
from search import search_similar

app = FastAPI(title="Reverse Image Search API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/images",
    StaticFiles(directory="data/images_with_product_ids"),
    name="images"
)

# Absolute uploads directory
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def health_check():
    return {"status": "API is running"}


@app.post("/search")
async def search_image(
    file: UploadFile = File(...),
    category: str | None = None
):
    print(f"Search request received with file: {file.filename}", flush=True)
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    # Generate unique filename to avoid overwrite
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    # Save uploaded image
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")

    # Generate query embedding
    try:
        query_emb = get_query_embedding(file_path)
        print(f"Generated embedding shape: {query_emb.shape}")
    except Exception as e:
        print(f"Embedding error: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")

    # Search similar images
    try:
        results = search_similar(query_emb, k=10, category=category)
        print(f"Found {len(results)} results")
    except Exception as e:
        print(f"Search error: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    return {
        "query_image": unique_name,
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)