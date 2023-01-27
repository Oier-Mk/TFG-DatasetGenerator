from fastapi import FastAPI, File, UploadFile, Request, Form, Query
from typing import Union
import shutil
import os
import io
import cv2
from starlette.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pathlib import Path
from pydantic import BaseModel
from typing import List


relative = os.getcwd()

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

# HOME


@app.get("/", response_class=HTMLResponse)
async def uploadFile(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# LOGIN PAGE


@app.get("/login/", response_class=HTMLResponse)
async def uploadImages(request: Request):
    link = "Login/login.html"
    return templates.TemplateResponse(link, {"request": request})


# LOGIN PAGE
@app.get("/confirmation/", response_class=HTMLResponse)
async def uploadImages(request: Request):
    link = "Utils/confirmation.html"
    return templates.TemplateResponse(link, {"request": request})

# LOGIN PAGE
@app.post("/check-password/", response_class=HTMLResponse)
async def uploadImages(request: Request):
    link = "Utils/confirmation.html"
    return "correct"

# UPLOADING IMAGES
@app.get("/uploadImages/", response_class=HTMLResponse)
async def uploadImages(request: Request):
    link = "Cropping/cropImages.html"
    return templates.TemplateResponse(link, {"request": request})


@app.post("/cropImages/", response_class=HTMLResponse)
async def cropImages(request: Request, files: List[UploadFile] = File(...), sessionName: str = Form(...)):
    if files:
        session_dir = "static" + os.path.sep + \
            "uploadedPictures" + os.path.sep + sessionName
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
        for f in files:
            filename = "static" + os.path.sep + "uploadedPictures" + \
                os.path.sep + sessionName + os.path.sep + f'{f.filename}'
            with open(filename, "wb") as buffer:
                shutil.copyfileobj(f.file, buffer)
        link = "/Utils/confirmation.html"
    else:
        link = "Utils/rejection.html"
    # TODO: add a THE PROCESS FOR THE TRAINING AND
    return templates.TemplateResponse(link,{"request":request})


@app.get("/upload/", response_class=HTMLResponse)
async def uploadImages(request: Request):
    link = "Cropping/uploadImages.html"
    return templates.TemplateResponse(link, {"request": request})

    #     path = "static" + os.path.sep + "ImageTransformator" + os.path.sep + "results" + os.path.sep + function + os.path.sep + file.filename.split('.')[0] + '.txt'
    #     return templates.TemplateResponse("ImageTransformator/returnText.html",{"request":request})
    # return templates.TemplateResponse("ImageTransformator/returnImage.html",{"request":request, "path": path})
