import app as app_module
from app import app, db, Listing


def test_create_listing_page_loads():
    client = app.test_client()

    response = client.get("/create")

    assert response.status_code == 200
    assert b"Create Listing" in response.data


def test_create_listing_requires_all_fields():
    client = app.test_client()

    response = client.post(
        "/create",
        data={
            "title": "",
            "description": "",
            "price": ""
        }
    )

    assert response.status_code == 200
    assert b"All fields are required" in response.data


def test_create_listing_rejects_invalid_price():
    client = app.test_client()

    response = client.post(
        "/create",
        data={
            "title": "Calculus Textbook",
            "description": "Used textbook",
            "price": "invalid"
        }
    )

    assert response.status_code == 200
    assert b"Please enter a valid price" in response.data


def test_create_listing_saves_valid_listing(monkeypatch):
    monkeypatch.setattr(
        app_module.moderation,
        "moderate_listing",
        lambda title, description: {
            "allowed": True,
            "flagged": False,
            "error": False,
            "reason": "Listing passed moderation."
        }
    )

    with app.app_context():
        db.create_all()

    client = app.test_client()
    test_title = "ZZZ Valid Listing Test 98765"

    try:
        response = client.post(
            "/create",
            data={
                "title": test_title,
                "description": "Temporary automated test listing",
                "price": "19.99"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert test_title.encode() in response.data

        with app.app_context():
            listing = Listing.query.filter_by(title=test_title).first()
            assert listing is not None
            assert listing.description == "Temporary automated test listing"
            assert listing.price == 19.99

    finally:
        with app.app_context():
            Listing.query.filter_by(title=test_title).delete()
            db.session.commit()


def test_flagged_listing_is_not_saved(monkeypatch):
    test_title = "ZZZ Flagged Integration Test 98765"

    monkeypatch.setattr(
        app_module.moderation,
        "moderate_listing",
        lambda title, description: {
            "allowed": False,
            "flagged": True,
            "error": False,
            "reason": "Listing was flagged by AI moderation."
        }
    )

    with app.app_context():
        db.create_all()

    client = app.test_client()
    response = client.post(
        "/create",
        data={
            "title": test_title,
            "description": "Flagged integration test",
            "price": "10.00"
        }
    )

    assert response.status_code == 200
    assert b"flagged by AI moderation" in response.data

    with app.app_context():
        assert Listing.query.filter_by(title=test_title).first() is None


def test_moderation_failure_does_not_publish_listing(monkeypatch):
    test_title = "ZZZ Moderation Failure Test 98765"

    monkeypatch.setattr(
        app_module.moderation,
        "moderate_listing",
        lambda title, description: {
            "allowed": False,
            "flagged": False,
            "error": True,
            "reason": "Moderation service unavailable. Please try again."
        }
    )

    with app.app_context():
        db.create_all()

    client = app.test_client()
    response = client.post(
        "/create",
        data={
            "title": test_title,
            "description": "Moderation failure integration test",
            "price": "10.00"
        }
    )

    assert response.status_code == 200
    assert b"Moderation service unavailable" in response.data

    with app.app_context():
        assert Listing.query.filter_by(title=test_title).first() is None
