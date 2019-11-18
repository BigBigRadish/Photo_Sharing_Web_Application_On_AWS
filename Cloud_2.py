# -*- coding: utf-8 -*-
'''
Created on 2019年11月5日 下午4:20:31
Zhukun Luo
Jiangxi University of Finance and Economics
'''

from flask import Flask , render_template, request, session
import datetime
import os
import boto3
from botocore.client import Config
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import hashlib
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
# put in your AWS details below

host="0.0.0.0"
port=8888
dbname="hire2020-hire-luozhukun1031"

dynamodb = boto3.resource('dynamodb',region_name='cn-north-1',aws_access_key_id='AKIAVLSEBUAJRL52NPMZ', aws_secret_access_key='7CJo4rxRqBXt/gA/NbYygqbiKMDEfnj1BpaBE+Wo')

table = dynamodb.Table('hire2020-hire-luozhukun1031')

app = Flask(__name__)

# Put in the keys of your AWS connection

app.secret_key = os.urandom(24)

ACCESS_KEY_ID = 'AKIAVLSEBUAJRL52NPMZ'
ACCESS_SECRET_KEY = '7CJo4rxRqBXt/gA/NbYygqbiKMDEfnj1BpaBE+Wo'
BUCKET_NAME = 'hire2020'

##########################

s3Client = boto3.client('s3',aws_access_key_id=ACCESS_KEY_ID,
  aws_secret_access_key=ACCESS_SECRET_KEY,
  config=Config(signature_version='s3v4',region_name='cn-north-1'))
#########################

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4',region_name='cn-north-1')
)


url = "http://s3.cn-north-1.amazonaws.com.cn/"


def uni_id():#s生成全局唯一ID
    nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S");#生成当前时间
    randomNum=random.randint(0,100);#生成的随机整数n，其中0<=n<=100
    if randomNum<=10:
        randomNum=str(0)+str(randomNum)
    uniqueNum=str(nowTime)+str(randomNum)
    return uniqueNum
@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        # print(session.values())
        uname = session['username']

    return render_template("index.html")
# https://docs.aws.amazon.com/zh_cn/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html


@app.route('/post', methods=['POST'])
def post():#主页

    if request.method == 'POST':


        f = request.files['file']
        title = request.form['title']
        ratings = request.form['ratings']
        user_comment = request.form['comments']
        # print(f)

        try:
            user_ip = request.headers['X-Forwarded-For'].split(',')[0]
        except:
            user_ip=request.remote_addr#用户ip
        # print(user_ip)
        filename = f.filename

        # keys = []
        # resp = s3Client.list_objects_v2(Bucket=BUCKET_NAME)
        # for obj in resp['Contents']:
        #     keys.append(obj['Key'])
        #
        # image_links = []
        # z = len(keys)
        # print(z)
        # for i in range(z):
        #     image_links.append(url+keys[i])
        #
        # print(image_links)


        if request.form['click'] == 'Upload Image':
            # object_1 = s3.Object(BUCKET_NAME,'hire2020-hire-luozhukun1031/'+filename)
            # object_1.put(Body=open(data, 'rb'))
            s3.Bucket(BUCKET_NAME).put_object(Key='hire2020-hire-luozhukun1031/'+filename, Body=f,ACL='public-read')
            #record user ip , date, time , photo name, photo url
            if('.jpg'in filename or '.jpeg' in filename or '.png' in filename):
                curr_time = datetime.datetime.now()
                date_str = curr_time.strftime(r'%Y-%m-%d')#日期
                time_str = curr_time.strftime(r'%H:%M:%S')#时间
                # print(date_str)
                # print(time_str)
                photo_name=''.join(filename.split('.')[:-1])#照片名字
                # print(photo_name)
                photo_url='https://hire2020.s3.cn-north-1.amazonaws.com.cn/hire2020-hire-luozhukun1031/'+filename
                # keys = []
                # resp = s3Client.list_objects_v2(Bucket=BUCKET_NAME,Prefix='hire2020-hire-luozhukun1031/')
                # print(resp['Contents'])
                # for bj in resp['Contents']:
                #     print(obj)
                #     keys.append(obj['Key'])
                #     priont(obj['Key'])
                # image_links = []
                # z = len(keys)
                # print(z)
                # print(user_ip)
                # for i in range(z):
                #     image_links.append(url + keys[i])
                # response = table.delete_item(
                #     Key={u'comments': {u'other_comment': None, u'user_comment': u'12'}}
                '''删除表所有项目'''
                # pe = "userip,datestr,timestr,photoname,photourl,comments,userID,ID"
                # response = table.scan(
                # ProjectionExpression=pe,
                # FilterExpression=Attr('datestr').exists()
                # )
                # Item=response['Items']                           
                # for i in Item:
                #     table.delete_item(
                #         Key={
                #             'ID':i['ID']
                #             }
                #         )

                Id=uni_id()
                response = table.put_item(
                Item={
                        'ID':Id,
                        'userID':Id,#生成uuid
                        # 'user_name':uname,
                        'userip': user_ip,
                        'datestr': date_str,
                        'timestr':time_str,
                        'photoname':photo_name,
                        'photourl':photo_url,
                        'comments':{
                        'usercomment':user_comment,
                        'othercomment':None
                        }
                        }
                        
                    
                )
                # print("PutItem succeeded:")
                # print(response['I'])
                return render_template("upload_succeed.html",suc_message='upload successful')
            else:
                err_message='picture format not right!'
                return render_template("upload_error.html",err_message=err_message)

