from flask import Blueprint,request,current_app
from flask_mail import Message  
from . import detection_model as model
import cv2
import numpy as np
import json
global res
res = ''
img_type = ('Abuse','Arrest','Arson','Normal')
views = Blueprint('views',__name__)

def bg_predict(filename = 'mix_all.mp4'):
    print(f'executing bg predict... on {filename}')
    from . import executor
    vid = cv2.VideoCapture(f'D:\\Torrent\\Video Anomaly\\vlc_extract_new\\{filename}')
    read = True
    sent = False
    old_count = 0
    count = 0
    while read:
        read,frame = vid.read()
        count += 1
        if count - old_count >= 150 and sent == True:
            sent = False
        if read == True and count == 30:
            pred = img_type[model.predict(np.expand_dims(cv2.resize(frame,(224,224)),axis=0),verbose = 0).argmax()]
            if pred != 'Normal' and sent == False:
                print(pred)
                print('sent mail!')
                sent = True
                old_count = count
                cv2.imwrite('anomaly1.png',frame)
                executor.submit(send_mail,pred,'anomaly1.png')
            count = 0
    print('completed...')

def send_mail(anomaly,file = 'anomaly.png'):
    from . import mail
    print('creating mail...',current_app.config['TESTING'])
    msg = Message(
                'Anomaly Detected!',
                sender ='madhvesham.teamchimera@gmail.com',
                recipients = ['madhvesham.cs20@rvce.edu.in']
               )
    msg.body = f'We have detected suspicious activity from the video footage, it is classified as : {anomaly}'
    with open(file,'rb') as fp:
        msg.attach("anomaly.png", "image/png", fp.read())
    mail.send(msg)
    print('mail sent successfully')

@views.route('/',methods=['POST','GET'])
def home():
    #executor.submit(bg_predict)
    return res

@views.route('/result',methods=['GET'])
def result():
    return res

@views.route('/predict',methods=['GET','POST'])
def predict():
    print('predict...')
    from . import executor
    file = request.json
    filename = file['name']
    #bg_predict(filename)
    executor.submit(bg_predict,filename)
    return file

@views.route('/custom_predict',methods = ['POST'])
def custom_predict():
    from . import executor
    file = request.json
    npimg = np.array(file['data']['data'],dtype=np.uint8)
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    img = cv2.resize(img,(224,224))
    cv2.imwrite('anomaly.png',img)
    pred = img_type[model.predict(np.expand_dims(img,axis=0)).argmax()]
    #if pred != 'Normal':
        #executor.submit(send_mail,pred)
    return json.dumps({'name':'Kaushik','success':pred})