from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json, make_response, send_file
import pandas as pd
import config, os, string
from func import impact_list_preprocess
from exts import db#, bs
from sqlalchemy import create_engine, distinct
from datetime import datetime
from calendar import timegm
from models import Impact_list, Hi_dm_list



app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
#bs.init_app(app)


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
    # On work: Use Ajax to update a notice in web tell user which HI/HA has no impacted data in database
    if request.method == 'GET':
        context = {
            'ImpactData_edz': Impact_list.query.with_entities(Impact_list.edz).filter(Impact_list.edz != None).distinct(),
            'ImpactData_harness': Impact_list.query.with_entities(Impact_list.harness).filter(Impact_list.harness != None).distinct()
        }
        return render_template('impact_list_extract.html', **context)


@app.route('/impact_list_download/', methods=['POST'])
def impact_list_download():
    '''
    This funcation query column 'edz' in database and return an impact list with .xlsx format for user downloading.
    User aware: Data not exist in impact assessment database could not show
    on work: For DCN do not have impact data which is contained by EDZ, need an additional to filter and add them into impact list
    '''

    edz_str = request.form.get('edz')
    harness_str = request.form.get('harness')

    print(edz_str)
    print(harness_str)
    # edz_str作为一个string返回多个用户选择的edz以逗号相隔的列表，E.X. '111, 222, 555'，这个列表可以直接用于SQL查询语句使用

    engine = create_engine('mysql+pymysql://root:init#201605@127.0.0.1:3306/change_demo?charset=utf8')

    if edz_str:
        df = pd.read_sql_query("SELECT * FROM impact_list WHERE edz in (%s)" % edz_str, engine, index_col='index')
        df = df.reset_index(drop=True)
        xlsdir = os.path.join(app.root_path, 'static/tmp','impact_list_%s.xlsx'%timegm(datetime.utcnow().timetuple()))
        df.to_excel(xlsdir, sheet_name='Sheet1')
        response = make_response(send_file(xlsdir))
        response.headers["Content-Disposition"] = "attachment; filename=impact_list_%s.xlsx"%timegm(datetime.utcnow().timetuple())
        return response
    elif harness_str:
        df = pd.read_sql_query("SELECT * FROM impact_list WHERE harness in (%s)" % harness_str, engine, index_col='index')
        df = df.reset_index(drop=True)
        xlsdir = os.path.join(app.root_path, 'static/tmp',
                              'impact_list_%s.xlsx' % timegm(datetime.utcnow().timetuple()))
        df.to_excel(xlsdir, sheet_name='Sheet1')
        response = make_response(send_file(xlsdir))
        response.headers["Content-Disposition"] = "attachment; filename=impact_list_%s.xlsx" % timegm(
            datetime.utcnow().timetuple())
        return response


if __name__ == '__main__':
    app.run() #host="10.180.35.86"