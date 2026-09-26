"""
Main entry point for the Lost and Found Management System.
Provides a simple command-line menu to interact with the system.
"""

from item import LostItem, FoundItem
from user import User
from database import Database
from search import MatchingEngine
from claim import ClaimManager
from utils import validate_input, format_item_summary


def report_lost_item(db, current_user):
    category = input("Category (e.g. Wallet, Phone, Keys): ")
    description = input("Description: ")
    location = input("Location lost: ")

    validate_input(
        {"category": category, "description": description, "location": location},
        ["category", "description", "location"]
    )

    item = LostItem(category, description, location, reported_by=current_user.user_id)
    db.save_item(item)
    print(f"\nLost item reported successfully. ID: {item.item_id}\n")


def report_found_item(db, current_user):
    category = input("Category (e.g. Wallet, Phone, Keys): ")
    description = input("Description: ")
    location = input("Location found: ")

    validate_input(
        {"category": category, "description": description, "location": location},
        ["category", "description", "location"]
    )

    item = FoundItem(category, description, location, found_by=current_user.user_id)
    db.save_item(item)
    print(f"\nFound item reported successfully. ID: {item.item_id}\n")


def search_items(matcher):
    keyword = input("Search keyword (or press Enter to skip): ").strip() or None
    category = input("Category (or press Enter to skip): ").strip() or None
    location = input("Location (or press Enter to skip): ").strip() or None

    results = matcher.search(keyword=keyword, category=category, location=location)

    if not results:
        print("\nNo matching items found.\n")
        return

    print(f"\nFound {len(results)} item(s):")
    for item in results:
        print(" -", format_item_summary(item))
    print()


def submit_claim(db, claim_manager, current_user):
    item_id = input("Enter the Item ID you want to claim: ").strip()
    proof = input("Describe proof of ownership: ").strip()

    claim = claim_manager.submit_claim(item_id, current_user.user_id, proof)
    print(f"\nClaim submitted. Claim ID: {claim.claim_id} (status: pending)\n")


def main():
    db = Database()
    matcher = MatchingEngine(db)
    claim_manager = ClaimManager(db)

    print("Welcome to the Lost and Found Management System")
    name = input("Enter your name: ").strip()
    contact = input("Enter your contact info: ").strip()

    current_user = User(name, contact, role="user")
    db.save_user(current_user)

    while True:
        print("\n--- MENU ---")
        print("1. Report Lost Item")
        print("2. Report Found Item")
        print("3. Search Items")
        print("4. Submit a Claim")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            report_lost_item(db, current_user)
        elif choice == "2":
            report_found_item(db, current_user)
        elif choice == "3":
            search_items(matcher)
        elif choice == "4":
            submit_claim(db, claim_manager, current_user)
        elif choice == "5":
            print("Goodbye!")
            db.close()
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
