import pytest
from app.validate import csv_check


#check valid row
def test_csv_check_valid_row():
    data = [{
        "sku": "Dat1",
        "name": "Shirt",
        "brand": "BrandA",
        "color": "red",        
        "size":"s",
        "mrp": "150",
        "price": "100",
        "quantity": "10"
    }]

    valid, invalid = csv_check(data)

    assert len(valid) == 1
    assert len(invalid) == 0

#check missing field
def test_csv_check_missing_fields():
    data = [{
        "sku": "",
        "name": "",
        "brand": "BrandA",
        "color": "red",
        "size":"s",
        "mrp": "150",
        "price": "100",
        "quantity": "10"
    }]

    valid, invalid = csv_check(data)

    assert len(valid) == 0
    assert len(invalid) == 1
    assert invalid[0]["errors"][0]["type"] == "missing_fields"

#check invalid quantity
def test_csv_check_negative_quantity():
    data = [{
        "sku": "Dat1",
        "name": "Shirt",
        "brand": "BrandA",
        "color": "red",
        "size":"s",
        "mrp": "150",
        "price": "100",
        "quantity": "-1"
    }]

    valid, invalid = csv_check(data)

    assert len(valid) == 0
    assert invalid[0]["errors"][0]["type"] == "invalid_quantity"
