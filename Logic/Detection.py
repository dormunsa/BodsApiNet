import requests
import json



def InsertDetection(weatherId , CameraId , ImagePath):
    data_set = {"CameraId": CameraId, "ImagePath": ImagePath, "WeatherId": weatherId}
    json_dump = json.dumps(data_set)
    response = requests.post('http://localhost:58157/api/Detection', json=data_set)
    return response.text




