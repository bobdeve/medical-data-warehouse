from sqlalchemy.orm import Session
from sqlalchemy import func
from models import FctMessages, FctImageDetections
from schemas import MessageSearch, TopProduct, ChannelActivity

def get_top_products(db: Session, limit: int = 10):
    return db.query(
        FctImageDetections.object_label,
        func.count(FctImageDetections.object_label).label("count")
    ).group_by(
        FctImageDetections.object_label
    ).order_by(
        func.count(FctImageDetections.object_label).desc()
    ).limit(limit).all()

def get_channel_activity(db: Session, channel_id: int):
    result = db.query(
        func.count(FctMessages.message_id),
        func.min(FctMessages.post_date),
        func.max(FctMessages.post_date)
    ).filter(FctMessages.channel_id == channel_id).first()

    if result:
        return {
            "channel_id": channel_id,
            "post_count": result[0],
            "first_post": str(result[1]),
            "last_post": str(result[2])
        }
    return None


def search_messages(db: Session, query: str):
    return db.query(FctMessages).filter(
        FctMessages.message_text.ilike(f"%{query}%")  # ✅ corrected field name
    ).limit(20).all()
