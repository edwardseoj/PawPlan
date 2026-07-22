import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("./pawplan_account.json")
    firebase_admin.initialize_app(cred)

db = firestore.client(database_id="pawplan")