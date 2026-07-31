from firebase_admin import firestore

from model.json.uid_json import UserIdStore
from setup.firebase_setup import db
import logging
logger = logging.getLogger(f"pawplan.{__name__}")
uid_account = UserIdStore()

def get_specific_pet(uid, index):
    pet_list = get_pet_list(uid)

    if not pet_list:
        logger.warning("get_specific_pet: no pets for uid=%s", uid)
        return {}
    return pet_list[index]

def get_pet_list(uid=None):
    pet_list = []
    uid = uid or uid_account.get()
    if not uid:
        logger.debug("get_pet_list: no uid set, returning empty list")
        return pet_list

    pets_ref = db.collection("users").document(uid).collection("details").document("pets")
    doc = pets_ref.get()
    if doc.exists:
        data = doc.to_dict()
        if not data.get("pets", []):
            logger.debug("pet list empty")
        pet_list = data.get("pets", [])
        logger.debug("Pet list: %s", pet_list)
    else:
        logger.debug("No such document!")

    return pet_list

def add_pet(name, pet_type, age, breed, allergies):
    uid = uid_account.get()
    if not uid:
        logger.error("add_pet: no uid set, aborting")
        return

    pets_ref = db.collection("users").document(uid).collection("details").document("pets")
    pets_ref.set({
        "pets": firestore.ArrayUnion([{
            "name": name,
            "type": pet_type,
            "age": age,
            "breed": breed,
            "allergies": allergies
        }])
    }, merge=True)
    logger.info(f"Added pet '{name}' for uid={uid}")

def remove_pet(uid, name):
    if not uid:
        logger.error("remove_pet: no uid set, aborting")
        return

    doc_ref = db.collection("users").document(uid).collection("details").document("pets")
    doc = doc_ref.get()
    data = doc.to_dict()

    pets = data.get("pets", [])
    target = next((pet for pet in pets if pet.get("name") == name), None)

    if target:
        doc_ref.update({
            "pets": firestore.ArrayRemove([target])
        })
    else:
        logger.warning(f"No pet named '{name}' found for uid={uid}")


