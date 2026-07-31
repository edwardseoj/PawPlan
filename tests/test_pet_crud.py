"""Unit tests for pet color handling in model.pet_crud.

Firestore is faked via module-level test doubles so these tests never touch
credentials or the network.
"""

import sys
import types
import unittest
from unittest import mock

_firestore = types.ModuleType("firebase_admin.firestore")
_firestore.ArrayUnion = lambda items: ("array_union", items)
_firestore.ArrayRemove = lambda items: ("array_remove", items)

_setup = types.ModuleType("setup.firebase_setup")
_setup.db = mock.MagicMock()

# Seed fake modules before pet_crud is imported, so the real Firestore client
# (which requires pawplan_account.json) is never initialised.
sys.modules.setdefault("firebase_admin.firestore", _firestore)
sys.modules.setdefault("setup.firebase_setup", _setup)

from model.pet_crud import (
    add_pet,
    get_pet_color_map,
    remove_pet,
    uid_account,
    DEFAULT_PET_COLOR,
    PASTEL_PET_COLORS,
)
from model.task_crud import remove_tasks_by_pet


class PetColorMapTests(unittest.TestCase):
    def test_contains_all_five_pastel_colors(self):
        self.assertEqual(
            list(PASTEL_PET_COLORS.keys()),
            ["Yellow", "Red", "Orange", "Blue", "Green"],
        )

    def test_uses_stored_color(self):
        pets = [
            {"name": "Bella", "color": "#FF8A80"},
            {"name": "Max", "color": "#81D4FA"},
        ]
        with mock.patch("model.pet_crud.get_pet_list", return_value=pets):
            self.assertEqual(
                get_pet_color_map("uid"),
                {"Bella": "#FF8A80", "Max": "#81D4FA"},
            )

    def test_defaults_for_legacy_pets_without_color(self):
        pets = [{"name": "Bella"}, {"name": "Max", "color": ""}]
        with mock.patch("model.pet_crud.get_pet_list", return_value=pets):
            self.assertEqual(
                get_pet_color_map("uid"),
                {"Bella": DEFAULT_PET_COLOR, "Max": DEFAULT_PET_COLOR},
            )

    def test_skips_pets_without_name(self):
        pets = [{"color": "#FFF59D"}]
        with mock.patch("model.pet_crud.get_pet_list", return_value=pets):
            self.assertEqual(get_pet_color_map("uid"), {})


class AddPetColorTests(unittest.TestCase):
    def setUp(self):
        uid_account.clear()
        _setup.db.reset_mock()
        # add_pet now reads the current pet count to enforce MAX_PETS.
        self._pet_list_patch = mock.patch("model.pet_crud.get_pet_list", return_value=[])
        self._pet_list_patch.start()

    def tearDown(self):
        self._pet_list_patch.stop()
        uid_account.clear()

    def _last_pet(self):
        doc = _setup.db.collection.return_value.document.return_value.collection.return_value.document.return_value
        payload = doc.set.call_args.args[0]
        _, pets = payload["pets"]
        return pets[0]

    def test_stores_chosen_color(self):
        uid_account.set("user@example.com")
        ok, _ = add_pet("Bella", "Dog", 3, "Chihuahua", [], "#81D4FA")

        self.assertTrue(ok)
        doc = _setup.db.collection.return_value.document.return_value.collection.return_value.document.return_value
        doc.set.assert_called_once()
        self.assertEqual(doc.set.call_args.kwargs["merge"], True)
        self.assertEqual(self._last_pet()["color"], "#81D4FA")
        self.assertEqual(self._last_pet()["name"], "Bella")

    def test_defaults_color_when_none_passed(self):
        uid_account.set("user@example.com")
        ok, _ = add_pet("Max", "Cat", 2, "Tabby", [], None)
        self.assertTrue(ok)
        self.assertEqual(self._last_pet()["color"], DEFAULT_PET_COLOR)

    def test_aborts_without_uid(self):
        ok, message = add_pet("Bella", "Dog", 3, "Chihuahua", [], "#81D4FA")
        self.assertFalse(ok)
        self.assertIn("not signed in", message)
        _setup.db.collection.assert_not_called()


