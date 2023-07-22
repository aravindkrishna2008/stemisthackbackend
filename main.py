from flask import Flask, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

from auth import create_user, verify_username_password


from stocks import get_entire_stock_history, adjust_randomness

# Create a Flask app
app = Flask(__name__)
# Allow CORS for all routes
CORS(app)


# Define a route for the home page
@app.route("/")
def home():
    return "Hello, this is a simple Flask server with CORS enabled!"


# Define a route for the stock history
@app.route("/stock_history/<int:amount>/<int:randomness_param>")
def stock_history(amount, randomness_param):
    return str(
        adjust_randomness(
            get_entire_stock_history(amount, randomness_param), randomness_param
        )
    )


@app.route("/auth", methods=["POST"])
def auth():
    data = request.json
    name = data.get("name")
    password = data.get("password")

    try:
       # Create a query to search for documents in the 'users' collection with the specified name
        query = db.collection("users").where("name", "==", name).limit(1)
        a = False

        # Get the query results (should be at most one document)
        query_results = query.stream()

        for _ in query_results:
            # If the loop is entered, a document with the specified name was found
            print(f"The name '{name}' exists in the 'users' collection.")
            a = True
            # return str(True)
        if a:
           if verify_username_password(name, password):
               return "verified user"
           else:
                return "wrong password"
        else:
            create_user(name, password)
            return "created user"
    except Exception as e:
        print(f"Error checking name in Firestore: {e}")
        return str(False)


@app.route("/leaderboard/add", methods=["POST"])
def add_to_leaderboard():
    # Get the JSON data from the request
    data = request.json
    print("hi")
    # Get the player's name and score from the JSON data
    name = data.get("name")
    score = data.get("score")
    doc_ref = db.collection("leaderboard").document(name)
    doc_ref.set({"name": name, "score": score})
    return name + "Added to leaderboard"


@app.route("/leaderboard/get")
def get_leaderboard():
    docs = db.collection("leaderboard").stream()
    leaderboard = []
    for doc in docs:
        leaderboard.append(doc.to_dict())
    return str(leaderboard)


if __name__ == "__main__":
    # Run the app in debug mode on http://127.0.0.1:5000/
    app.run(host="0.0.0.0", port=8000, debug=True)
