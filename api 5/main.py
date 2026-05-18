from fastapi import FastAPI, Query

app = FastAPI()

# ---------------- SAMPLE DATA ----------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = []

# ---------------- ORDERS POST (for testing Q4/Q6 bonus) ----------------
@app.post("/orders")
def create_order(customer_name: str, product_id: int):
    order = {
        "order_id": len(orders) + 1,
        "customer_name": customer_name,
        "product_id": product_id
    }
    orders.append(order)
    return order


# ---------------- Q1: SEARCH PRODUCTS ----------------
@app.get("/products/search")
def search_products(keyword: str):
    result = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {"total_found": len(result), "products": result}


# ---------------- Q2: SORT PRODUCTS ----------------
@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = (order == "desc")

    result = sorted(products, key=lambda p: p[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": result
    }


# ---------------- Q3: PAGINATION ----------------
@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    start = (page - 1) * limit
    end = start + limit

    total_pages = -(-len(products) // limit)

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": products[start:end]
    }


# ---------------- Q4: ORDER SEARCH ----------------
@app.get("/orders/search")
def search_orders(customer_name: str):

    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }


# ---------------- Q5: SORT BY CATEGORY THEN PRICE ----------------
@app.get("/products/sort-by-category")
def sort_by_category():

    result = sorted(products, key=lambda p: (p["category"], p["price"]))

    return {
        "products": result,
        "total": len(result)
    }


# ---------------- Q6: BROWSE (SEARCH + SORT + PAGINATION) ----------------
@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):

    result = products

    # 1. SEARCH
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # 2. SORT
    if sort_by in ["price", "name"]:
        reverse = (order == "desc")
        result = sorted(result, key=lambda p: p[sort_by], reverse=reverse)

    # 3. PAGINATION
    total = len(result)
    start = (page - 1) * limit
    end = start + limit

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": result[start:end]
    }