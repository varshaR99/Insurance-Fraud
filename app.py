from flask import Flask,render_template,request,redirect,url_for,session,flash
import sqlite3
import smtplib
import os
from encrypt import *
from main import *
import joblib
from docx2pdf import convert
import pdfplumber
import base64
import random
user=[]
database='database1.db'
conn=sqlite3.connect(database)
cursor=conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS police_details(Id INTEGER PRIMARY KEY AUTOINCREMENT, police_id TEXT,  official_email TEXT, password TEXT,status TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS user_details(Id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, user_ID TEXT, user_email TEXT,  password TEXT,status text)")
cursor.execute("CREATE TABLE IF NOT EXISTS encrypt_user_details(Id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, user_ID TEXT, user_email TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS user_upload(Id INTEGER PRIMARY KEY AUTOINCREMENT, user_ID TEXT,  reason TEXT,document_id text,status INTEGER,pupdate INTEGER,result INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS encrypt_result(Id INTEGER PRIMARY KEY AUTOINCREMENT, user_ID TEXT,  reason TEXT,document_id text, result INTEGER)")

app=Flask(__name__)
@app.route("/")
@app.route("/index")
def index():
        return render_template("index.html")


@app.route("/user_details",methods=['POST','GET'])
def user_details():
    if request.method=="POST":    
        user_name=request.form['user_name']
        user_ID=request.form['user_ID']
        user_email=request.form['user_email']
        password=request.form['password']
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute(" SELECT user_email FROM user_details WHERE user_email=?",(user_email,))
        registered=cursor.fetchall()
        if registered:
            return render_template('index.html',show_alert1=True)
        else:
             cursor.execute("insert into user_details (user_name,user_ID,user_email,password,status) values(?,?,?,?,?)",(user_name,user_ID,user_email,password,0))
             conn.commit()
             return render_template("index.html",show_alert2=True)
    return render_template('index.html')


@app.route("/user_login",methods=['POST','GET'])
def user_login():
    email=request.form['email']
    password=request.form['password']
    conn=sqlite3.connect(database)
    cursor=conn.cursor()
    cursor.execute("select * from user_details where user_email = ? and  password=?",(email,password))
    data=cursor.fetchone()
    if data:
        userid=data[2]
        user.append(userid)
        cursor.execute("select * from user_details where status=? and user_email=?",(1,email))
        data1=cursor.fetchone()
        if data1:
                return render_template("USER_UPLOAD.html")
        else:
            return render_template("index.html",show_alert3=True)    
    else:
        return render_template("index.html",show_alert4=True)    
       

@app.route("/police_details",methods=['POST','GET'])
def police_details():
    if request.method=="POST":
        police_ID=request.form['police_ID']
        police_email=request.form['police_email']
        password=request.form['password']
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute(" SELECT * FROM police_details WHERE police_ID=?",(police_ID,))
        registered=cursor.fetchall()
        if registered:
            return render_template('index.html',show_alert1=True)
        else:
            cursor.execute("insert into police_details (police_id,official_email,password,status) values(?,?,?,?)",(police_ID,police_email,password,0))
            conn.commit()
            return render_template("index.html",show_alert2=True)
    return render_template("index.html")


@app.route("/police_login",methods=['POST','GET'])
def police_login():
        if request.method == 'POST':
            user_id=request.form['user_id']
            password=request.form['password']
            conn=sqlite3.connect(database)
            cursor=conn.cursor()
            cursor.execute("select * from police_details where  police_id= ? and  password=?",(user_id,password))
            data=cursor.fetchone()
            if data:
                    cursor.execute("select * from user_upload where  status= ? ",(2,))
                    data1=cursor.fetchall()      
                    return render_template("police_view.html",data=data1)
            else:
                return render_template("index.html",show_alert4=True) 
        return render_template("staff_page.html")

ADMIN_USERNAME='admin'
ADMIN_PASSWORD='admin'

@app.route('/admin',methods=["GET","POST"])
def admin():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        if name==ADMIN_USERNAME and password==ADMIN_PASSWORD:
               conn=sqlite3.connect(database)
               cursor=conn.cursor()
               cursor.execute("select * from user_details where status=?",(0,))
               data=cursor.fetchall()
               cursor.execute("select * from police_details")
               data1=cursor.fetchall()
               cursor.execute("select * from encrypt_user_details" )
               data2=cursor.fetchall()
               cursor.execute("select * from user_upload where status=?",(3,))
               data3=cursor.fetchall()
               cursor.execute("select * from user_upload where status=?",(2,))
               data4=cursor.fetchall()
               cursor.execute("select * from user_upload where pupdate=?",(1,))
               data5=cursor.fetchall()
               return render_template("admin_view.html",data=data,data1=data1,data2=data2,data3=data3,data4=data4,data5=data5)

        else:
                return render_template('index.html',show_alert4=True)
    return render_template('index.html')




password="123456"
@app.route("/approve_user",methods=['POST','GET'])
def approve_user():
    idnum=request.form['idnum']
    conn=sqlite3.connect(database)
    cursor=conn.cursor()
    cursor.execute("update user_details set status=? where Id =?",(1,idnum))
    conn.commit()
    cursor.execute("select * from user_details where Id=?",(idnum,))
    data1=cursor.fetchone()
    #print(data1)
    user_name = encrypt(data1[1], password)
    user_ID = encrypt(data1[2], password)
    user_email = encrypt(data1[3], password)
    cursor.execute("insert into encrypt_user_details (user_name,user_ID,user_email) values(?,?,?)",(user_name,user_ID,user_email))
    conn.commit()
    return render_template("index.html")







@app.template_filter('b64encode')
def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')


@app.route("/decrypt_user",methods=['POST','GET'])
def decrypt_user():
        Id1 = request.form['number1']
        password=request.form['pass']
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("select * from encrypt_user_details where Id=?",(Id1,))
        data1=cursor.fetchone()
        id1=data1[0]
        name = decrypt(data1[1], password)
        ID = decrypt(data1[2], password)
        email = decrypt(data1[3], password)
        return render_template("decrypt_data.html",id1=id1,ID=ID,name=name,email=email)


    
loaded_model = joblib.load('xgboost_model.pkl')


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


import random

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        reason = request.form['Reason']  
        file = request.files['upload_file']
        file_id = ''.join(random.choices('123456789', k=4))
        file_path = 'static/document/' + file_id + '.pdf'  
        file.save(file_path)
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("insert into user_upload (user_ID,reason,document_id,status,pupdate) values(?,?,?,?,?)",(user[-1],reason,file_id,3,0))
        conn.commit()
        return render_template("index.html",show_alert5=True)
    return "Method not allowed"




@app.route('/sent_pdf', methods=['POST'])
def sent_pdf():
        idnum=request.form["filename"]
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("update user_upload set status=? where Id =?",(2,idnum))
        conn.commit()
        return render_template("index.html",show_alert6=True)

       

@app.route('/verify', methods=['POST'])
def verify():
        idnum=request.form["filename"]
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("UPDATE user_upload SET `status` = ?, `pupdate` = ? WHERE Id = ?", (1, 1, idnum))
        conn.commit()
        return render_template("index.html",show_alert7=True)



@app.route('/not_verify', methods=['POST'])
def not_verify():
        idnum=request.form["filename"]
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("update user_upload set status=?,pupdate=? where Id =?",(0,1,idnum))
        conn.commit()
        return render_template("index.html",show_alert7=True)

@app.route('/prediction', methods=['POST'])
def prediction():
        idnum=request.form["filename"]
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("select * from  user_upload where Id =?",(idnum,))
        data=cursor.fetchone()
        #print(data)
        policereport=int(data[4])
        file=int(data[3])
        file_path = f'static/document/{file}.pdf'   
        input_string=extract_text_from_pdf(file_path)
        words = input_string.split()
        #print(words)
        age=int(words[6])
        #print(age,"age")
        pannul=float(words[12])
        #print(pannul,"pannul")
        umlimit=int(words[15])
        #print(umlimit,"umlimit")
        incident_type=words[18]
        #print(incident_type,"incident_type:")
        incident_typeno=int(output1(incident_type))
        collosion_type=words[21]
        #print(collosion_type,"collosion_type")
        collosion_typeno=int(output1(collosion_type))
        inci_severcity=words[24]
        #print(inci_severcity,"inci_severcity")
        inci_severcityno=int(output1(inci_severcity))
        authorised_contact=words[26]
        #print(authorised_contact,"authorised_contact")
        authorised_contactno=output1(authorised_contact)
        incident_location=words[28]
        #print(incident_location,"incident_location")
        #incident_locationno=output1(incident_location)
        BODILY_INJURIES=int(words[30])
        #print(BODILY_INJURIES,"BODILY_INJURIES")
        vehiles_invlove=int(words[32])
        #print(vehiles_invlove,"vehiles_invlove")
        ##policereport=words[34]
        ##policereportno=int(output1(policereport))
        AUTO_MODEL=words[34]
        #print(AUTO_MODEL,"AUTO_MODEL")
        AUTO_MODELno=int(output1(AUTO_MODEL))
        AUTO_MAKE=words[36]
        #print(AUTO_MAKE,"AUTO_MAKE")
        AUTO_MAKEno=int(output1(AUTO_MAKE))
        policydate=words[38]
        #print(policydate,"policydate")
        pyear=int(policydate[-4:])
        pmonth=int(policydate[3:5])
        pdate=int(policydate[0:2])
        incidentdate=words[40]
        #print(incidentdate,"incident date")
        inyear=int(incidentdate[-4:])
        inmonth=int(incidentdate[3:5])
        indate=int(incidentdate[0:2])
        #print(pyear,pmonth,pdate,inyear,inmonth,indate)
        #print(incident_typeno,collosion_typeno,inci_severcityno,authorised_contactno,incident_location,policereportno,AUTO_MODELno,AUTO_MAKEno)
        #print(pannul,umlimit,incident_typeno,collosion_typeno,inci_severcityno,authorised_contactno,age,124,BODILY_INJURIES,vehiles_invlove,
##                                                AUTO_MODELno,AUTO_MAKEno,pyear,pmonth,pdate,inyear,inmonth,indate)
        input_data = np.array([[pannul,umlimit,incident_typeno,collosion_typeno,inci_severcityno,authorised_contactno,age,124,BODILY_INJURIES,vehiles_invlove,
                                                policereport,AUTO_MODELno,AUTO_MAKEno,pyear,pmonth,pdate,inyear,inmonth,indate]])
        y_predict_xgb = loaded_model.predict(input_data)
        prediction=y_predict_xgb[0]
        prediction1=int(prediction)
        password1=data[1]
        reason = encrypt(data[2], password1)
        document_id=encrypt(data[3], password1)
        prediction2=encrypt(str(prediction1), password1)
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("update user_upload set pupdate=? where Id =?",(2,idnum))
        conn.commit()
        cursor.execute("update user_upload set result=? where Id =?",(prediction1,idnum))
        conn.commit()
        cursor.execute("insert into encrypt_result (user_ID,reason,document_id,result) values(?,?,?,?)",(data[1],reason,document_id,prediction2))
        conn.commit()
        return render_template("output.html",result=prediction)

        #return render_template("result.html",result=y_predict_xgb,reason=data[2])
        

@app.route('/pdf_view', methods=['POST'])
def pdf_view():
    complaint_number = request.form['filename']
    return render_template('pdf_view.html',new=complaint_number)
             

@app.route('/notification')
def notification():
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("select * from  encrypt_result where user_ID =?",(user[-1],))
        data=cursor.fetchall()
        return render_template('notification.html',new=data)

        
        

@app.route('/decrypt_result',methods=['POST'])
def decrypt_result():
        Id1 = request.form['number1']
        password=request.form['pass']
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("select * from encrypt_result where Id=?",(Id1,))
        data1=cursor.fetchone()
        userid=data1[1]
        reason = int(decrypt(data1[2], password))
        document_id = decrypt(data1[3], password)
        #print(document_id)
        result = int(decrypt(data1[4], password))
        #print(result)
        if document_id==1:
                return render_template("result.html",userid="**",reason="**",document_id="**",result="**")
        else:
                return render_template("result.html",userid=userid,reason=reason,document_id=int(document_id),result=result)

    
if __name__=='__main__':
    app.run(port=500,debug=False)
