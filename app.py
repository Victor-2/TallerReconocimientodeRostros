import os
from flask import Flask
from flask_cors import CORS
from flask import Flask, render_template, request, send_file
import os
from shutil import rmtree
import MySQLdb
app = Flask(__name__)



@app.route('/test')

def AllTabl():
    datos =['localhost','root','','rostros']
    conn=MySQLdb.connect(*datos)
    cursor = conn.cursor()
    cursor.execute("SELECT *FROM rostros ORDER BY(id) DESC")
    data=cursor.fetchall()
    rostro=data[0]
    cursor.execute("SELECT * FROM coordenadas WHERE id_rostro="+str(rostro[0]))
    coordenadas=cursor.fetchall()
    conn.close()
    return render_template('index.html', rostro=rostro, coordenadas=coordenadas)

@app.route('/')

def upload_file():
    return render_template('post_form.html')


@app.route("/consulta", methods=['GET'])

def consultar():
    if request.method == 'GET':
        datos =['localhost','root','','rostros']
        conn=MySQLdb.connect(*datos)
        cursor = conn.cursor()
        cursor.execute("SELECT *FROM rostros")
        data=cursor.fetchall()
        conn.close()
        return render_template('AllTable.html',data=data)

app.config['UPLOAD_FOLDER'] = "./Archivos/"
@app.route("/upload", methods=['POST'])

def uploader():
    if request.method == 'POST':
        rmtree("./Archivos")
        rmtree("./runs/detect")
        os.mkdir("Archivos")
        os.mkdir("./runs/detect")
        
        
        f = request.files['archivo']
        filename = f.filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.system("python ./yolov5/detect.py")
        datos =['localhost','root','','rostros']
        conn=MySQLdb.connect(*datos)
        cursor = conn.cursor()
        """
        ID=cursor.execute("SELECT MAX(id) FROM rostros")
        
        path=os.getcwd()
        
        cad=os.path.join(path,"Archivos")
        print(os.path.join(path,"Archivos"))

        with open(cad, "r") as original_file:
            string = base64.b64encode(original_file.read())

        print(string)
   """     
        cursor.execute("SELECT *FROM rostros ORDER BY(id) DESC")
        data=cursor.fetchall()
        rostro=data[0]
        cursor.execute("SELECT * FROM coordenadas WHERE id_rostro="+str(rostro[0]))
        coordenadas=cursor.fetchall()
        conn.close()
        return render_template('index.html', rostro=rostro, coordenadas=coordenadas,path=os.getcwd())

        #return render_template('index.html')
        #return send_file(os.getcwd()+"\\runs\detect\exp\\"+filename, mimetype='image/gif')
    
@app.route("/cargar", methods=['GET'])

def cargador():
    if request.method == 'GET':
        #rmtree("./Archivos")
        #rmtree("./runs/detect")
        #os.mkdir("Archivos")
        #os.mkdir("./runs/detect")
        filename = request.args.get('filename','')
        #filename = f.filename
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #os.system("python ./yolov5/detect.py")
        return send_file(os.getcwd()+"\\runs\detect\exp\\"+filename, mimetype='image/gif')


@app.route("/cargar1", methods=['GET'])

def cargador1():
    if request.method == 'GET':
        #rmtree("./Archivos")
        #rmtree("./runs/detect")
        #os.mkdir("Archivos")
        #os.mkdir("./runs/detect")
        filename = request.args.get('filename','')
        #filename = f.filename
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #os.system("python ./yolov5/detect.py")
        return send_file(os.getcwd()+"\\Archivos\\"+filename, mimetype='image/gif')


@app.route("/images", methods=['GET'])

def images():
    if request.method == 'GET':
        #rmtree("./Archivos")
        #rmtree("./runs/detect")
        #os.mkdir("Archivos")
        #os.mkdir("./runs/detect")
        filename = request.args.get('filename','')
        #filename = f.filename
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #os.system("python ./yolov5/detect.py")
        #return send_file(os.getcwd()+"\\Archivos\\"+filename, mimetype='image/gif')
        return render_template('images.html', nombre=filename)



if __name__=='__main__':
    app.run(debug=True)