# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import math
from flask import Flask, request, render_template
import re

app = Flask("__name__")

@app.route("/")
def loadPage():
    return render_template('home.html',query="")

@app.route("/", methods=['POST'])
def cancerPrediction():
    dataset_url = "https://raw.githubusercontent.com/apogiatzis/breast-cancer-azure-ml-notebook/master/breast-cancer-data.csv"
    df = pd.read_csv(dataset_url)
    
    inputQuery1=request.form['query1']
    inputQuery2=request.form['query2']
    inputQuery3=request.form['query3']
    inputQuery4=request.form['query4']
    inputQuery5=request.form['query5']
    
    df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})
    
    features = ['radius_mean', 'texture_mean', 'perimeter_mean', 'smoothness_mean', 'compactness_mean']

    X = df[features]
    y = df.diagnosis
    
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)
    
    model = RandomForestClassifier(n_estimators=500,n_jobs=-1)
    model.fit(X_train, y_train)
    
    #prediction = model.predict(X_test)
    
    data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5]]
    
    new_df = pd.DataFrame(data, columns=['radius_mean', 'texture_mean', 'perimeter_mean', 'smoothness_mean', 'compactness_mean'])
    single = model.predict(new_df)
    proba = model.predict_proba(new_df)[:,1]
    
    if single==1:
        output1= "The patient is diagnosed with Breast Cancer"
        output2 = "Confidence: {}".format(proba*100)
    else:
        output1 = "The patient is not diagnosed with Breast Cancer"
        output2 = ""
    
    return render_template('home.html', output1=output1, output2=output2, query1=request.form['query1'], query2=request.form['query2'], query3=request.form['query3'], query4=request.form['query4'], query5=request.form['query5'])

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render gives PORT dynamically
    app.run(host="0.0.0.0", port=port)
