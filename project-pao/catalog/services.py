import os
import requests

API_URL = os.environ.get("API_URL")

def get_token():
    payload = {
        "query": """
        mutation Login($email: String!, $password: String!) {
            login(email: $email, password: $password) {
                accessToken
            }
        }
        """,
        "variables": {
            "email": os.environ.get("API_EMAIL"),
            "password": os.environ.get("API_PASSWORD")
        }
    }

    response = requests.post(API_URL, json=payload)
    return response.json()["data"]["login"]["accessToken"]

def get_catalog_all():
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    all_products = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        payload = {
            "query": """
            query GetDistribuitorCatalog($page: Int!) {
                distribuitorProductCatalog(page: $page) {
                    currentPage
                    totalPages
                    data {
                        productModel {
                            nameProductModel
                            media { mainImages }
                            filters {
                                familyFilterable
                                subFamilyFilterable
                            }
                        }
                        variants {
                            sku
                            color
                            pricing { priceMx { amount } }
                        }
                    }
                }
            }
            """,
            "variables": {"page": page}
        }

        response = requests.post(API_URL, json=payload, headers=headers)
        result = response.json()

        catalog = result["data"]["distribuitorProductCatalog"]

        total_pages = catalog["totalPages"]

        all_products.extend(catalog["data"])

        print(f"📦 Página {page} de {total_pages}")

        page += 1

    return all_products

def group_by_category(products):
    categories = {}

    for item in products:
        model = item["productModel"]
        variant = item["variants"][0]

        category = model["filters"]["familyFilterable"] or "OTROS"

        product = {
            "sku": variant["sku"],
            "name": model["nameProductModel"],
            "price": float(variant["pricing"]["priceMx"][0]["amount"]),
            "image": model["media"]["mainImages"][0] if model["media"]["mainImages"] else None,
            "color": variant["color"],
        }

        categories.setdefault(category, []).append(product)

    return categories