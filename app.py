from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restful import Resource,Api

app = Flask(__name__)
api =Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///note.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return jsonify({"name":"sandra"})

class Notes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    data=db.Column(db.String(1000),nullable=False)
    date=db.Column(db.DateTime,default=datetime.now())

    def __repr__(self):
        return f"{self.date} : {self.title} : {self.data}"

class Getnotes(Resource):
    def get(self):
        notes = Notes.query.all()
        all_notes = []
        for note in notes:
            note_data = {"id":note.id,"title":note.title,"data":note.data}
            all_notes.append(note_data)
            return {"notes": all_notes},200

class Getnote(Resource):
    def get(self,id):
        note = Notes.query.filter_by(id=id).first()
        if note is None:
            return {"error": "not found"}
        return {note.id: note.title}

class Addnotes(Resource):
    def post(self):
        note = Notes(title=request.json["title"], data=request.json["data"])
        db.session.add(note)
        db.session.commit()
        return {"message":"Note added"},200

class Updatenote(Resource):
    def put(self,id):
        note = Notes.query.filter_by(id=id).first()
        if note is None:
            return {"error": "note not found"}
        note.title=request.json["title"]
        note.data=request.json["data"]
        db.session.commit()
        return {"message":"note updated"}

class Deletenote(Resource):
    def delete(self,id):
        note = Notes.query.filter_by(id=id).first()
        if note:
            db.session.delete(note)
            db.session.commit()
            return {"message": "note deleted"}
        return {"error": " note not found"}


api.add_resource(Getnotes,"/get")
api.add_resource(Getnote,"/get/<id>")
api.add_resource(Addnotes, "/add")
api.add_resource(Updatenote, "/update/<id>")
api.add_resource(Deletenote, "/delete/<id>")

if __name__ == "__main__":
    app.run(debug=True)