@app.route('/upload', methods=['GET','POST'])#获取全部图片
def upload():

    if request.method == 'POST':

        if request.form['click'] == 'View Image':

            pe = "userip,datestr,timestr,photoname,photourl,comments,userID,ID"
            # ean={ "#date": 'date', '#time':'time',}
            
            # Expression Attribute Names for Projection Expression only.
            response = table.scan(
                ProjectionExpression=pe,
                FilterExpression=Attr('datestr').exists()
                )
            Item=response['Items']
            # print(Item)
            # return '<img src="' + image_links[0]+ '"/>'
            return render_template("gallary.html", Item=Item)
@app.route('/pic_details', methods=['GET','POST'])#获取图片详情
def pic_details():
    picture_detail={}
    if request.method == 'POST':
        picture_detail['userID'] = request.form['userID']
        picture_detail['ID'] = request.form['ID']
        picture_detail['userip'] = request.form['userip']
        picture_detail['uploaddate'] = request.form['uploaddatetime']
        picture_detail['photourl'] = request.form['photourl']
        picture_detail['usercomment'] = request.form['usercomment']
        picture_detail['photoname']=request.form['photoname']
        if request.form['othercomment']!='None':
            picture_detail['othercomment']=str(request.form['othercomment'])
        else:
            picture_detail['othercomment']='暂无其他人评论'
        return render_template("picture_detail.html", picture_detail=picture_detail)

@app.route('/comment', methods=['GET','POST'])
def comment():
    if request.method == 'POST':
        # print(request.form)
        other_comment = request.form['comments']
        ID=request.form['ID']
        userID=request.form['userID']
        usercomment=request.form['usercomment']
        uploaddate=request.form['uploaddate']
        photoname=request.form['photoname']
        photourl=request.form['photourl']
        # print(photourl)
        userip=request.form['userip']
        try:
            userIp = request.headers['X-Forwarded-For'].split(',')[0]
        except:
            userIp=request.remote_addr#用户ip
        if request.form['click'] == '评论':
            # response = table.update_item(
            # Key={
            #     # 'datestr': uploaddate.split(' ')[0],
            #     # 'timestr':uploaddate.split(' ')[1],
            #     # 'photoname':photoname
            #     'ID':ID
            #     },
            # UpdateExpression="set comments.othercomment = :coc",
            # ExpressionAttributeValues={
            #     ':coc':{'userIP':userip,'commentTime':datetime.datetime.now().strftime("%Y-%m-%d:%H-%M-%S"),'commentContent':user_comment}
            #     },
            # # ReturnValues="UPDATED_NEW"
            # )
            # new_uuid=uni_id()
            # Item={
            #         'ID':new_uuid,
            #         'userID':new_uuid,#生成uuid
            #         # 'user_name':uname,
            #         'userip': userip,
            #         'datestr': uploaddate.split(' ')[0],
            #         'timestr':uploaddate.split(' ')[1],
            #         'photoname':photoname,
            #         'photourl':photourl,
            #         'comments':{
            #         'usercomment':usercomment,
            #         'othercomment':{'userIP':userip,'commentTime':datetime.datetime.now().strftime("%Y-%m-%d:%H:%M:%S"),'commentContent':user_comment}
            #             }
            #         }
            # table.put_item(Item=Item)#新增一条数据
            othercomments={'userIP':userIp.encode('utf-8'),'commentTime':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode('utf-8'),'commentContent':other_comment.encode('utf-8')}
            I_tems=table.query(ProjectionExpression='comments',
                        KeyConditionExpression=Key('ID').eq(ID) 
            )
            already_comments=I_tems['Items'][0]['comments']['othercomment']
            table.update_item(
                Key={
                    'ID':ID
                    },
                UpdateExpression="set comments.othercomment= :coc",
                ExpressionAttributeValues={
                    ':coc': str(already_comments).replace('None','')+'--'+str(othercomments),
                    },
                ReturnValues="UPDATED_NEW"
            )
            pe = "userip,datestr,timestr,photoname,photourl,comments,userID,ID"
            response = table.scan(
                ProjectionExpression=pe,
                FilterExpression=Key('ID').eq(ID)    
                )
            picture_detail={}
            item = response['Items']
            # print(item)
            othercomments=''
            for it in item:
                othercomments=othercomments+str(it['comments']['othercomment'])

            # picture_detail['userID']=item['userID']
            picture_detail['ID']=item[0]['ID']
            picture_detail['userip'] = item[0]['userip']
            picture_detail['uploaddate'] = item[0]['datestr']+' '+item[0]['timestr']
            picture_detail['photourl'] = item[0]['photourl']
            picture_detail['usercomment'] = item[0]['comments']['usercomment']
            picture_detail['photoname']=item[0]['photoname']
            picture_detail['othercomment']=othercomments.replace('None','')
            return render_template("picture_detail.html", picture_detail=picture_detail)


