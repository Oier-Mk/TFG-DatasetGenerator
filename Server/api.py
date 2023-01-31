from fastapi import FastAPI, Depends, UploadFile, Request, Form, Response
import shutil
import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import List
from user_management.sessions import *
from uuid import uuid4

relative = os.getcwd()
users = {}
users["oime3564@gmail.com"] = ["Oier", "oime3564@gmail.com", "1234"]
users["oime6435@gmail.com"] = ["Oier", "oime6435@gmail.com", "1234"]

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


@app.post("/login/", response_class=HTMLResponse)
async def check_login(request: Request, response: Response, name: str = Form(...), email: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    print(email +" - "+ password)
    if email in users: 
        if(users[email][2] == password): 
            session = uuid4()
            data = SessionData(username=email)
            await backend.create(session, data)
            cookie.attach_to_response(response, session)
            return "correct"
        else: 
            return "incorrect"
    else:
        if name == "Name":
            return "singup"
        else:
            users[email] = [name, email, password]
            session = uuid4()
            data = SessionData(username=email)
            await backend.create(session, data)
            cookie.attach_to_response(response, session)   
            return "correct"

@app.get("/correct-login/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def uploadImages(request: Request, session_data: SessionData = Depends(verifier)):
    try: return templates.TemplateResponse("Login/correctLogin.html", {"request": request, "name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})
    


@app.get("/correct-singup/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def correct_singup(request: Request, session_data: SessionData = Depends(verifier)):
    try: return templates.TemplateResponse("Login/correctSingup.html", {"request": request, "name": session_data.username})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

# LOGOUT

@app.post("/logout/")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
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
            "uploadedPictures" + os.path.sep + session_data.username + os.path.sep + sessionName + os.path.sep
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)

        for i in files:
            print(i.filename)
            with open(session_dir + i.filename, "wb") as buffer:
                buffer.write(i.file.read())
                buffer.close()
        link = "/Utils/confirmation.html"
    else: 
        link = "Utils/rejection.html"
    # TODO añadir proceso de training de las fotos
    return templates.TemplateResponse(link, {"request": request})


# FILE EXPLORER

@app.get("/fileExplorer/{session}", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def uploadImages(request: Request, session: str, session_data: SessionData = Depends(verifier)):
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

        link = "FileExplorer/fileExplorer.html"
        return templates.TemplateResponse(link, {"request": request, "sessions": sessions, "folder": folder})
    except: return templates.TemplateResponse("Utils/loginPlease.html", {"request": request})

# DOWNLOAD BUTTON

@app.get("/download/{session}", dependencies=[Depends(cookie)])
async def download_zip(request: Request, session: str, session_data: SessionData = Depends(verifier)):
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

@app.get("/trainingParameters/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def uploadImages(request: Request, session_data: SessionData = Depends(verifier)):
    name = "Guest"
    try: name = session_data.username
    except: pass
    return templates.TemplateResponse("Login/correctLogin.html", {"request": request, "name": name})