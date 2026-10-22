# Campus Marketplace

Campus Marketplace is a web application developed for COSC 412 Software Engineering at Towson University. The application is designed to provide students with a simple marketplace for creating and searching item listings.

## Current Features

- Create marketplace listings
- Enter a title, description, and price for each listing
- Validate required listing fields
- Validate listing prices
- Display available listings on the marketplace homepage
- Search listings by title
- Display a message when no listings match a search
- Reset a search to display all listings

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML/CSS
- Pytest
- GitHub Actions

## Project Structure

```text
campus-marketplace/
├── app.py
├── requirements.txt
├── static/
├── templates/
├── tests/
│   ├── conftest.py
│   ├── test_create_listing.py
│   └── test_search.py
└── .github/
    └── workflows/
        └── tests.yml
```

## Setup

Clone the repository:

```bash
git clone https://github.com/EgeKalenderoglu/campus-marketplace.git
cd campus-marketplace
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the application in a browser at:

```text
http://127.0.0.1:5000
```

## Automated Testing

The project currently includes automated tests for the Create Listing and Search features.

Run all tests with:

```bash
python -m pytest -v
```

The current test suite checks:

- Create Listing page loads successfully
- Required listing fields are validated
- Invalid prices are rejected
- Search returns matching listings
- Search displays a no-results message when appropriate
- Resetting search displays all listings

## Continuous Integration

GitHub Actions automatically runs the test suite when code is pushed or when a pull request is opened.

This helps verify that new changes do not break existing functionality before they are merged into the main branch.

## Development Workflow

New work should be completed on a separate Git branch.

Typical workflow:

```text
Create feature branch
        ↓
Make changes
        ↓
Run tests
        ↓
Push branch to GitHub
        ↓
Open pull request
        ↓
GitHub Actions runs tests
        ↓
Review and merge into main
```