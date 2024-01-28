import os
from os import path
from pathlib import Path

from flask import Flask, render_template, request, jsonify
from flask_frozen import Freezer
import plotly.express as px
import pandas as pd
# import joblib
import numpy as np

# # Load models and preprocessor
# targets = ['Estr110', 'EstrInjec110', 'EstrProgComb110', 'OtherHormone1']

# models = {target: joblib.load(f"{target}_model.pkl") for target in targets}
# preprocessor = joblib.load("preprocessor.pkl")

template_folder = path.abspath('./wiki')

app = Flask(__name__, template_folder=template_folder)
#app.config['FREEZER_BASE_URL'] = environ.get('CI_PAGES_URL')
app.config['FREEZER_DESTINATION'] = 'public'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
freezer = Freezer(app)

@app.cli.command()
def freeze():
    freezer.freeze()

@app.cli.command()
def serve():
    freezer.run()

#experimenting with plotly - following is from chatgpt

@app.route('/')
def home():  
    data = {
        #More accurately, "Non-Hispanic/Latinx White", "Non-Hispanic/Latinx Black", "Hispanic/Latinx"
    "Ethnicity": ["White", "Black", "Latinx"],
    "Odds Ratio": [1, 0.74, 0.68]
    }
    fig = px.bar(data, x='Ethnicity', y='Odds Ratio', title="HRT Access by Ethnicity")
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',     # Set plot background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',    # Set paper background color to transparent
        font=dict(
        size=18,
        color="white"
    ),
    title_x=.5
)

    plot_div = fig.to_html(full_html=False)
    return render_template('pages/home.html', plot_div=plot_div)


@app.route('/<page>')
def pages(page):
    return render_template(str(Path('pages')) + '/' + page.lower() + '.html')


# @app.route('/modeling', methods=['GET','POST'])
# def modeling():
#     predictions = {}
#     df = {}
#     if request.method == 'POST':
#         data = {
#             'Race': [request.form['Race']],
#             'MenoStatus': [request.form['MenoStatus']],
#             'Age': [int(request.form['Age'])],
#             'Language': [request.form['Language']],
#             'data.INSURAN10': [int(request.form['data.INSURAN10'])],
#             'data.NOTAFFR10': [int(request.form['data.NOTAFFR10'])],
#             'data.INCOME10': [int(request.form['data.INCOME10'])],
#             'data.HOTFLAS10': [int(request.form['data.HOTFLAS10'])]
#         }
#         df = pd.DataFrame(data)

#         predictions = {target: models[target].predict(df)[0] for target in targets}

#     return render_template(str(Path('pages')) + '/' + 'modeling' + '.html', predictions=predictions)

@app.route('/yale/modeling', methods=['GET', 'POST'])
def modeling():
    # feedback = "test feedback"  # To store feedback messages
    # feedback += "Hardcoded model feedback. "
    # feedback += (f'method is {request.method}')
    # # Checking model loading
    # if 'Estr110' in models:
    #     feedback += "Model is loaded. "
    # else:
    #     feedback += "Model is not loaded. "

    # if os.path.exists("Estr110_model.pkl"):
    #     feedback += "Model file exists. "
    # else:
    #     feedback += "Model file does NOT exist. "

    # predictions = {}
    # df = {}

    # if request.method == 'POST':
    #     feedback += "POST request detected. "
    #     feedback += f"Received data: {request.form}. "
    #     data = {
    #         'Race': [request.form['Race']],
    #         'MenoStatus': [request.form['MenoStatus']],
    #         'Age': [int(request.form['Age'])],
    #         'Language': [request.form['Language']],
    #         'data.INSURAN10': [int(request.form['data.INSURAN10'])],
    #         'data.NOTAFFR10': [int(request.form['data.NOTAFFR10'])],
    #         'data.INCOME10': [int(request.form['data.INCOME10'])],
    #         'data.HOTFLAS10': [int(request.form['data.HOTFLAS10'])]
    #     }

    #     # Checking if the data is received
    #     feedback += f"Received data: {data}\n"

    #     df = pd.DataFrame(data)
    #     try:
    #         predictions = {target: models[target].predict(df)[0] for target in targets}
    #     except Exception as e:
    #         feedback += f"Error while making predictions: {e}"

    # return render_template(str(Path('pages')) + '/' + 'modeling' + '.html', predictions=predictions, feedback=feedback)
    return render_template(str(Path('pages')) + '/' + 'modeling' + '.html')

# Main Function, Runs at http://0.0.0.0:8080
if __name__ == "__main__":
    app.run(port=8080)
