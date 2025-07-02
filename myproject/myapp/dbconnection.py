import pymysql
conn=pymysql.connect(host='localhost',user='root',password='',database='phishing_email')

def logindata(qry):
    cursor=conn.cursor()
    sql=qry
    cursor.execute(sql)
    data=cursor.fetchone()
    #data=cursor
    return data

def selectdata(qry):
    cursor=conn.cursor()
    sql=qry
    cursor.execute(sql)
    data=cursor.fetchone()
    #data=cursor
    return data

def insertdata(qry):        
    cursor=conn.cursor()
    sql=qry
    cursor.execute(sql)
    conn.commit()

def selectalldata(qry):
    cursor=conn.cursor()
    sql=qry
    cursor.execute(sql)
    #data=cursor.fetchone()
    data=cursor
    return data

def updatedata(qry):        
    cursor=conn.cursor()
    sql=qry
    cursor.execute(sql)
    conn.commit()


def deletedata(qry):        
    cursor=conn.cursor()
    sql=qry
    cursor.execute(sql)
    conn.commit()