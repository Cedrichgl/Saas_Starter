import stripe

from app.config import get_settings

settings = get_settings()

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(user_email: str, price_id: str) -> str:
    """
    Crée une session Stripe Checkout et retourne l'URL de paiement.
    """
    session = stripe.checkout.Session.create(
        customer_email=user_email,
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,  # ex: "price_1Nb..."
                "quantity": 1,
            }
        ],
        mode="subscription",
        success_url=settings.STRIPE_SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=settings.STRIPE_CANCEL_URL,
    )

    return session.url


def handle_webhook(payload: bytes, sig_header: str) -> dict:
    # 1. Vérification de la signature
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        # Payload invalide
        raise ValueError("Invalid payload")
    except SignatureVerificationError:
        # Signature invalide → requête non Stripe
        raise SignatureVerificationError("Invalid signature", sig_header)

    # 2. Routing des événements
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        _handle_checkout_completed(session)

    return {"status": "ok"}


def _handle_checkout_completed(session: dict):
    user_email = session.get("customer_email")
    stripe_session_id = session.get("id")
