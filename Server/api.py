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
users = {}
users["oime3564@gmail.com"] = ["Oier","oime3564@gmail.com","1234"]

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

@app.get("/correct-login/", response_class=HTMLResponse)
async def uploadImages(request: Request):
    return templates.TemplateResponse("Login/correctLogin.html", {"request": request})

@app.get("/correct-singup/", response_class=HTMLResponse)
async def uploadImages(request: Request):
    return templates.TemplateResponse("login/correctSingup.html", {"request": request})

@app.post("/check-password/", response_class=HTMLResponse)
async def uploadImages(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    # TODO gestionar base de datos con usuarios
    print(email +" "+ password)
    if (name == "Name" and password2 == "Repeat your password"):
        print("login")
        if(email in users): 
            if (users[email][2] == password): 
                return "correct"
            else: 
                return "incorrect"
        else:
            return "singup"
    else:
        users[email] = [name,email,password]
        print(users[email])
        return "correct"
    
# UPLOADING IMAGES
@app.get("/uploadImages/", response_class=HTMLResponse)
async def uploadImages(request: Request):
    # TODO: comprobar que el usuario se ha logueado y de no ser asi mandarle loguearse
    userLoggedin = True
    if (userLoggedin):
        link = "Cropping/cropImages.html"
        return templates.TemplateResponse(link, {"request": request})
    else:
        #TODO pass message throw variable.
        link = "Utils/rejection.html"
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
    # TODO añadir proceso de training de las fotos
    return templates.TemplateResponse(link,{"request":request})
