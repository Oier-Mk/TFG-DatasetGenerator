# pytest --cov --disable-pytest-warnings 
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_get_login():
    response = client.get("/login")
    assert response.status_code == 200

def test_post_login():
    response = client.post("/login/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "name": "Name", 
            "email": "oime3564@gmail.com",
            "password": "asdf",
            "password2": "password",
            },
                            )
    
    assert response.status_code == 200
    assert response.text == "correct"

def test_post_singup():
    response = client.post("/login/",
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            data={
                                "name": "Oier", 
                                "email": "oime3564@gmail.com",
                                "password": "asdf",
                                "password2": "asdf",
                                },
                            )
    
    assert response.status_code == 200
    assert response.text == "correct"

def test_get_correctlogin():
    response = client.get("/correct-login")
    assert response.status_code == 200

def test_get_correctsingup():
    response = client.get("/correct-singup")
    assert response.status_code == 200

def test_get_uploadimages():
    response = client.get("/uploadImages")
    assert response.status_code == 200

from starlette.testclient import TestClient
from fastapi import UploadFile
def test_post_crop_images():
    with TestClient(app) as client:
        image_path = "/Users/mentxaka/Github/TFG-DatasetGenerator/Server/static/assets/images/testUpload.png"

        # Create a list of filenames to upload
        filenames = [image_path, image_path, image_path]

        # Create a list of UploadFile objects
        upload_files = []
        for filename in filenames:
            with open(filename, "rb") as f:
                upload_files.append(UploadFile(filename, f))

        response = client.post("/cropImages/",
                    data={
                        "ssession_data" : "username='oime3564@gmail.com'",
                        "files": upload_files,
                        "sessionName": "testsession"
                    }
    
        )


        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")


        # check response status code and text
        # assert response.status_code == 200
        # assert response.text == "correct"

def test_get_fileexplorer():
    response = client.get("/fileExplorer/ftm")
    assert response.status_code == 200

def test_get_download():
    response = client.get("/download/ftm")
    assert response.status_code == 200

def test_get_train():
    response = client.get("/")
    assert response.status_code == 200

def test_post_train():
    response = client.post("/train/",
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            data={
                                "session": "DefaultBiscuits", 
                                "resume_training": "False",
                                "unet_training": "650",
                                "unet_learning": "2E-5",
                                "encoder_training": "250",
                                "concept_training": "0",
                                "encoder_learning": "PNDM",
                                "style": "False"
                                },
                            )
    
    assert response.status_code == 200
    assert response.text == "correct"
    
def test_get_infere():
    response = client.get("/infere")
    assert response.status_code == 200

def test_post_infere():
    response = client.post("/infere/",
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            data={
                                "name": "DefaultBiscuitsNEW", 
                                "model": "DefaultBiscuits",
                                "prompt": "a DefaultBiscuit",
                                "nIterations": "20",
                                "element": "DefaultBiscuit",
                                "scheduler": "PNDM"
                                },
                            )
    
    assert response.status_code == 200

def test_get_generate():
    response = client.get("/generate")
    assert response.status_code == 200

def test_post_generate():
    response = client.post("/generate/",
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            data={
                                "name": "DefaultBiscuitsNEW", 
                                "model": "DefaultBiscuits",
                                "prompt": "a DefaultBiscuit",
                                "nIterations": "20",
                                "nImages": "2",
                                "element": "DefaultBiscuit",
                                "scheduler": "PNDM"
                                },
                            )
    
    assert response.status_code == 200
    assert response.text == "correct"


def test_get_correctgeneration():
    response = client.get("/correct-generation")
    assert response.status_code == 200

def test_get_correcttraining():
    response = client.get("/correct-training")
    assert response.status_code == 200

def test_post_logout():
    response = client.post("/logout/")
    assert response.status_code == 200
