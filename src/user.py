"""
User module - defines the User class for the Lost and Found Management System.
"""

import uuid


class User:
    """Represents any person using the system - regular user or admin."""

    def __init__(self, name, contact_info, role="user"):
        self.user_id = str(uuid.uuid4())[:8]
        self.name = name
        self.contact_info = contact_info
        self.role = role  # "user" or "admin"

    def is_admin(self):
        return self.role == "admin"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "contact_info": self.contact_info,
            "role": self.role,
        }

    def __str__(self):
        return f"[{self.user_id}] {self.name} ({self.role})"
