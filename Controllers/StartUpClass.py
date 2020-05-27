from flask_restful import  Resource
from PreProccess.md import getVideo2
from PreProccess.md_zoom_script import getVideo
from PreProccess.relativeZoom import  main
from flask import request , Response
class StartApp(Resource):

    def get(self):
        video = request.args.get('video')
        getVideo(video)
        return {"about" : "hello world"}
