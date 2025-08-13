from flask import Flask,render_template,url_for,json,request,redirect
import pickle
import numpy as np

with open('model.pkl','rb') as file:
    model=pickle.load(file)

app=Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('prediction'))

@app.route('/prediction',methods=['GET','POST'])
def prediction():
    if request.method=='POST':
        Gender=int(request.form['Gender'])
        Age=float(request.form['Age'])
        Haemoglobin=float(request.form['Haemoglobin'])
        ESR=float(request.form['ESR'])
        WBC=float(request.form['WBC'])
        Neutrophil=int(request.form['Neutrophil'])
        Lymphocyte=float(request.form['Lymphocyte'])
        Monocyte=float(request.form['Monocyte'])
        Eosinophil=float(request.form['Eosinophil'])
        Basophil=float(request.form['Basophil'])
        RBC=float(request.form['RBC'])
        Platelets=int(request.form['Platelets'])

        output=np.array([[Gender, Age, Haemoglobin, ESR, WBC,
        Neutrophil, Lymphocyte, Monocyte, Eosinophil, Basophil, RBC,
        Platelets]])
        pred=model.predict(output)[0]
        result='Postive' if pred==1 else 'Negative'
        return render_template('prediction.html',prediction=result)
    return render_template('prediction.html')
if __name__=='__main__':
    app.run(debug=True)