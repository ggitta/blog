from utils import qiniu
import io
from PIL import Image
import uuid
import json
from django.shortcuts import render,HttpResponse
def upload(req):
    img=req.FILES.get("editormd-image-file")
    _img = img.read()
    image = Image.open(io.BytesIO(_img))
    filename=str(uuid.uuid1()).replace("-","")[0:8]
    realfilename = filename + "." + image.format
    image.save('./media/' + realfilename)
    result = {}
    try:
        url = qiniu.upload(realfilename, './media/' + realfilename)
        result["success"]=1
        result["message"]="上传成功"
        result["url"]=url
    except Exception as a:
        result["success"]=0
        result["message"]="上传失败"
    return HttpResponse(json.dumps(result))
