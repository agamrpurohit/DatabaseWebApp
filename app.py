from flask import Flask, render_template, request
from flask_sqlalchemy  import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func 

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:postgres123@localhost/height_collector'
#app.config["SQLALCHEMY_DATABASE_URI"]='postgres://pfohugbcxhhqko:0984a595ccf535705a9a0e1b35407a77c3545611f342276d21f57a06d1c123a1@ec2-54-159-138-67.compute-1.amazonaws.com:5432/d9ro1ivnto7n7n?sslmode=require'
#app.config["SQLALCHEMY_DATABASE_URI"]='postgres://kipsxnxvormwkl:9194c43ade5f7e871ae514d860af27eb2b39ca16dfe36901bf11610e87c2a945@ec2-54-243-67-199.compute-1.amazonaws.com:5432/debj90jofe3a4l?sslmode=require'
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120), unique=True)
    height=db.Column(db.Integer)

    def __init__(self,email,height):
        self.email=email
        self.height=height 

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/success/',methods=['POST'])
def success():
    if request.method=="POST":
        email=request.form["email_name"]
        height=request.form["height_name"]
        
        if db.session.query(Data).filter(Data.email==email).count()== 0: 
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height)).scalar()
            average_height=round(average_height,2)
            count=db.session.query(Data.height).count()
            send_email(email, height, average_height, count)
            return render_template("success.html")        
    return render_template('index.html',
            text="Seems like we've got something from that email address already!")

if __name__=="__main__":
    app.debug=True
    app.run()