import csv
from flask import Flask, render_template,request,redirect,url_for
import diseaseprediction
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'brinda06'
app.config['MYSQL_DB'] = 'doctor1'
mysql = MySQL(app)


with open('templates/Testing.csv', newline='') as f:
        reader = csv.reader(f)
        symptoms = next(reader)
        symptoms = symptoms[:len(symptoms)-1]
@app.route('/', methods=['GET'])
def dropdown():
        return render_template('includes/default.html', symptoms=symptoms)

@app.route("/forward/",methods=['POST'])
def move_forward():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from details")
    data1 = cur.fetchall()
    return render_template('table.html',data1=data1)


@app.route('/disease_predict', methods=['POST'])
def disease_predict():
    selected_symptoms = []
    if(request.form['Symptom1']!="") and (request.form['Symptom1'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom1'])
    if(request.form['Symptom2']!="") and (request.form['Symptom2'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom2'])
    if(request.form['Symptom3']!="") and (request.form['Symptom3'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom3'])
    if(request.form['Symptom4']!="") and (request.form['Symptom4'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom4'])
    if(request.form['Symptom5']!="") and (request.form['Symptom5'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom5'])

    disease = diseaseprediction.dosomething(selected_symptoms)
    with open('Book1.csv', mode='r') as infile:
     reader = csv.reader(infile)
     with open('Book1_new.csv', mode='w') as outfile:
         writer = csv.writer(outfile)
         mydict = {rows[0]:rows[1] for rows in reader}
         med = mydict[disease[0]]

    with open('Book2.csv', mode='r') as infile1:
     reader = csv.reader(infile1)
     with open('Book2_new.csv', mode='w') as outfile1:
         writer = csv.writer(outfile1)
         mydict1 = {rows[0]:rows[1] for rows in reader}
         home = mydict1[disease[0]]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from details")
    data1 = cur.fetchall()

    return render_template('disease_predict.html',disease=disease,symptoms=symptoms,med=med,home=home,data1=data1)
 

if __name__ == '__main__':
    app.run(debug=True)