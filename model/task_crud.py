from firebase_admin import firestore

from model.json.uid_json import UserIdStore
from setup.firebase_setup import db
from datetime import datetime, timezone
import logging
logger = logging.getLogger(f"pawplan.{__name__}")


uid_account = UserIdStore()

# read task
def get_task_list(uid=None):
    task_list = []
    uid = uid or uid_account.get()
    if not uid:
        logger.debug("get_task_list: no uid set, returning empty list")
        return task_list

    tasks_ref = db.collection("users").document(uid).collection("details").document("tasks")

    doc = tasks_ref.get()
    if doc.exists:
        data = doc.to_dict()
        if not data.get("tasks", []):
            logger.debug("task list empty")
        task_list = data.get("tasks", [])
        logger.debug("Task list: %s", task_list)
    else:
        logger.debug("No such document!")

    return task_list

# add task
def add_task(task_name, pet_name, description, alarm):
    uid = uid_account.get()
    if not uid:
        logger.error("add_task: no uid set, aborting")
        return

    tasks_ref = db.collection("users").document(uid).collection("details").document("tasks")

    # append to existing

    # new task based on pet
    tasks_ref.set({
        "tasks": firestore.ArrayUnion([{
            "task_name": task_name,
            "pet_name": pet_name,
            "description": description,
            "created_at": datetime.now(timezone.utc),
            "alarm": alarm,
        }])
    }, merge=True)





# update task

# delete task