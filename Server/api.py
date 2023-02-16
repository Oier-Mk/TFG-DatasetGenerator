from fastapi import FastAPI, Depends, UploadFile, Request, Form, Response
import shutil
import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import List
from uuid import uuid4
from mail_sender.sender import *
from user_management.sessions import *
from database.database import *


#delete_database()

# CREATE APP

app = FastAPI()

# STATIC FILES

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

#LOAD TEMPLATES

templates = Jinja2Templates(directory="templates") 

# LOAD EMAIL CONFIG

envMail = load_email(".env")

envDDBB = "/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.envDDBB"

# HOME

@app.get("/", response_class=HTMLResponse)
async def home(request: Request): return templates.TemplateResponse("home.html", {"request": request})

# LOGIN PAGE


@app.get("/login/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def getLogin(request: Request, session_data: SessionData = Depends(verifier)):
    try: 
        session_data.username
        logout(request, session_data)
    except: pass 
    return templates.TemplateResponse("Login/login.html", {"request": request})


@app.post("/login/", response_class=HTMLResponse)
async def postLogin(request: Request, response: Response, name: str = Form(...), email: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    print(email + " - " + password)
    if user_exists(envDDBB, email):
        if (get_password(envDDBB, email) == password):
            session = uuid4()
            data = SessionData(username=email)
            await backend.create(session, data)
            cookie.attach_to_response(response, session) #TODO get User
            return "correct"
        else:
            return "incorrect"
    else:
        if name == "Name":
            return "singup"
        else:
            session = uuid4()
            data = SessionData(username=email)
            await backend.create(session, data)
            cookie.attach_to_response(response, session)
            print(data.username)
            insert_user(envDDBB, email, name, password)
            return "correct"


@app.get("/correct-login/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def correctLogin(request: Request, session_data: SessionData = Depends(verifier)):
    try: 
        print(session_data.username)
        return templates.TemplateResponse("Login/correctLogin.html", {"request": request, "name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})


@app.get("/correct-singup/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def correctSingup(request: Request, session_data: SessionData = Depends(verifier)):
    try: return templates.TemplateResponse("Login/correctSingup.html", {"request": request, "name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

# LOGOUT

@app.post("/logout/")
async def logout(response: Response, session_id: UUID = Depends(cookie)):
    try:
        await backend.delete(session_id)
        cookie.delete_from_response(response)
    except Exception as e:
        e.printstack()

# UPLOADING IMAGES


@app.get("/uploadImages/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def uploadImages(request: Request, session_data: SessionData = Depends(verifier)):
    try: return templates.TemplateResponse("Cropping/cropImages.html", {"request": request, "name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})


@app.post("/cropImages/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def cropImages(request: Request, session_data: SessionData = Depends(verifier), files: List[UploadFile] = Form(...), sessionName: str = Form(...)):
    if files:
        session_dir = "static" + os.path.sep + os.path.sep + \
            "uploadedPictures" + os.path.sep + session_data.username + \
            os.path.sep + sessionName + os.path.sep
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)

        for i in files:
            print(i.filename)
            with open(session_dir + i.filename, "wb") as buffer:
                buffer.write(i.file.read())
                buffer.close()
        return templates.TemplateResponse("/Utils/confirmation.html", {"request": request})
    else:
        return templates.TemplateResponse("Utils/rejection.html", {"request": request})


# FILE EXPLORER

@app.get("/fileExplorer/{session}", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def fileExplorer(request: Request, session: str, session_data: SessionData = Depends(verifier)):
    try:
        try:
            # muestro las sesiones del usuario
            directory = os.path.join(os.getcwd(), "static",
                                    "uploadedPictures", session_data.username)
            sessions = []
            for f in os.listdir(directory):
                if (f != ".DS_Store"):
                    sessions.append(f)

            # por defecto muestro la primera sesion del usuario.
            if (session != "ftm"):
                for f in os.listdir(directory):
                    if (f == session):
                        folder_path = os.path.join(directory, f)
                        folder = os.listdir(folder_path)
                        break
            else:
                for f in os.listdir(directory):
                    if (f != ".DS_Store"):
                        folder_path = os.path.join(directory, f)
                        folder = os.listdir(folder_path)
                        break

            folder_path = folder_path.split("static/")[1]

            folder = [folder_path + os.path.sep + file for file in folder]

            for i in folder:
                if i.endswith('.DS_Store'):
                    folder.remove(i)

            n = 3
            folder = [folder[i:i+n] for i in range(0, len(folder), n)]

            return templates.TemplateResponse("FileExplorer/fileExplorer.html", {"request": request, "sessions": sessions, "folder": folder, "user_name": session_data.username})
        except: return templates.TemplateResponse("Utils/noFiles.html", {"request": request, "user_name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

# DOWNLOAD BUTTON


@app.get("/download/{session}", dependencies=[Depends(cookie)])
async def download(request: Request, session: str, session_data: SessionData = Depends(verifier)):
    try:
        if (session == "ftm"):
            session = os.listdir(os.path.join(
                os.getcwd(), "static", "uploadedPictures", session_data.username))[0]
        if (session != "ftm"):

            folder_path = os.path.join(
                os.getcwd(), "static", "uploadedPictures", session_data.username, session)

            zip_path = os.path.join(
                os.getcwd(), "static", "uploadedPictures", "compressed", session_data.username)
            if not os.path.exists(zip_path):
                os.makedirs(zip_path)
            zip_path = os.path.join(os.getcwd(
            ), "static", "uploadedPictures", "compressed", session_data.username, session)

            shutil.make_archive(zip_path, "zip", folder_path)

            return Response(content=open(zip_path+".zip", 'rb').read(), media_type="application/zip")
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

# TRAINING PHASE


@app.get("/train/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def getTrain(request: Request, session_data: SessionData = Depends(verifier)):
    try:
        try:
            # muestro las sesiones del usuario
            directory = os.path.join(
                os.getcwd(), "static", "uploadedPictures", session_data.username)
            sessions = []
            for f in os.listdir(directory):
                if (f != ".DS_Store"):
                    sessions.append(f)
            return templates.TemplateResponse("Training/training.html", {"request": request, "sessions": sessions})
        except: return templates.TemplateResponse("Utils/noFiles.html", {"request": request, "user_name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})


@app.post("/train/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def postTrain(request: Request, session_data: SessionData = Depends(verifier), 
session : str = Form(...), 
resume_training : str = Form(...),  
unet_training : str = Form(...), 
unet_learning : str = Form(...), 
encoder_training : str = Form(...), 
concept_training : str = Form(...), 
encoder_learning : str = Form(...), 
style : str = Form(...)):
    try:
        session_data.username
        try:
            print(session) 
            print(resume_training)
            print(unet_training)
            print(unet_learning) 
            print(encoder_training)
            print(concept_training)
            print(encoder_learning)
            print(style) 

            await send_email(envMail, session_data.username, "Training completed", "Your training has been completed. You can now use the application.")

            # TODO: proceder a entrenar

            return "correcto"

        except: "incorrecto"
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})
