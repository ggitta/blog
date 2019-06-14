from qiniu import Auth, put_file, etag
from jfsite.settings import ACCESS_KEY,SECRET_KEY,PERURL,BKNAME
q = Auth(ACCESS_KEY, SECRET_KEY)
#上传后保存的文件名
key = 'my-python-logo.png'
def upload(key,localfile):

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(BKNAME, key, 3600)
    #要上传文件的本地路径
    ret, info = put_file(token, key, localfile)
    print(ret)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)
    return PERURL+ret["key"]
