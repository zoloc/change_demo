from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json, make_response, send_file
import pandas as pd
import config, os, string
from func import impact_list_preprocess
from exts import db
from sqlalchemy import create_engine

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
        engine = create_engine('mysql+pymysql://root:init#201605@127.0.0.1:3306/change_demo?charset=utf8')
        pd.io.sql.to_sql(df, 'impact_list', engine, schema='change_demo', if_exists='replace')
        return render_template('upload_success.html', upload_filename='Impact List ')


@app.route('/impact_list_extract/', methods=['GET','POST'])
def impact_list_extract():
    if request.method == 'GET':
        context = {
            'HIs' : Hi_dm_list.query.all()
        }
        return render_template('impact_list_extract.html', **context)
    # else:
    #     edz_list = request.get_json('edz_data')
    #     print(edz_list)
    #     return

@app.route('/impact_list_test/', methods=['POST'])
def impact_list_test():
    '''
    This funcation query column 'edz' in database and return an impact list with .xlsx format for user downloading.
    User aware: Data not exist in impact assessment database could not show
    on work: For DCN do not have impact data which is contained by EDZ, need an additional to filter and add them into impact list
    '''
    edz_str = request.form.get('edz')
    edz_list = edz_str.split(',')
    engine = create_engine('mysql+pymysql://root:init#201605@127.0.0.1:3306/change_demo?charset=utf8')

    df = pd.read_sql_query('SELECT * FROM impact_list WHERE edz in (%s)'%edz_str, engine)
    xlsdir = 'C://Users//LKS00085//Python//learn flask//change_demo//static//tempfile//testsave.xlsx'
    df.to_excel(xlsdir, sheet_name='Sheet1')
    response = make_response(send_file(xlsdir))
    response.headers["Content-Disposition"] = "attachment; filename=abc.xlsx"
    return response

# @app.route('/impact_list_test/download/', methods=['GET'])
# def impact_list_test_download(filedir):
#     response = make_response(send_file(filedir))
#     response.headers["Content-Disposition"] = "attachment; filename=%s" % filedir
#     return response

if __name__ == '__main__':
    app.run()
