from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import config
from lib import impact_list_preprocess
from exts import db
from sqlalchemy import create_engine
import json

from models import Impact_list, Hi_dm_list

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_impact_list/', methods=['GET', 'POST'])
def upload_impact_list():
    if request.method == 'GET':
        return render_template('upload_impact_list.html')
    else:
        # on work: Input Excel check, error return
        file = request.files['upload_impact_list']
        df = impact_list_preprocess(file)
        yconnect = create_engine('mysql+pymysql://root:init#201605@127.0.0.1:3306/change_demo?charset=utf8')
        pd.io.sql.to_sql(df, 'impact_list', yconnect, schema='change_demo', if_exists='replace')
        return render_template('upload_success.html', upload_filename='Impact List ')


@app.route('/impact_list_extract', methods=['GET','POST'])
def impact_list_extract():
    if request.method == 'GET':
        context = {
            'HIs' : Hi_dm_list.query.all()
        }
        return render_template('impact_list_extract.html', **context)
    else:
        edz_list = request.get_json('edz_data')
        print(edz_list)
        return render_template('extract_result.html', edz_list=edz_list)


if __name__ == '__main__':
    app.run()
