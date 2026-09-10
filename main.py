#import backend ------------------------------------------------------------------------------------------------------------
from fastapi import FastAPI

app = FastAPI()




#import object detection model-----------------------------------------------------------------------------------------------
from ultralytics import YOLO

model = YOLO("best.pt")




#import cv2 for croping and text detection----------------------------------------------------------------------------------- 
import cv2
import easyocr

reader = easyocr.Reader(['en'], gpu=True)




#allow react app ------------------------------------------------------------------------------------------------------------
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:5173"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)




#data validation --------------------------------------------------------------------------------------------------------
from pydantic import BaseModel

class codeRemembermebase(BaseModel):      
    code : str
    remember_me : bool

class akauntingUserbase(BaseModel):
    akaunting_email : str
    akaunting_password : str 
    company_name : str

class akauntingDatabase(BaseModel):
    customer : str 
    due_date : str 
    invoice_num : str 
    item01_name : str 
    item01_description : str = None 
    item01_quantity : str 
    item01_price : str 
    item02_name : str 
    item02_description : str = None  
    item02_quantity : str 
    item02_price : str 
    item03_name : str 
    item03_description : str = None  
    item03_quantity : str 
    item03_price : str




#authentication ----------------------------------------------------------------------------------------------------------------
from fastapi.responses import RedirectResponse

@app.get("/login")   #fastapi_route, no need allow google CORSMiddleware
async def login():
    #redirect to my_google_client (google_fill_form, google_auth)
    #redirect to /auth/callback   
    web_client_01 = "https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=591564998629-bumuj9i4tv97cos33jblsetldtb91jl8.apps.googleusercontent.com&redirect_uri=http://localhost:8000/auth/callback&scope=openid email profile&access_type=offline&prompt=consent"
    return RedirectResponse(web_client_01) 




@app.get("/auth/callback")
async def auth_callback(code:str):
    #redirect to frontend
    frontend_url = f"http://localhost:5173/callback?code={code}"
    return RedirectResponse(frontend_url)




import requests
import json
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from datetime import datetime, UTC, timedelta
from jose import jwt 
from fastapi import HTTPException
from fastapi import Response
import os
from dotenv import load_dotenv
load_dotenv()

