import requests
from agents import Agent, Runner, function_tool
from connection import config

BASE_URL = "https://hackathon-apis.vercel.app/api/products"

@function_tool
def get_all_products():
    """
    Fetch all available products from the shopping API.
    """
    response = requests.get(BASE_URL)
    return response.json()

@function_tool
def get_product_by_id(product_id: str) -> dict:
    """
    Get product details using a specific product ID.
    """
    response = requests.get(f"{BASE_URL}/{product_id}")
    return response.json()

@function_tool
def search_product_by_name(name: str) -> list[dict]:
    """
    Search for products by name.
    """
    response = requests.get(BASE_URL)
    all_products = response.json()
    results = [product for product in all_products if name.lower() in product["name"].lower()]
    return results

@function_tool
def filter_products_by_price(max_price: float) -> list[dict]:
    """
    Return products that cost less than or equal to the given max price.
    """
    response = requests.get(BASE_URL)
    all_products = response.json()
    results = [product for product in all_products if product.get("price", 0) <= max_price]
    return results


agent = Agent(
    name="Shopping Agent",
    instructions=(
        "You are a helpful shopping agent. You can show products, search by name and "
        "filter by price."
    ),
    tools=[
        get_all_products,
        get_product_by_id,
        search_product_by_name,
        filter_products_by_price
    ]
)
response = Runner.run_sync(
    agent,
    input="show me only 5 product with their name,id and $price",
            
    run_config=config
)

print("\033[92m" + response.final_output + "\033[0m")
