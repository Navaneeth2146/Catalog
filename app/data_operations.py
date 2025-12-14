from sqlalchemy.orm import Session
from sqlalchemy import func
import app.models as models
from app.database import SessionLocal,Base,engine
import io,csv

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
db: Session = SessionLocal()

class DBOperation:
    def __init__(self):
        self.product =  models.Product

    def create(self, data):
        try:
            for pro in data:
                Product = self.product(**pro)
                db.add(Product)
                db.commit()
            return "success"
        except Exception as e:
            db.rollback()
            raise e

    def fetch(self, offset, limit):
        product_data = (
            db.query(self.product)
            .offset(offset)
            .limit(limit)
            .all()
        )    
        db.close()

        return product_data

    def count(self):
        Total = db.query(self.product).count()
        return Total
    
    def filter(self,
        brand: str | None = None,
        color: str | None = None,
        minPrice: float | None = None,
        maxPrice: float | None = None
        ):
        product=self.product

        query = db.query(product)

        if brand:
            query = query.filter(func.lower(product.brand) == brand.lower())
        elif color:
            query = query.filter(func.lower(product.color) == color.lower())
        elif minPrice is not None or maxPrice is not None:
            if minPrice is not None:
                query = query.filter(product.price >= minPrice)
            if maxPrice is not None:
                query = query.filter(product.price <= maxPrice)

        return query.all()

class Dataparser:
    async def parse_csv(self,file):
        content =await file.read()
        text = content.decode('utf-8')
        reader = csv.DictReader(io.StringIO(text))
        data = list(reader)
        return data 
