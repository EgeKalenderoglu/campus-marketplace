import pytest

from app import app, db, Listing


@pytest.fixture
def search_test_listings():
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

        macbook = Listing(
            title="ZZZ Search MacBook 98765",
            description="Test MacBook listing",
            price=25.00
        )

        textbook = Listing(
            title="ZZZ Search Calculus 98765",
            description="Test textbook listing",
            price=15.00
        )

        db.session.add_all([macbook, textbook])
        db.session.commit()

        listing_ids = [macbook.id, textbook.id]

    yield

    with app.app_context():
        for listing_id in listing_ids:
            listing = db.session.get(Listing, listing_id)
            if listing:
                db.session.delete(listing)

        db.session.commit()


def test_search_finds_matching_listing(search_test_listings):
    client = app.test_client()

    response = client.get("/?q=MacBook+98765")

    assert response.status_code == 200
    assert b"ZZZ Search MacBook 98765" in response.data
    assert b"ZZZ Search Calculus 98765" not in response.data


def test_search_shows_no_results_message(search_test_listings):
    client = app.test_client()

    response = client.get("/?q=DefinitelyNotARealListing98765")

    assert response.status_code == 200
    assert b"No listings found." in response.data


def test_reset_search_shows_all_listings(search_test_listings):
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"ZZZ Search MacBook 98765" in response.data
    assert b"ZZZ Search Calculus 98765" in response.data