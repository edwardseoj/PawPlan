from firebase_admin import firestore

from model.json.uid_json import UserIdStore
from setup.firebase_setup import db
from datetime import datetime, timezone, date, timedelta
import logging
import re
logger = logging.getLogger(f"pawplan.{__name__}")


uid_account = UserIdStore()

# Matches the day_names saved by taskboard_input.py's AlarmClockSelector
WEEKDAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _alarm_of(task):
    return task.get("alarm") or {}


def _split_day_names(day_names):
    """Normalize day_names, which may be stored as a list or a joined string."""
    if not day_names:
        return []
    if isinstance(day_names, str):
        return [name.strip() for name in re.split(r"[,\s]+", day_names) if name.strip()]
    return list(day_names)


def task_occurs_on(task, target_date):
    """True if the task's schedule (repeating days or specific date) falls on target_date."""
    day_names = _split_day_names(_alarm_of(task).get("day_names"))
    if day_names:
        return WEEKDAY_NAMES[target_date.weekday()] in day_names
    date_str = _alarm_of(task).get("date")
    if date_str:
        try:
            return date.fromisoformat(date_str) == target_date
        except ValueError:
            return False
    return False


def task_occurrences(tasks, start_date, days_ahead=7):
    """Expand tasks into (occurrence_date, task) pairs, one per scheduled day.

    Repeating tasks are expanded to each selected weekday inside the window;
    single-date tasks yield their date if it falls in the window.
    """
    end_date = start_date + timedelta(days=days_ahead)
    occurrences = []
    for task in tasks:
        day_names = _split_day_names(_alarm_of(task).get("day_names"))
        if day_names:
            for offset in range(days_ahead):
                candidate = start_date + timedelta(days=offset)
                if WEEKDAY_NAMES[candidate.weekday()] in day_names:
                    occurrences.append((candidate, task))
        else:
            date_str = _alarm_of(task).get("date")
            if date_str:
                try:
                    task_date = date.fromisoformat(date_str)
                except ValueError:
                    continue
                if start_date <= task_date < end_date:
                    occurrences.append((task_date, task))
    return occurrences


def split_tasks_by_occurrence(tasks, target_date, days_ahead=7):
    """Split tasks into per-day (date, task) pairs for today and the upcoming week.

    A task scheduled on multiple days (e.g. Fri + Sun) yields one entry per day.
    """
    occurrences = task_occurrences(tasks, target_date, days_ahead)
    todays = [(d, t) for d, t in occurrences if d == target_date]
    upcoming = [(d, t) for d, t in occurrences if d > target_date]
    upcoming.sort(key=lambda pair: pair[0])
    return todays, upcoming


def format_occurrence_date(occ_date, today=None):
    """Short label for a task occurrence, e.g. "Today (Fri)" or "Sun, Aug 02"."""
    today = today or date.today()
    if occ_date == today:
        return f"Today ({occ_date.strftime('%a')})"
    return occ_date.strftime("%a, %b %d")

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