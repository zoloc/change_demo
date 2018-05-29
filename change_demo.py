from flask import Flask, render_template, request, redirect, url_for, session
import config
from exts import db

from models import Impact_list, Hi_dm_list

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)



@app.route('/extract/', methods=['GET','POST'])
def extract():
    a = request.args.get('a', 0, type=int)
    print()
    pass

@app.route('/')
def impact_list():
    context = {
        'HIs' : Hi_dm_list.query.all()
    }
    return render_template('impact_list.html', **context)


if __name__ == '__main__':
    app.run()
