"""
Claim module - handles claim requests and their verification
for the Lost and Found Management System.
"""

import uuid
from datetime import date


class ClaimRequest:
    """Represents a claim made by a user for a found item."""

    def __init__(self, item_id, claimant_id, proof_description, status="pending", date_resolved=None):
        self.claim_id = str(uuid.uuid4())[:8]
        self.item_id = item_id
        self.claimant_id = claimant_id
        self.proof_description = proof_description
        self.status = status              # pending, verified, rejected
        self.date_resolved = date_resolved

    def to_dict(self):
        return {
            "claim_id": self.claim_id,
            "item_id": self.item_id,
            "claimant_id": self.claimant_id,
            "proof_description": self.proof_description,
            "status": self.status,
            "date_resolved": self.date_resolved,
        }

    def __str__(self):
        return f"[{self.claim_id}] Item {self.item_id} claimed by {self.claimant_id} ({self.status})"


class ClaimManager:
    """Handles the verification workflow for claim requests."""

    def __init__(self, database):
        self.db = database

    def submit_claim(self, item_id, claimant_id, proof_description):
        claim = ClaimRequest(item_id, claimant_id, proof_description)
        self.db.save_claim(claim)
        return claim

    def verify_claim(self, claim, approved, admin_user):
        """
        Approves or rejects a claim. If approved, marks the related item
        as 'claimed' in the database.
        """
        if not admin_user.is_admin():
            raise PermissionError("Only an admin can verify claims.")

        claim.status = "verified" if approved else "rejected"
        claim.date_resolved = date.today().isoformat()
        self.db.save_claim(claim)

        if approved:
            self.db.update_item_status(claim.item_id, "claimed")

        return claim
