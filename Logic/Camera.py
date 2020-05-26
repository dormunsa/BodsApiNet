
import requests
import json



def readCameraByLocation(latitude , longitude):
    send_url = 'http://localhost:58157/api/CameraLocation?latitude='+str(latitude)+'&longitude='+ str(longitude)
    id = requests.get(send_url)
    json_data = json.loads(id.text)
    return json_data



def readPhoneByCameraId(cameraId ):
    send_url = 'http://localhost:58157/api/GetPhone?cameraId='+str(cameraId)
    phone = requests.get(send_url)
    return phone.text

def readHookByCameraId(cameraId ):
    send_url = 'http://localhost:58157/api/GetHook?cameraId='+str(cameraId)
    phone = requests.get(send_url)
    return phone.text
