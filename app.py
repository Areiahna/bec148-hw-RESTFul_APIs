from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from password import my_password

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{my_password}@localhost/fitness_center'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Create Flask routes to add, retrieve, update, and delete members from the Members table.
# Use appropriate HTTP methods: POST for adding, GET for retrieving, PUT for updating, and DELETE for deleting members.
# Ensure to handle any errors and return appropriate responses.

# --- Structuring member data
class MemberSchema(ma.Schema):
    id = fields.Int(dump_only= True) 
    name = fields.String(required= True) 
    email = fields.String()
    start_date = fields.String()
    session_id = fields.Int()

    class Meta:
        fields = ("id","name", "email", "start_date","session_id")

member_schema = MemberSchema()
members_schema = MemberSchema(many= True)


class Member(db.Model):
    __tablename__ = 'Members'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(150))
    start_date = db.Column(db.Date, nullable=False)
    # One member can have many sessions
    sessions = db.relationship('Session', backref='member')

class SessionSchema(ma.Schema):
    id = fields.Int(dump_only= True) 
    instructor = fields.String(required= True) 
    duration = fields.String()
    session_date = fields.String()
    category = fields.String()
    member_id = fields.Int(nullable=False)

    class Meta:
        fields = ("id","instructor", "duration", "session_date","category","member_id")

session_schema = SessionSchema()
sessions_schema = SessionSchema(many= True)

class Session(db.Model):
    __tablename__ = "Workout_Sessions"
    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String(75), nullable=False)
    instructor = db.Column(db.String(75), nullable=False)
    duration = db.Column(db.String(30))
    session_date = db.Column(db.Date,nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('Members.id'))


# Initialize the database
with app.app_context():
    db.create_all()


# --- GET MEMBERS
@app.route('/members')
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)


# --- ADD MEMBER 
@app.route('/members', methods=['POST'])
def add_member():
    try:
        # Validate and deserialize input
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_member =                                                            Member(name=member_data['name'],
          email=member_data['email'],
          start_date=member_data['start_date'])
                                                                 
    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "New member added succesfully"}),201


# --- UPDATE MEMBER
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get_or_404(id)
    try:
        member_data= member_schema.load(request.json)    

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    member.name = member_data['name']
    member.email = member_data['email']
    member.start_date = member_data['start_date']
    db.session.commit()

    return jsonify({"message": "Member details updated sucessfully"}), 200
    
# --- DELETE MEMBER
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()

    return jsonify({"message": "Member removed successfully"}), 200

#  Develop routes to schedule, update, and view workout sessions. Implement a route to retrieve all workout sessions for a specific member.

# --- VIEW SESSIONS
@app.route('/sessions')
def get_sessions():
    sessions = Session.query.all()
    return sessions_schema.jsonify(sessions)


# --- GET SESSIONS BY MEMBER
@app.route('/sessions/by-member_id', methods=['GET'])
def get_member_sessions():
    member_id = request.args.get('member_id')
    sessions = Session.query.filter_by(member_id=member_id).all()
    if sessions:
        return sessions_schema.jsonify(sessions)
    else:
        return jsonify({"message : Member sessions not found"}), 404


# --- SCHEDULE SESSIONS
@app.route('/sessions', methods=['POST'])
def schedule_session():
    try:
        # Validate and deserialize input
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_session =                                                           Session(category=session_data['category'],
          instructor=session_data['instructor'],
          session_date=session_data['session_date'],
          duration=session_data['duration'],
          member_id=session_data['member_id']
          )
                                                                 
    db.session.add(new_session)
    db.session.commit()

    return jsonify({"message": "New session scheduled succesfully"}),201


# --- UPDATE SESSIONS
@app.route('/sessions/<int:id>', methods=['PUT'])
def update_session(id):
    session = Session.query.get_or_404(id)
    try:
        session_data= session_schema.load(request.json)    

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    session.instructor = session_data['instructor']
    session.category = session_data['category']
    session.session_date = session_data['session_date']
    session.duration = session_data['duration']
    session.member_id = session_data['member_id']
    db.session.commit()

    return jsonify({"message": "Workout Session details updated sucessfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)