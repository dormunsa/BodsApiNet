from flask_restful import  Resource
from PreProccess.md import getVideo2
from PreProccess.md_zoom_script import getVideo
from PreProccess.relativeZoom import  main
from flask import request , Response
class StartApp(Resource):
    # run video by file path
    def get(self):
        video = request.args.get('video')
        main(video)
        return {"about" : "hello world"}
