from app import app


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
