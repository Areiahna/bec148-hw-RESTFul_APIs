from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connection import connection, Error

app = Flask(__name__)
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

class SessionSchema(ma.Schema):
    id = fields.Int(dump_only= True) 
    instructor = fields.String(required= True) 
    duration = fields.String()
    session_date = fields.String()
    category = fields.String()

    class Meta:
        fields = ("id","instructor", "duration", "session_date","category")

session_schema = SessionSchema()
sessions_schema = SessionSchema(many= True)

@app.route('/')
def home():
    return "YOUR PAGE IS UP AND RUNNING"

# --- FETCHING MEMBER DATA
@app.route('/members')
def view_members():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "SELECT * FROM members;"

            cursor.execute(query)

            members = cursor.fetchall()

        except Error as e:
            print("Failed to return member data")
            print(f"Error: {e}")

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return members_schema.jsonify(members)

# --- ADDING MEMBER TO SQL DATABASE
@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.message), 400
    
    conn = connection()

    if conn is not None:
        try: 
            cursor = conn.cursor()

            #-- Creating new_member
            new_member = (member_data["name"], member_data["email"], member_data["start_date"])

            # --- SQL COMMAND TO ADD TO MEMBERS TABLE
            query = "INSERT INTO members (name, email, start_date) VALUES (%s, %s, %s)"

            # -- COMMITING/SAVING MEMBER
            cursor.execute(query, new_member)
            conn.commit()

            return jsonify({'message': 'New member added successfully!'}), 200

        except Error as e:
            return jsonify(e.messages), 500
  
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "CONNECTION FAILED SUS"}), 500

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "SELECT * FROM members WHERE id = %s"

            cursor.execute(query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({"error": "Member not found."}), 404

            cursor.execute(query)

        except Error as e:
            print("Failed to return member data")
            print(f"Error: {e}")

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return member_schema.jsonify(member)


# Develop routes to schedule, update, and view workout sessions.
# Implement a route to retrieve all workout sessions for a specific member.

# -- VIEW SESSIONS
@app.route('/sessions')
def view_sessions():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "SELECT * FROM workout_sessions;"

            cursor.execute(query)

            sessions = cursor.fetchall()

        except Error as e:
            print("Failed to return workout_sessions data")
            print(f"Error: {e}")

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return sessions_schema.jsonify(sessions)

# -- UPDATE SESSIONS
@app.route('/sessions/update/<int:id>', methods= ["PUT"])
def update_session(id):
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = "SELECT * FROM workout_sessions WHERE id = %s"
            cursor.execute(query, (id,))
            session = cursor.fetchone()
            if not session :
                return jsonify({"error": "Session was not found."}), 404
            
            updated_session = (session_data['instructor'], session_data['duration'], session_data['session_date'],session_data["category"],id)

            query = "UPDATE workout_sessions SET instructor = %s, duration = %s, session_date = %s, category = %s WHERE id = %s"

            cursor.execute(query, updated_session)
            conn.commit()

            return jsonify({'message': f"Successfully update workout_session {id}"}), 200
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Databse connection failed"}), 500

# -- SCHEDULE SESSION
@app.route('/sessions', methods=['POST'])
def schedule_session():
    try:
        session_data = session_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.message), 400
    
    conn = connection()

    if conn is not None:
        try: 
            cursor = conn.cursor()

            new_session = (session_data["instructor"], session_data["duration"], session_data["session_date"], session_data["category"])

            query = "INSERT INTO workout_sessions (instructor, duration, session_date,category) VALUES (%s, %s, %s, %s)"

            cursor.execute(query, new_session)
            conn.commit()

            return jsonify({'message': 'New session scheduled successfully!'}), 200

        except Error as e:
            return jsonify(e.messages), 500
  
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "CONNECTION FAILED"}), 500

@app.route('/sessions/members/<int:id>', methods=['GET'])
def get_member_sessions(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query ="SELECT * FROM workout_sessions WHERE member_id = %s "
            cursor.execute(query, (id,))
            sessions = cursor.fetchall()

            if not sessions:
                return jsonify({"error": "Sessions not found."}), 404

            cursor.execute(query)

        except Error as e:
            print("Failed to return member sessions data")
            print(f"Error: {e}")

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return sessions_schema.jsonify(sessions)

   

if __name__ == "__main__":
    app.run(debug=True)