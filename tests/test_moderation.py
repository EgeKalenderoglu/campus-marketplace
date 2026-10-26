from types import SimpleNamespace

import moderation
from moderation import moderate_listing


class FakeModerations:
    def __init__(self, flagged):
        self.flagged = flagged
        self.last_model = None
        self.last_input = None

    def create(self, model, input):
        self.last_model = model
        self.last_input = input
        return SimpleNamespace(
            results=[SimpleNamespace(flagged=self.flagged)]
        )


class FakeClient:
    def __init__(self, flagged):
        self.moderations = FakeModerations(flagged)


def test_safe_listing_is_allowed():
    client = FakeClient(flagged=False)

    result = moderate_listing(
        "Calculus Textbook",
        "Used calculus textbook in good condition.",
        client=client
    )

    assert result["allowed"] is True
    assert result["flagged"] is False
    assert client.moderations.last_model == "omni-moderation-latest"
    assert "Calculus Textbook" in client.moderations.last_input


def test_flagged_listing_is_rejected():
    client = FakeClient(flagged=True)

    result = moderate_listing(
        "Flagged Test Listing",
        "Content that the moderation service flags.",
        client=client
    )

    assert result["allowed"] is False
    assert result["flagged"] is True
    assert "flagged" in result["reason"].lower()


class FailingModerations:
    def create(self, model, input):
        raise RuntimeError("API unavailable")


class FailingClient:
    def __init__(self):
        self.moderations = FailingModerations()


def test_moderation_failure_blocks_listing():
    result = moderate_listing(
        "Test Listing",
        "Test description",
        client=FailingClient()
    )

    assert result["allowed"] is False
    assert result["error"] is True
    assert "unavailable" in result["reason"].lower()


def test_client_creation_failure_is_handled(monkeypatch):
    def fail_client():
        raise RuntimeError("Missing API key")

    monkeypatch.setattr(moderation, "OpenAI", fail_client)

    result = moderate_listing(
        "Test Listing",
        "Test description"
    )

    assert result["allowed"] is False
    assert result["error"] is True
    assert "unavailable" in result["reason"].lower()
