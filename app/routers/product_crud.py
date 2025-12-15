from fastapi import APIRouter
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.validate import csv_check
from app.data_operations import DBOperation, Dataparser

db_operation = DBOperation()
data_parser = Dataparser()

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/upload")
async def upload_products(
    file: UploadFile = File(...)):
    try:
        contenttype=file.content_type
        print(contenttype)
        if not contenttype=="text/csv":
            return JSONResponse(status_code=400,content="The current file type is unsupported, UPLOAD A CSV FILE")
        
        data = await data_parser.parse_csv(file)

        valid,invalid=csv_check(data)
        if not valid:
            return JSONResponse(status_code=400,content={"msg":"no valid data found","errors":invalid})
        db_operation.create(valid)
        
        return JSONResponse(status_code=201,content={"msg": "DATA PARTIALLY INSERTED" if invalid else "DATA INSERTED SUCCESSFULLY",
                                                     "success":len(valid), "failure":len(invalid),                                               
                                                     "errors":invalid})

    except Exception as e:
        raise HTTPException(
            status_code=500,detail=str(e)
        )
        
@router.get("")
def product_get(page:int,limit:int):
    try:
        offset = (page - 1) * limit
        product_data = db_operation.fetch(offset,limit)
        product_list = []
        for p in product_data:
            product_list.append({
                "sku": p.sku,
                "name": p.name,
                "brand": p.brand,
                "color": getattr(p, "color", None),
                "size": getattr(p, "size", None),
                "mrp": p.mrp,
                "price": p.price,
                "quantity": getattr(p, "quantity", None)
            })
        total = db_operation.count()
        pages = (total + limit - 1) // limit
        return JSONResponse(status_code=200,content={"total":total,"pages":pages,"data":product_list})                                          
    except Exception as e:
         raise HTTPException(
            status_code=500,detail=str(e)
        )

@router.get("/search")
def search(brand:str | None = None,
           color:str | None = None,
           minprice:int | None=None,
           maxprice:int | None = None):
    try:
        product_data = db_operation.filter(brand, color, minprice, maxprice)
        product_list = []
        for p in product_data:
            product_list.append({
                "sku": p.sku,
                "name": p.name,
                "brand": p.brand,
                "color": getattr(p, "color", None),
                "size": getattr(p, "size", None),
                "mrp": p.mrp,
                "price": p.price,
                "quantity": getattr(p, "quantity", None)
            })    
        return JSONResponse(status_code=200,content={"data":product_list})
    except Exception as e:
         raise HTTPException(
            status_code=500,detail=str(e)
        )
    


