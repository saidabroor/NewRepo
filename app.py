from flask import Flask, request, render_template, method
import pandas as pd
import numpy as np

application = Flask(__name__)

app = application

@app.route('/')
def index():
   return render_template('template/index.html')

@app.route('/ predictdata', method=['GET', 'POST'])
def predict_datapoint():
   if request.method == 'GET':
      return render_template('home.html')
   else:
      return CustomData
