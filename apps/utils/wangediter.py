# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/5/28 14:05'

import os
from flask import Flask, request,Response

UPLOAD_FOLDER = '/TmageUploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#文件名合法性验证
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#对文件上传进行相应
app.route("/ImageUpdate",methdos = ["POST"])
def GetImage():
    file = request.files[0]
    if file == None:
        result = r"error|未成功获取文件，上传失败"
        res = Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
    else:
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imgUrl = "http://localhost:5000" + UPLOAD_FOLDER + "/" + filename
            res = Response(imgUrl)
            res.headers["ContentType"] = "text/html"
            res.headers["Charset"] = "utf-8"
            return res