@app.route('/picture_search', methods=['GET','POST'])#按照片名字或者日期进行数据搜索
def picture_search():

    if request.method == 'POST':
            photoname=request.form['search_name'].strip()#过滤条件按照片名字
            # print(photoname)
            if request.form['search_date']:
                date=request.form['search_date']#过滤条件按日期
            else:
                date=None
            if date not in ['0000-00-00','',None] and photoname  in['',None]:
                response = table.scan(
                    FilterExpression=Attr('datestr').eq(date) 
                    )
                Item=response['Items']
            elif date in ['0000-00-00','',None] and photoname not in['',None]:
                response = table.scan(
                        FilterExpression=Attr('photoname').eq(photoname)
                        )
                Item=response['Items']
            else:
                response = table.scan(
                            FilterExpression=Attr('photoname').eq(photoname) and Attr('datestr').eq(date)
                            )
                Item=response['Items']
            
            if len(Item)==0:#如果无结果，重新扫描全表
                response = table.scan(
                        FilterExpression=Attr('datestr').exists()
                        )
                Item=response['Items'] 
            # print(Item)
            # return '<img src="' + image_links[0]+ '"/>'
            return render_template("gallary.html", Item=Item)

@app.route('/picture_share', methods=['GET','POST'])#分享图片并生成有时效的链接
def picture_share():
    
    if request.method == 'POST':
        ID=request.form['ID']
        photourl=request.form['photourl']
        key_photo=photourl.replace("https://hire2020.s3.cn-north-1.amazonaws.com.cn/",'')
        generateUrl=generate_link(key_photo)
        pe = "userip,datestr,timestr,photoname,photourl,comments,userID,ID"
        response = table.scan(
                ProjectionExpression=pe,
                FilterExpression=Key('ID').eq(ID)    
                )
        picture_detail={}
        item = response['Items']
        print(item)
        # print(item)
        othercomments=''
        for it in item:
            othercomments=othercomments+str(it['comments']['othercomment'])

        # picture_detail['userID']=item['userID']
        picture_detail['ID']=item[0]['ID']
        picture_detail['userip'] = item[0]['userip']
        picture_detail['uploaddate'] = item[0]['datestr']+' '+item[0]['timestr']
        picture_detail['photourl'] = item[0]['photourl']
        picture_detail['usercomment'] = item[0]['comments']['usercomment']
        picture_detail['photoname']=item[0]['photoname']
        picture_detail['othercomment']=othercomments.replace('None','')
        return render_template("picture_share.html", picture_detail=picture_detail,generateUrl=generateUrl,Item=item) 

def generate_link(key_photo):#生成预签名
    url = s3Client.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': BUCKET_NAME,
        'Key':key_photo
    },
    ExpiresIn=60#设置过期时间60s
    )
    return url




if __name__== '__main__':
    app.run(host = host,port = port, debug = True)


# port = os.getenv('0.0.0.0','8080')
#
# if __name__== '__main__':
#     app.run(host = '0.0.0.0',port = int(port), debug = True)
