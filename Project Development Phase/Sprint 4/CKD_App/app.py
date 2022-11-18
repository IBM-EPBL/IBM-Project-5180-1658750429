from flask import Flask, request, render_template

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "nsbW84O5-58I1rSeLI_8YhWJ7ZmphElqVB5ZMf1g1i8S"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)
import pickle
import numpy as np

model=pickle.load(open('ckd_ensemble_model.pkl','rb'))
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login/')
def login():
    return render_template('Login.html')
@app.route('/reg/')
def reg():
    return render_template('Registration.html')
@app.route('/form/')
def form():
    return render_template('fill2.html')
@app.route('/predict/',methods=["POST","GET"])
def predict():
    if request.method=="POST":
        i1=float(request.form['sg'])
        i2=request.form['htn']
        if i2=='Yes':
            i2=1
        else:
            i2=0
        
        #i2=0 if 'No' else 1
        
        
        i3=float(request.form['hemo'])
        i4=int(request.form['al'])
        i5=float(request.form['pcv'])
        i6=request.form['dm']
        
        if i6=='Yes':
            i6=1
        else:
            i6=0
        
        #i6=0 if 'No' else 1
        i7=float(request.form['rc'])
        i8=float(request.form['sod'])
        i9=float(request.form['bu'])
        i10=float(request.form['bp'])
        
        payload_scoring = {"input_data": [{"fields": [['bp', 'al', 'bu', 'sg', 'sod', 'hemo', 'pcv', 'rc', 'htn', 'dm']], "values": [[i10,i4,i9,i1,i8,i3,i5,i7,i2,i6]]  }]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f1dfeb85-c1e4-4b8e-a479-a4364b22c6fd/predictions?version=2022-11-17', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        pred = response_scoring.json()
        #prediction
        
        final_result=pred['predictions'][0]['values'][0][0]
        print(final_result)
        
        if(final_result==1):
            result='Positive'
        else:
            result='Negative'
            
            
        return ''' <!DOCTYPE html>
        <html>
        <head>
        <title>CKD Diagnosis Result</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <style>
        body, h1,h2,h3,h4,h5,h6 {font-family: "Montserrat", sans-serif}
        .w3-row-padding img {margin-bottom: 12px}
        /* Set the width of the sidebar to 120px */
        .w3-sidebar {width: 120px;background: #08d;}
        .submit {    background-color: #08d;
            border-radius: 12px;
            border: 0;
            box-sizing: border-box;
            color: #eee;
            cursor: pointer;
            font-size: 18px;
            height: 100px;
            margin-top: 38px;
            outline: 0;
            text-align: center;
            width: 30%;
          }
          .submit:active {
            background-color: #06b;
          }
          .input-container {
            height: 40px;
            position: relative;
            width: 100%;
          }
          
          .ic1 {
            margin-top: 50px;
          }
          
          .ic2 {
            margin-top: 40px;
          }
          
          .input {
            background-color: #303245;
            border-radius: 12px;
            border: 0;
            box-sizing: border-box;
            color: #eee;
            font-size: 18px;
            height: 100%;
            outline: 0;
            padding: 4px 20px 0;
            width: 100%;
          }
          
          .cut {
            background-color: #15172b;
            border-radius: 10px;
            height: 20px;
            left: 20px;
            position: absolute;
            top: -20px;
            transform: translateY(0);
            transition: transform 200ms;
            width: 76px;
          }
          
          .cut-short {
            width: 50px;
          }
          
          
          .placeholder {
            color: #65657b;
            font-family: sans-serif;
            left: 20px;
            line-height: 14px;
            pointer-events: none;
            position: absolute;
            transform-origin: 0 50%;
            transition: transform 200ms, color 200ms;
            top: 50px;
          }
          
           
          .submit {
            background-color: #08d;
            border-radius: 12px;
            border: 0;
            box-sizing: border-box;
            color: #eee;
            cursor: pointer;
            font-size: 18px;
            height: 50px;
            margin-top: 38px;
            outline: 0;
            text-align: center;
            width: 100%;
          }
          
          .submit:active {
            background-color: #06b;
          }
          .input:focus ~ .placeholder,
          .input:not(:placeholder-shown) ~ .placeholder {
            transform: translateY(-30px) translateX(10px) scale(0.75);
          }
          
          .input:not(:placeholder-shown) ~ .placeholder {
            color: #808097;
          }
        #main {margin-left: 120px}
        /* Remove margins from "page content" on small screens */
        @media only screen and (max-width: 600px) {#main {margin-left: 0}}
        .link:link, .link:visited {
          background-color: #08d;
          border-radius: 12px;
          color: white;
          padding: 14px 25px;
          font-size: 18px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          width: 30%;
        }
        .title {
            color: #eee;
            font-family: sans-serif;
            font-size: 36px;
            font-weight: 600;
            margin-top: 30px;
          }
          
          .subtitle {
            color: #eee;
            font-family: sans-serif;
            font-size: 16px;
            font-weight: 600;
            margin-top: 10px;
          }
          
        .link:hover, .link:active {
            background-color: #06b;
        }
        </style>
        </head>
        <body class="w3-black" style="background-color: #303245;">
        <!-- Icon Bar (Sidebar - hidden on small screens) -->
        <nav class="w3-sidebar w3-bar-block w3-small w3-hide-small w3-center">
          <!-- Avatar image in top left corner -->
          <a href="{{url_for('home')}}" class="w3-bar-item w3-button w3-padding-large w3-black">
            <i class="fa fa-home w3-xxlarge"></i>
            <p>HOME</p>
          </a>
          <a href="{{url_for('home')}}" class="w3-bar-item w3-button w3-padding-large w3-hover-black">
            <i class="fa fa-user w3-xxlarge"></i>
            <p>ABOUT</p>
          </a>
          <a href="{{url_for('predict')}}" class="w3-bar-item w3-button w3-padding-large w3-hover-black">
            <i class="fa fa-eye w3-xxlarge"></i>
            <p>Diagnosis</p>
          </a>
        </nav>
        <!-- Navbar on small screens (Hidden on medium and large screens) -->
        <div class="w3-top w3-hide-large w3-hide-medium" id="myNavbar">
          <div class="w3-bar w3-black w3-opacity w3-hover-opacity-off w3-center w3-small">
            <a href="#" class="w3-bar-item w3-button" style="width:25% !important">HOME</a>
            <a href="#about" class="w3-bar-item w3-button" style="width:25% !important">ABOUT</a>
            <a href="#photos" class="w3-bar-item w3-button" style="width:25% !important">PHOTOS</a>
            <a href="#contact" class="w3-bar-item w3-button" style="width:25% !important">CONTACT</a>
          </div>
        </div>
        <!-- Page Content -->
        <div class="w3-padding-large" id="main">
            <header class="w3-container w3-padding-32 w3-center w3-black" id="home">
            <h1 class="w3-jumbo"><span class="w3-hide-small">Based on the given values for the attributes, the person has been diagnosed 
                <span style="font-weight: bold; color:#08d;">'''+result+'''</span>
                for Chronic Kidney Disease.
            </span></h1>
            </header>
        </div>
        </body>
        </html>
'''
    return render_template('index.html')
if __name__ == '__main__':
    app.run()
