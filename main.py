from flask import Flask, jsonify, request
app = Flask(__name__)
import psycopg2
import psycopg2.extras
import json


@app.route('/')
def hello_world():
    conn = psycopg2.connect("dbname=eq_crunch_db user=jerryturcios08")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    # return json.dumps(cur.fetchall())
    columns = ("firstName", "lastName", "email", "id", "password")
    results = []
    for row in cur.fetchall():
        results.append(dict(zip(columns, row)))

    return jsonify(results)


@app.route("/user", methods=["POST"])
def add_user():
    print(request.json)
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']

    try:
        conn = psycopg2.connect("dbname=eq_crunch_db user=jerryturcios08")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (firstName, lastName, email, password) VALUES (%s, %s, %s, %s)",
                    (firstName, lastName, email, password))
        conn.commit()
    except Exception as e:
        print(e)
        return "", 400

    return "", 200


@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    progress = request.json['progress']

    try:
        conn = psycopg2.connect("dbname=eq_crunch_db user=jerryturcios08")
        cur = conn.cursor()
        cur.execute("UPDATE USERS SET progress=%s where id=%s",
                    (progress, id))
        conn.commit()
    except Exception as e:
        print(e)
        return "", 400

    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
