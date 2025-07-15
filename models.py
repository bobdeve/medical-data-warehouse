from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FctMessages(Base):
    __tablename__ = "fct_messages"

    message_id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String, index=True)
    post_text = Column(String)
    post_date = Column(Date)
    channel_id = Column(Integer)  # ✅ Make sure this is added

class FctImageDetections(Base):
    __tablename__ = "fct_image_detections"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("fct_messages.message_id"))
    object_class = Column(String)
    object_label = Column(String)
    confidence_score = Column(Float)
