# app/main.py
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .face_service import save_user_image, train_all, recognize_image_bytes, list_users, delete_user, list_models, force_reload_cache

app = FastAPI(title="Face Locker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "b77d74d1a7f4f83fcb134b4d8a09fdcd0a4b4921b739e84de3d6a29e43e1cfb3")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/add-user/{username}")
async def api_add_user(username: str, file: UploadFile = File(...), authorization: str = Header(None)):
    if authorization:
        if not authorization.lower().startswith("bearer ") or authorization.split(" ", 1)[1] != ADMIN_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")
    content = await file.read()
    try:
        saved = save_user_image(username, content)
        force_reload_cache()
        return JSONResponse(status_code=201, content={"saved": saved})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
def api_train(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer ") or authorization.split(" ", 1)[1] != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        results = train_all()
        return {"status": "ok", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recognize")
async def api_recognize(file: UploadFile = File(...)):
    content = await file.read()
    res = recognize_image_bytes(content)
    return res

@app.get("/users")
def api_list_users():
    return {"users": list_users()}

@app.delete("/users/{username}")
def api_delete_user(username: str, authorization: str = Header(None)):
    if authorization:
        if not authorization.lower().startswith("bearer ") or authorization.split(" ", 1)[1] != ADMIN_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")
    ok = delete_user(username)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    force_reload_cache()
    return {"deleted": username}

@app.get("/models")
def api_list_models():
    return {"models": list_models()}
