from flask import Flask, render_template, request
from werkzeug.utils import redirect
# from flask.helpers import url_for
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model2.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index1.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST', 'GET'])
def predict():
    # Fuel_Type_Diesel=0
    if request.method =='GET':
        return redirect('/')
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        #Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type=request.form['Fuel_Type']
        if(Fuel_Type=='Petrol'):
                Fuel_Type=1
        elif(Fuel_Type=='Diesel'):
            Fuel_Type=2
        else:
            Fuel_Type=3
        Year=2021-Year
        Seller_Type=request.form['Seller_Type']
        if(Seller_Type=='Individual'):
            Seller_Type=2
        else:
            Seller_Type=1	
        Transmission=request.form['Transmission']
        if(Transmission=='Mannual'):
            Transmission=1
        else:
            Transmission=2
        prediction=model.predict([[Present_Price,Kms_Driven,Fuel_Type,Seller_Type,Transmission,Owner,Year]])
        #Present_Price	Kms_Driven	Fuel_Type	Seller_Type	Transmission	Owner	Years_Old
        output=round(prediction[0],2)
        if output<0:
            return render_template('index1.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index1.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index1.html')
    
    


if __name__=="__main__":
    app.run(debug=True)