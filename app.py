from flask import Flask
from flask_mysqldb import MySQL
from flask import jsonify
from flask import request
import pymysql 

app = Flask(__name__)

conn = pymysql.connect(
    user="sql6581671",
    password="NuYPGjXERw", 
    host="sql6.freemysqlhosting.net",
    port=3306,
    database="sql6581671",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)
# conn = pymysql.connect(
#     user="root",
#     password="", #GANTI PASSWORDNYA
#     host="127.0.0.1",
#     port=3306,
#     database="tubestst",
#     cursorclass=pymysql.cursors.DictCursor,
#     autocommit=True
# )

mysql = MySQL(app)
cur = conn.cursor()

@app.route('/')
def homepage():
    return ("<p><h1>Selamat datang di Tubes TST Kelompok 10!</h1></p>Anggota :<p><h2>David Hugo Triannas 18220004</h2></p><p><h2>Muhammad Rizki Pratama 18220110</h2></p><p>Untuk mengakses data covid pada negara USA dapat dengan menambahkan '/uscovid' dan data ecommerce pada negara USA dengan menambahkan '/ecommerce'")

@app.route("/ecommerce", methods = ['GET'])
def ecommerce():
    cur.execute("SELECT * FROM ecommerce")
    rv = cur.fetchall()  
    return jsonify(rv)

@app.route("/uscovid", methods = ['GET'])
def uscovid():
    cur.execute("SELECT * FROM uscovid")
    rv = cur.fetchall()  
    return jsonify(rv)

@app.route("/uscovid/insert", methods=['POST'])
#http://127.0.0.1:5000/uscovid/insert?date="04-04-2022"&county="Jakarta"&state="DKI"&cases=3
def insertuscovid():
    try:
        sqlQuery = "INSERT INTO uscovid(date, county, state, cases) VALUES(%s, %s, %s, %s)"
        bindData = (request.args.get('date'), 
        request.args.get('county'), 
        request.args.get('state'), 
        request.args.get('cases',type=int))            
        cur.execute(sqlQuery, bindData)
        response = jsonify('Covid data added successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)    

@app.route("/uscovid/update", methods = ['PUT'])
def updateuscovid():
    try:
        sqlQuery = "UPDATE uscovid SET county=%s, state=%s, cases=%s WHERE date=%s"
        bindData = (request.args.get('county'), 
        request.args.get('state'), 
        request.args.get('cases', type=int), 
        request.args.get('date'))
        cur.execute(sqlQuery, bindData)
        response = jsonify('Covid data updated successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)

@app.route('/uscovid/delete', methods=['DELETE'])
def deleteuscovid():
    try:		
        sqlQuery = "DELETE from uscovid where county=%s and state=%s"
        bindData = (request.args.get('county'), 
        request.args.get('state'))
        cur.execute(sqlQuery, bindData)
        response = jsonify('Covid data deleted successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response  

@app.route("/ecommerce/insert", methods=['POST'])
#http://127.0.0.1:5000/ecommerce/insert?order_id=1901&product="AYAM GORENG KUNING"&quantity_ordered=5&price_each=3&city="Jakarta"
def insertecommerce():
    try:
        sqlQuery = "INSERT INTO ecommerce(order_id, product, quantity_ordered, price_each, city) VALUES(%s, %s, %s, %s, %s)"
        bindData = (request.args.get('order_id',type=int), 
        request.args.get('product'), 
        request.args.get('quantity_ordered',type=int), 
        request.args.get('price_each',type=int),           
        request.args.get('city'))           
        cur.execute(sqlQuery, bindData)
        response = jsonify('Ecommerce data added successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)    

@app.route("/ecommerce/update", methods = ['PUT'])
def updateecommerce():
    try:
        sqlQuery = "UPDATE ecommerce SET product=%s, quantity_ordered=%s, price_each=%s, city=%s WHERE order_id=%s"
        bindData = (request.args.get('product'), 
        request.args.get('quantity_ordered',type=int), 
        request.args.get('price_each', type=int), 
        request.args.get('city'),
        request.args.get('order_id',type=int))
        cur.execute(sqlQuery, bindData)
        response = jsonify('Ecommerce data updated successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)

@app.route('/ecommerce/delete', methods=['DELETE'])
def deleteecommerce():
    try:		
        sqlQuery = "DELETE from ecommerce where order_id=%s"
        bindData = (request.args.get('order_id',type=int))
        cur.execute(sqlQuery, bindData)
        response = jsonify('Ecommerce deleted successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)      

if __name__ == "__main__":
    app.run(debug=True)