@app.post("/token")
async def get_token(item:codeRemembermebase, resp:Response):
    token_uri = "https://oauth2.googleapis.com/token"
    data = {
        "code" : item.code,
        "client_id" : os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret" : os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri" : "http://localhost:8000/auth/callback",
        "grant_type" : "authorization_code"
    }

    try:
        #exchange code for google_token
        response = requests.post(token_uri, data=data)
        token = response.json()
        if "id_token" not in token:
            raise HTTPException(status_code=400, detail="Did not have access token")
        #make_sure google_token is google_authed
        payload = id_token.verify_oauth2_token(token["id_token"], google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))

        #jwt_encode + secretkey = jwt_token
        need_encoded = {"sub":payload["email"], "pic":payload["picture"], "first_name":payload["given_name"]}  
        expires_time = datetime.now(UTC).astimezone() + timedelta(hours=1)
        need_encoded.update({"exp": int(expires_time.timestamp())})
        jwt_token = jwt.encode(need_encoded,"b1f3c9a7e4d8f2a1c3b6d7e8f9a0b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f809", algorithm="HS256")

        #clear refresh_token that stored 
        resp.delete_cookie("refresh_token")
        #if remember_me, store refresh_token in browser
        if item.remember_me and "refresh_token" in token:
            resp.set_cookie(key="refresh_token", value=token["refresh_token"], httponly=True, secure=False, samesite="lax")
        #if not remember_me, no refresh_token in browser 
        
        return {"jwt_token":jwt_token, "token_type":"bearer"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Wrong access token")




from fastapi import Request

@app.post("/refresh")
async def refresh_token(req:Request):
    #get refresh_token in browser
    refresh_token = req.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token found")

    token_uri = "https://oauth2.googleapis.com/token"
    data = {
        "refresh_token" : refresh_token,
        "client_id" : os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret" : os.getenv("GOOGLE_CLIENT_SECRET"),
        "grant_type" : "refresh_token"
    }

    try:
        #exchange refresh_token for google_token
        response = requests.post(token_uri, data=data)
        token = response.json()
        if "id_token" not in token:
            raise HTTPException(status_code=400, detail="Did not have access token")
        #make_sure google_token is google_authed
        payload = id_token.verify_oauth2_token(token["id_token"], google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))

        #google_encode must have pic and first_name
        pic = payload.get("picture")
        first_name = payload.get("given_name")
        if not pic or first_name:
            headers = {"Authorization": f"Bearer {token['access_token']}"}
            response = requests.get("https://openidconnect.googleapis.com/v1/userinfo", headers=headers)
            userinfo = response.json()
            pic = userinfo["picture"]
            first_name = userinfo["given_name"]
            payload["picture"] = pic
            payload["given_name"] = first_name 

        #jwt_encode + secretkey = jwt_token
        need_encoded = {"sub":payload["email"], "pic":payload["picture"], "first_name":payload["given_name"]}  
        expires_time = datetime.now(UTC).astimezone() + timedelta(hours=1)
        need_encoded.update({"exp": int(expires_time.timestamp())})
        jwt_token = jwt.encode(need_encoded,"b1f3c9a7e4d8f2a1c3b6d7e8f9a0b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f809", algorithm="HS256")

        return {"jwt_token":jwt_token, "token_type":"bearer"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Fail refresh token")




from fastapi.security import HTTPBearer
header = HTTPBearer()
from fastapi import Depends
from jose import JWTError
from jwt.exceptions import ExpiredSignatureError

async def auth_decode(header = Depends(header)):  
    token = header.credentials
    try:
        #jwt_token - secretkey = jwt_encode
        payload = jwt.decode(token, "b1f3c9a7e4d8f2a1c3b6d7e8f9a0b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f809", algorithms=["HS256"])
        subject = payload.get("sub")
        picture = payload.get("pic")
        first_name = payload.get("first_name")
        return {"subject":subject, "picture":picture, "first_name":first_name}
    except JWTError:   
        raise HTTPException(status_code=401 ,detail="Did not have access token")




#backend development ------------------------------------------------------------------------------------------------------
from fastapi.responses import Response as RawResponse

@app.get("/userinfo")
async def user_info(auth_fetch = Depends(auth_decode)):
    url = auth_fetch["picture"]
    response = requests.get(url)
    content = response.content
    return RawResponse(content)




from Crypto.Cipher import AES
import base64

def decrypt(encrypted_password):
    engine = AES.new("passfgdfg259hkjh".encode("utf-8"), AES.MODE_ECB)
    decrypted_byte = engine.decrypt(base64.b64decode(encrypted_password))
    
    padding = decrypted_byte[-1]
    text_byte = decrypted_byte[:-padding]
    text = text_byte.decode("utf-8")
    return text



 
from fastapi import UploadFile
import numpy as np

@app.post("/object_detection")
async def object_detection(files: list[UploadFile], auth_fetch = Depends(auth_decode)):
    file_list = []
    for file in files:
        #take UploadFile.content, convert to numpy_array_3d, append into list 
        content = await file.read()
        np_arr_1d = np.frombuffer(content, np.uint8)
        np_arr_3d = cv2.imdecode(np_arr_1d, cv2.IMREAD_COLOR)
        file_list.append(np_arr_3d)


    #from predict to n_sub data structure
    class_id_map = {0:'Customer', 1:'Due Date', 2:'Invoice Num', 3:'Item_01 Description', 4:'Item_01 Name', 5:'Item_01 Price', 6:'Item_01 Quantity', 7:'Item_02 Description', 8:'Item_02 Name', 9:'Item_02 Price', 10:'Item_02 Quantity', 11:'Item_03 Description', 12:'Item_03 Name', 13:'Item_03 Price', 14:'Item_03 Quantity'}
    predict = model.predict(source=file_list, save=False, save_txt=False, save_conf=False, project=".", name="yoloignore", exist_ok=True)  
    total_list = []   

    for n, image in enumerate(predict):
        img = file_list[n]
        image_list = {} 

        for detection in image:
            detection_value = detection.boxes.data.tolist()
            for x1, y1, x2, y2, score, class_id in detection_value: 
                x1, y1, x2, y2, class_id = int(x1), int(y1), int(x2), int(y2), int(class_id)
                detection_list = []
                crop_detection = img[y1:y2, x1:x2]
                crop_detection = cv2.cvtColor(crop_detection, cv2.COLOR_BGR2GRAY)

                detection_text = reader.readtext(crop_detection)
                for block, text, score in detection_text:
                    detection_list.append(str(text))

                key = class_id_map[class_id]
                image_list[key] = detection_list   #image_list, sub is detection   #detection is **one key-value-pair**  
                ###image_list[key].extend(detection_list)   #dont overwrite previous_value  

        total_list.append(image_list)   #total_list, sub is image   #image find target
    return total_list




from web_crawl import web_crawl_fnc

@app.post("/invoice_automation")
async def invoice_automation(data_01:akauntingUserbase, data_02:akauntingDatabase, auth_fetch = Depends(auth_decode)):
        result = web_crawl_fnc(data_01.akaunting_email, decrypt(data_01.akaunting_password), data_01.company_name, data_02.customer, data_02.due_date, data_02.invoice_num, data_02.item01_name, data_02.item01_description, data_02.item01_quantity, data_02.item01_price, data_02.item02_name, data_02.item02_description, data_02.item02_quantity, data_02.item02_price, data_02.item03_name, data_02.item03_description, data_02.item03_quantity, data_02.item03_price)
        return result

