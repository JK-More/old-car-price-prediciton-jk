# import requied packages

import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from flask import Flask, render_template , request

# create flask object
app = Flask("car_price_model")

# load ml model which is store in .pkl format
model = pickle.load(open('car_price_model.pkl','rb'))

# route to which we need to send http request
@app.route('/',methods=['GET'])

# function that will return index.html
def Home():
    return render_template('index.html')

# create odject for Standardscaler
standard_to = StandardScaler()

# HTTP post request method
@app.route("/predict",methods=['POST'])

# function to predict the result from ml model
def predict():

    if request.method == 'POST':

        #use request.method to get the data from html form through post method
        Year = int(request.form['Year'])
        Year = 2021 -Year
        Present_price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])

        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        # Fuel_type is categorised into petrol, diesel, cng . one-hot encoding is needed for it.
        if(Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif (Fuel_Type_Petrol == 'Diesel'):
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else :
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        Seller_Type_Individual = request.form['Seller_Type_Individual']
        # seller_type is categorised into individual and dealer
        if (Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else :
            Seller_Type_Individual = 0

        Transmission_Mannual = request.form['Transmission_Mannual']
        # Transmission_Mannual is categorised into mannual and automatic
        if (Transmission_Mannual == 'Mannual'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0

        prediction = model.predict([[Present_price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output = round(prediction[0],2)

        #condition for invalid value and valid value
        if output<0:
            return render_template('index.html',prediction_text="Sorry you can't sell this car")
        else:
            return render_template('index.html',prediction_text="You can sell this car at {} lakhs.".format(output))

    # Page display when no value are inserted.without any output.
    else:
        return render_template('index.html')


if __name__ == "__main__":
    # to start web server
    # debug : when i save something in my structure, server should restart again
    app.run(debug=True)