import json
import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        port=5432
    )

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }

def lambda_handler(event, context):

    method = event['requestContext']['http']['method']

    conn = get_connection()
    cursor = conn.cursor()

    try:

        if method == "POST":
            body = json.loads(event['body'])
            cursor.execute(
                "INSERT INTO users (name,email,age) VALUES (%s,%s,%s) RETURNING id;",
                (body['name'], body['email'], body['age'])
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            return response(200, {"message": f"User created ID {user_id}"})

        elif method == "GET":
            cursor.execute("SELECT * FROM users;")
            rows = cursor.fetchall()
            return response(200, {"users": rows})

        elif method == "PUT":
            body = json.loads(event['body'])
            cursor.execute(
                "UPDATE users SET name=%s, age=%s WHERE email=%s;",
                (body['name'], body['age'], body['email'])
            )
            conn.commit()
            return response(200, {"message": "User updated"})

        elif method == "DELETE":
            body = json.loads(event['body'])
            cursor.execute(
                "DELETE FROM users WHERE email=%s;",
                (body['email'],)
            )
            conn.commit()
            return response(200, {"message": "User deleted"})

        else:
            return response(400, {"message": "Unsupported method"})

    except Exception as e:
        return response(500, {"error": str(e)})

    finally:
        cursor.close()
        conn.close()
