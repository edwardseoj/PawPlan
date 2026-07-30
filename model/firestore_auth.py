import logging
from setup.firebase_setup import db
from model.json.create_account_json import NewAccountStore
from model.json.uid_json import UserIdStore

create_account = NewAccountStore()
uid_account = UserIdStore()
logger = logging.getLogger(__name__)

# For new accounts (register and oauth)
def create_user_doc():
    # logger.debug("Creating user document in Firestore...")
    uid = create_account.get_username()
    doc_ref = db.collection("users").document(uid)
    doc = doc_ref.get()

    if doc.exists:
        return
    else:
        data = {"uid": str(uid)}
        db.collection("users").document(str(uid)).set(data)
        uid_account.set(str(uid))  # set uid json
        setup_user_details(uid)
        setup_pet(uid)

def setup_user_details(uid):
    user_data = create_account.get()

    if user_data is None:
        # logger.debug(f"No user details for UID: {uid}")
        pass
    else:
        username = user_data["username"]
        email = user_data["email"]
        gender = user_data["gender"]
        dob = user_data["dob"]

        data = {"username": username, "email": email, "gender": gender, "dob": dob}

        db.collection("users").document(str(uid)).collection("details").document("user details").set(data)
        # logger.debug(f"User details created for UID: {uid}")

def setup_pet(uid):
    db.collection("users").document(uid).collection("details").document("pets").set({"temp": "temp"})

def create_oauth_user_doc(uid: str):
    doc_ref = db.collection("users").document(uid)
    if doc_ref.get().exists:
        return
    doc_ref.set({"uid": str(uid)})
    uid_account.set(str(uid))
    setup_pet(uid)

# to get uid in homepage
def get_uid():
    # set uid
    uid = uid_account.get()

    # check doc
    doc_ref = db.collection("users").document(uid)
    doc = doc_ref.get()

    if doc.exists:
        logger.debug(f"User document exists for UID: {uid}")
        return uid
    else:
        logger.debug(f"User document does not exist for UID: {uid}")
        return None