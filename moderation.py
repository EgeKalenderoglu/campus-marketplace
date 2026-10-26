from openai import OpenAI


def moderate_listing(title, description, client=None):
    """Check a marketplace listing using OpenAI moderation."""
    content = f"Title: {title}\nDescription: {description}"

    try:
        if client is None:
            client = OpenAI()

        response = client.moderations.create(
            model="omni-moderation-latest",
            input=content
        )
        result = response.results[0]

        return {
            "allowed": not result.flagged,
            "flagged": result.flagged,
            "error": False,
            "reason": "Listing passed moderation."
            if not result.flagged
            else "Listing was flagged by AI moderation."
        }

    except Exception:
        return {
            "allowed": False,
            "flagged": False,
            "error": True,
            "reason": "Moderation service unavailable. Please try again."
        }