class AddPetLimitTests(unittest.TestCase):
    def setUp(self):
        uid_account.clear()
        _setup.db.reset_mock()

    def tearDown(self):
        uid_account.clear()

    def _doc(self):
        return _setup.db.collection.return_value.document.return_value.collection.return_value.document.return_value

    def test_rejects_when_at_limit(self):
        uid_account.set("user@example.com")
        pets = [{"name": f"Pet{i}"} for i in range(5)]
        with mock.patch("model.pet_crud.get_pet_list", return_value=pets):
            ok, message = add_pet("Bella", "Dog", 3, "Chihuahua", [], "#81D4FA")

        self.assertFalse(ok)
        self.assertIn("5", message)
        self._doc().set.assert_not_called()

    def test_rejects_when_over_limit(self):
        uid_account.set("user@example.com")
        pets = [{"name": f"Pet{i}"} for i in range(7)]
        with mock.patch("model.pet_crud.get_pet_list", return_value=pets):
            ok, _ = add_pet("Bella", "Dog", 3, "Chihuahua", [], "#81D4FA")

        self.assertFalse(ok)
        self._doc().set.assert_not_called()

    def test_allows_when_under_limit(self):
        uid_account.set("user@example.com")
        pets = [{"name": f"Pet{i}"} for i in range(4)]
        with mock.patch("model.pet_crud.get_pet_list", return_value=pets):
            ok, _ = add_pet("Bella", "Dog", 3, "Chihuahua", [], "#81D4FA")

        self.assertTrue(ok)
        self._doc().set.assert_called_once()


class RemovePetCascadeTests(unittest.TestCase):
    """Deleting a pet must also delete its tasks from the tasks document."""

    def setUp(self):
        uid_account.clear()
        _setup.db.reset_mock()

    def tearDown(self):
        uid_account.clear()

    # The pets and tasks documents are both reached through the same mocked
    # chain, so this is the ref used for both `.update` (pet removal) and
    # `.set` (task rewrite).
    def _doc(self):
        return _setup.db.collection.return_value.document.return_value.collection.return_value.document.return_value

    def test_removes_tasks_that_reference_deleted_pet(self):
        uid_account.set("user@example.com")
        doc = self._doc()
        doc.get.return_value.to_dict.return_value = {
            "pets": [{"name": "Bella", "type": "Dog"}]
        }

        tasks = [
            {"task_name": "Walk", "pet_name": "Bella"},
            {"task_name": "Feed", "pet_name": "Max"},
        ]
        with mock.patch("model.task_crud.get_task_list", return_value=tasks):
            remove_pet("user@example.com", "Bella")

        doc.update.assert_called_once()  # pet removed from pets array
        doc.set.assert_called_once_with(
            {"tasks": [{"task_name": "Feed", "pet_name": "Max"}]},
            merge=True,
        )

    def test_keeps_tasks_document_untouched_when_no_matching_tasks(self):
        uid_account.set("user@example.com")
        doc = self._doc()
        doc.get.return_value.to_dict.return_value = {
            "pets": [{"name": "Bella", "type": "Dog"}]
        }

        with mock.patch("model.task_crud.get_task_list", return_value=[]):
            remove_pet("user@example.com", "Bella")

        doc.update.assert_called_once()
        doc.set.assert_not_called()

    def test_does_nothing_when_pet_not_found(self):
        uid_account.set("user@example.com")
        doc = self._doc()
        doc.get.return_value.to_dict.return_value = {
            "pets": [{"name": "Bella", "type": "Dog"}]
        }

        remove_pet("user@example.com", "Ghost")

        doc.update.assert_not_called()
        doc.set.assert_not_called()

    def test_remove_tasks_by_pet_filters_entire_array(self):
        uid_account.set("user@example.com")
        tasks = [
            {"task_name": "Walk", "pet_name": "Bella"},
            {"task_name": "Groom", "pet_name": "Bella"},
            {"task_name": "Feed", "pet_name": "Max"},
        ]
        with mock.patch("model.task_crud.get_task_list", return_value=tasks):
            remove_tasks_by_pet("Bella")

        self._doc().set.assert_called_once_with(
            {"tasks": [{"task_name": "Feed", "pet_name": "Max"}]},
            merge=True,
        )

    def test_remove_tasks_by_pet_skips_write_without_uid(self):
        remove_tasks_by_pet("Bella")
        _setup.db.collection.assert_not_called()


if __name__ == "__main__":
    unittest.main()
