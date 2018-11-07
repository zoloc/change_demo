from exts import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100),nullable=False)

class Impact_list(db.Model):
    # Extract by TP tool
    # On work: could be saved per change authority in the future
    __tablename__ = 'impact_list'
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    change_number = db.Column(db.Text)
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
    edz = db.Column(db.Integer)
    harness = db.Column(db.Integer)
    type = db.Column(db.Text)


class Hi_dm_list(db.Model):
    # Extract from Engineering Manager/DM Management
    __tablename__ = 'hi_dm_list'
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edz = db.Column(db.Integer, nullable=False)
    dci = db.Column(db.String(50),nullable=False)
    AC103_pn = db.Column(db.String(20))
    AC104_pn = db.Column(db.String(20))


