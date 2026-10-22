from app import app, db, Listing


def test_read_listing_page_shows_listing_details():
    with app.app_context():
        db.create_all()
        listing = Listing(
            title="ZZZ Read Listing Test 98765",
            description="Full description for automated read listing test",
            price=42.50
        )
        db.session.add(listing)
        db.session.commit()
        listing_id = listing.id

    try:
        client = app.test_client()
        response = client.get(f"/buy/{listing_id}")

        assert response.status_code == 200
        assert b"ZZZ Read Listing Test 98765" in response.data
        assert b"Full description for automated read listing test" in response.data
        assert b"$42.50" in response.data

    finally:
        with app.app_context():
            listing = db.session.get(Listing, listing_id)
            if listing:
                db.session.delete(listing)
                db.session.commit()


def test_read_listing_returns_404_for_missing_listing():
    with app.app_context():
        db.create_all()

    client = app.test_client()
    response = client.get("/buy/999999999")

    assert response.status_code == 404
