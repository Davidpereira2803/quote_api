from sqlalchemy import Column, Integer, String
from database import Base

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    text = Column(String, nullable=False)
    author = Column(String, nullable=False)
    category = Column(String, nullable=False)
