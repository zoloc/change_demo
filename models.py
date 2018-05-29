from exts import db

class Impact_list(db.Model):
    __tablename__ = 'impact_list'
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cfg_of_change_authority = db.Column(db.Text)
    change_type = db.Column(db.Text)
    pn_bef = db.Column(db.Text)
    edition_bef = db.Column(db.Text)
    quantity_bef = db.Column(db.Integer)
    effectivity_bef = db.Column(db.Integer)
    pn_after = db.Column(db.Text)
    edition_aft = db.Column(db.Text)
    quantity_aft = db.Column(db.Text)
    effectivity_aft = db.Column(db.Text)

class Hi_dm_list(db.Model):
    __tablename__ = 'hi_dm_list'
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edz = db.Column(db.Integer, nullable=False)
    dci = db.Column(db.String(50),nullable=False)
    AC103_pn = db.Column(db.String(20))
    AC104_pn = db.Column(db.String(20))