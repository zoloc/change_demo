from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import config
from lib import impact_list_preprocess
from exts import db
from sqlalchemy import create_engine

from models import Impact_list, Hi_dm_list

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/input-impact_list/', methods=['GET', 'POST'])
def input():
    if request.method == 'GET':
        return render_template('input-impact_list.html')
    else:
        file = request.files['input-impact_list']
        df = impact_list_preprocess(file)
        yconnect = create_engine('mysql+pymysql://root:init#201605@127.0.0.1:3306/change_demo?charset=utf8')
        pd.io.sql.to_sql(df, 'impact_list', yconnect, schema='change_demo', if_exists='replace')

        return 'Upload Success'


@app.route('/extract/', methods=['GET','POST'])
def extract():
    a = request.args.get('a', 0, type=int)
    print()
    pass

@app.route('/impact_list/')
def impact_list():
    context = {
        'HIs' : Hi_dm_list.query.all()
    }
    return render_template('impact_list.html', **context)


if __name__ == '__main__':
    app.run()
