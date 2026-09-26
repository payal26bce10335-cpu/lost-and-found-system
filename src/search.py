"""
Search module - handles searching items and matching lost items
against found items for the Lost and Found Management System.
"""


class MatchingEngine:
    """Compares lost and found item records to suggest possible matches."""

    def __init__(self, database):
        self.db = database

    def search(self, keyword=None, category=None, location=None):
        """Search all items using given filters."""
        return self.db.search_items(keyword=keyword, category=category, location=location)

    def find_matches(self, lost_item_dict):
        """
        Compare a lost item against all 'found' items in the database
        and return a list of possible matches, best match first.
        """
        all_items = self.db.search_items(category=lost_item_dict.get("category"))
        found_items = [item for item in all_items if item.get("type") == "found"]

        scored_matches = []
        for found in found_items:
            score = self._compare(lost_item_dict, found)
            if score > 0:
                scored_matches.append((score, found))

        scored_matches.sort(key=lambda pair: pair[0], reverse=True)
        return [item for score, item in scored_matches]

    def _compare(self, lost, found):
        """
        Very simple scoring: compares category, location, and description
        keywords. Returns a score from 0 to 3.
        """
        score = 0

        if lost.get("category") and lost.get("category") == found.get("category"):
            score += 1

        if lost.get("location") and found.get("location"):
            if lost["location"].strip().lower() == found["location"].strip().lower():
                score += 1

        lost_desc = (lost.get("description") or "").lower()
        found_desc = (found.get("description") or "").lower()
        lost_words = set(lost_desc.split())
        found_words = set(found_desc.split())
        if lost_words & found_words:  # any overlapping words
            score += 1

        return score
