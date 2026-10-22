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


def test_create_listing_saves_valid_listing():
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
