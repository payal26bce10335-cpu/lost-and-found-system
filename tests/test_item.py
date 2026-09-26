"""
Basic tests for the Lost and Found Management System.
Run with: python -m unittest discover tests
(Run this from the project's root folder, not inside src/)
"""

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from item import Item, LostItem, FoundItem
from user import User
from claim import ClaimRequest
from utils import validate_input, is_non_empty_string, normalize_text


class TestItem(unittest.TestCase):

    def test_item_creation(self):
        item = Item("Wallet", "Black leather wallet", "Library")
        self.assertEqual(item.category, "Wallet")
        self.assertEqual(item.status, "unmatched")

    def test_update_status_valid(self):
        item = Item("Phone", "Blue phone", "Cafeteria")
        item.update_status("claimed")
        self.assertEqual(item.status, "claimed")

    def test_update_status_invalid(self):
        item = Item("Keys", "Bunch of keys", "Parking lot")
        with self.assertRaises(ValueError):
            item.update_status("not_a_real_status")

    def test_lost_item_type(self):
        lost = LostItem("Bag", "Grey backpack", "Bus stop", reported_by="user123")
        self.assertEqual(lost.type, "lost")
        self.assertEqual(lost.reported_by, "user123")

    def test_found_item_type(self):
        found = FoundItem("Bag", "Grey backpack", "Bus stop", found_by="user456")
        self.assertEqual(found.type, "found")
        self.assertEqual(found.found_by, "user456")


class TestUser(unittest.TestCase):

    def test_user_creation(self):
        user = User("Payal", "payal@example.com")
        self.assertEqual(user.role, "user")
        self.assertFalse(user.is_admin())

    def test_admin_user(self):
        admin = User("Admin One", "admin@example.com", role="admin")
        self.assertTrue(admin.is_admin())


class TestClaim(unittest.TestCase):

    def test_claim_creation(self):
        claim = ClaimRequest(item_id="abc123", claimant_id="user789", proof_description="It's mine")
        self.assertEqual(claim.status, "pending")
        self.assertEqual(claim.item_id, "abc123")


class TestUtils(unittest.TestCase):

    def test_validate_input_success(self):
        data = {"category": "Wallet", "description": "desc", "location": "loc"}
        self.assertTrue(validate_input(data, ["category", "description", "location"]))

    def test_validate_input_missing_field(self):
        data = {"category": "Wallet", "description": ""}
        with self.assertRaises(ValueError):
            validate_input(data, ["category", "description", "location"])

    def test_is_non_empty_string(self):
        self.assertTrue(is_non_empty_string("hello"))
        self.assertFalse(is_non_empty_string("   "))
        self.assertFalse(is_non_empty_string(123))

    def test_normalize_text(self):
        self.assertEqual(normalize_text("  Wallet  "), "wallet")


if __name__ == "__main__":
    unittest.main()
