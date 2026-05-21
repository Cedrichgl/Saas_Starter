from fastapi import APIRouter, Header, HTTPException, Request

from app.services.stripe import handle_webhook

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/webhook")
async def stripe_webhook(
    request: Request, stripe_signature: str = Header(alias="stripe-signature")
):
    payload = await request.body()

    try:
        return handle_webhook(payload, stripe_signature)
    except (ValueError, Exception):
        raise HTTPException(status_code=400, detail="Webhook error")
