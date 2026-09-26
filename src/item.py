"""
Item module - defines the core Item class and its Lost/Found variants
for the Lost and Found Management System.
"""

import uuid
from datetime import date


class Item:
    """Base class representing any reported item (lost or found)."""

    def __init__(self, category, description, location, date_reported=None, status="unmatched"):
        self.item_id = str(uuid.uuid4())[:8]      # short unique ID
        self.category = category
        self.description = description
        self.location = location
        self.date_reported = date_reported or date.today().isoformat()
        self.status = status                       # unmatched, possible_match, claimed, disposed

    def update_status(self, new_status):
        valid_statuses = ["unmatched", "possible_match", "claimed", "disposed"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "category": self.category,
            "description": self.description,
            "location": self.location,
            "date_reported": self.date_reported,
            "status": self.status,
        }

    def __str__(self):
        return f"[{self.item_id}] {self.category} - {self.description} ({self.status})"


class LostItem(Item):
    """Represents an item reported as lost by a user."""

    def __init__(self, category, description, location, reported_by, date_reported=None):
        super().__init__(category, description, location, date_reported)
        self.type = "lost"
        self.reported_by = reported_by

    def to_dict(self):
        data = super().to_dict()
        data.update({"type": self.type, "reported_by": self.reported_by})
        return data


class FoundItem(Item):
    """Represents an item reported as found by a user."""

    def __init__(self, category, description, location, found_by, image_path=None, date_reported=None):
        super().__init__(category, description, location, date_reported)
        self.type = "found"
        self.found_by = found_by
        self.image_path = image_path

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": self.type,
            "found_by": self.found_by,
            "image_path": self.image_path,
        })
        return data
