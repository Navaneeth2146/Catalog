import pytest
import aiofiles
from app.data_operations import Dataparser, DBOperation
from pathlib import Path

@pytest.mark.asyncio
async def test_parse_csv_real_file():
    csv_path = Path("tests/test_products.csv")
    async with aiofiles.open(csv_path, "rb") as file:
        parser = Dataparser()
        result = await parser.parse_csv(file)
    file.close()

    assert len(result) == 2

def test_search_by_brand():
    db_op = DBOperation()
    results = db_op.filter(brand="CarryAll")

    assert len(results) > 0
    for product in results:
        assert product.brand.lower() == "carryall"

def test_search_by_color():
    db_op = DBOperation()
    results = db_op.filter(color="Red")

    assert len(results) > 0
    for product in results:
        assert product.color.lower() == "red"

def test_search_by_price_range():
    db_op = DBOperation()
    results = db_op.filter(minPrice=500, maxPrice=1300)

    assert len(results) > 0
    for product in results:
        assert 500 <= product.price <= 1300
