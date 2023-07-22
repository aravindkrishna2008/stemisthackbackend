import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore




db = firestore.client()


def create_user(name, password):
    doc_ref = db.collection("users").document(name)
    doc_ref.set({"name": name, "password": password})
    return name + "Added to users"


def verify_username_password(name, password):
    doc_ref = db.collection("users").document(name)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()["password"] == password
    else:
        return False


# create_user("test", "abc12345")
print(verify_username_password("test", "abc123456"))