from sqlalchemy import Column, Integer, String,VARCHAR,Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    sku= Column(Integer, primary_key=True, index=True)
    name = Column(String)
    brand = Column(VARCHAR)
    color = Column(VARCHAR)
    mrp = Column(Float)
    size = Column(VARCHAR)
    price = Column(Float)
    quantity = Column(Integer)

