from firebase_admin import firestore

from setup.firebase_setup import db
import logging
logger = logging.getLogger(f"pawplan.{__name__}")

def get_specific_pet(uid, index):
    pet_list = get_pet_list(uid)

    # return dict
    pet_details = pet_list[index]
    return pet_details

def get_pet_list(uid):
    pet_list = []

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

def remove_pet(uid, name):
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