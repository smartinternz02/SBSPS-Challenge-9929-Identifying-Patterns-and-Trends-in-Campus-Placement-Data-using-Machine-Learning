from flask import Flask, request, render_template
import util

app = Flask(__name__)

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/predict")
def predicts():
    return render_template("predict.html")

@app.route('/submit', methods =['GET', 'POST']) 
def predict():
    gender =request.form['gender']
    ssc_p =  float(request.form['ssc_p']) 
    hsc_p = float(request.form['hsc_p']) 
    hsc_s=request.form[ 'hsc_s']
    degree_p = float(request.form['degree_p'])
    degree_t= request.form['degree_t']
    workex= request.form['workex']
    etest_p = float(request.form['etest_p'])
    specialisation = request.form['specialisation']
    mba_p = float(request.form['mba_p'])
    util.column(gender,ssc_p,hsc_p,hsc_s,degree_p,degree_t,workex,etest_p,specialisation,mba_p)
    status=util.predict_status()
    if(status==1):
        salary=util.predict_salary()
        return render_template('result.html', salary=salary)
    else:
        return render_template('submit.html')

if __name__=="__main__":
    app.run(debug=True)