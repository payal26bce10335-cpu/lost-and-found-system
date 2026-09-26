# Lost and Found Management System

A Python 3 command-line application to help institutions (colleges, offices, transit hubs) manage lost and found items — from reporting, to searching and matching, to claim verification.

## Overview

Most institutions still track lost and found items using a physical register or notice board, which makes items hard to search for, match, and reliably return to their owners. This project digitizes that entire process: users can report lost or found items, search the database with filters, get automatic match suggestions between lost and found reports, and submit/verify claims through a tracked workflow.

## Features

- **Report Lost Items** — log a lost item with category, description, and location
- **Report Found Items** — log a found item with category, description, and location
- **Search Items** — filter items by keyword, category, or location
- **Automatic Matching** — a scoring-based matching engine compares lost items against found items and suggests possible matches
- **Claim Submission & Verification** — users submit claims with proof of ownership; admins verify and approve/reject claims
- **Persistent Storage** — all data is stored in a local SQLite database
- **Status Tracking** — items move through statuses: `unmatched → possible_match → claimed`

## Technologies Used

- **Python 3**
- **SQLite3** (built into Python, no separate install needed)
- **unittest** (Python's built-in testing framework)

## Project Structure

## Steps to Install & Run

1. **Install Python 3** from [python.org](https://www.python.org/downloads/) (make sure to check "Add Python to PATH" during install).
2. **Download this repository** — click the green **Code** button on GitHub → **Download ZIP** → extract it. (Or clone it with `git clone` if you have Git installed.)
3. Open a terminal (Command Prompt / Terminal) and navigate into the project's `src` folder:
4. Run the program:
5. Follow the on-screen menu to report items, search, and submit claims.

## Instructions for Testing

Unit tests are included in the `tests/` folder, covering the `Item`, `User`, `ClaimRequest`, and utility functions.

Run all tests from the project's **root folder** (not inside `src`):

## How It Works (Basic Workflow)

1. A user reports a **lost** item or a **found** item with a category, description, and location.
2. The system automatically checks for possible matches between lost and found records using a simple scoring system (matching category, location, and overlapping description keywords).
3. Any user can **search** the database using keyword, category, or location filters.
4. If a user finds their item, they can **submit a claim** with proof of ownership.
5. An **admin** reviews the claim and either verifies it (item status becomes `claimed`) or rejects it.

## Future Enhancements

- Add a graphical user interface (GUI) or web interface
- Add image-based matching for found items with photos
- Add email/SMS notifications when a match is found
- Add an admin dashboard with analytics (most lost categories, average recovery time, etc.)

## Author

Payal
