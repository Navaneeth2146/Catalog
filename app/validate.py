def csv_check(data: list):
    required_fields = ["sku", "name", "brand", "mrp", "price", "quantity"]
    valid_data=[]
    invalid_data = []

    for x in data:
        errors=[]

        missing_fields = [field for field in required_fields if field not in x or str(x[field]).strip() == ""]
        if missing_fields:
            errors.append({
                "type": "missing_fields",
                "fields": missing_fields
            })

        if "price" not in missing_fields:
            try:
                price = float(x.get("price", 0))
                mrp = float(x.get("mrp", 0))

                if price >= mrp:
                    errors.append({
                        "type": "invalid_price",
                        "message": "price must be less than or equal to mrp"
                    })
            except ValueError:
                errors.append({
                    "type": "invalid_price",
                    "message": "price and mrp must be numeric"
                })
        if "quantity" not in missing_fields:
            try:
                quantity = float(x.get("quantity", 0))
                if quantity < 0:
                    errors.append({
                        "type": "invalid_quantity",
                        "message": "quantity must be greater than or equal to 0"
                    })
            except ValueError:
                errors.append({
                    "type": "invalid_quantity",
                    "message": "quantity must be numeric"
                })

        if errors:
            invalid_data.append({
                "row": x,
                "errors": errors
            })
        else:
            valid_data.append(x)

    return valid_data,invalid_data
