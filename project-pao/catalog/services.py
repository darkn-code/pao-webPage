import os
import requests
import time
import base64
import json

# =========================
# CONFIG
# =========================
API_URL = os.environ.get("API_URL")

# =========================
# TOKEN CACHE
# =========================
TOKEN_CACHE = {
    "token": None,
    "expires_at": 0
}

# =========================
# CATALOG CACHE
# =========================
CATALOG_CACHE = {
    "data": None,
    "expires_at": 0
}


# =========================
# JWT DECODER
# =========================
def decode_jwt(token):
    payload = token.split('.')[1]

    # Fix padding
    padding = '=' * (-len(payload) % 4)
    payload += padding

    decoded = base64.urlsafe_b64decode(payload)
    return json.loads(decoded)


# =========================
# GET TOKEN (CACHEADO)
# =========================
def get_token():
    global TOKEN_CACHE

    now = int(time.time())

    # ✅ Usar token si sigue vigente
    if TOKEN_CACHE["token"] and TOKEN_CACHE["expires_at"] > now:
        return TOKEN_CACHE["token"]

    print("🔄 Renovando token...")

    try:
        response = requests.post(API_URL, json={
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
        })

        data = response.json()
        token = data["data"]["login"]["accessToken"]

        # 🧠 Decodificar expiración
        decoded = decode_jwt(token)
        exp = decoded["exp"]

        TOKEN_CACHE = {
            "token": token,
            "expires_at": exp - 120  # margen de seguridad
        }

        return token

    except Exception as e:
        print("❌ Error obteniendo token:", e)
        return None


# =========================
# GET CATALOG (PAGINADO + CACHE)
# =========================
def get_catalog_all():
    global CATALOG_CACHE

    now = int(time.time())

    # ✅ Usar cache si existe
    if CATALOG_CACHE["data"] and CATALOG_CACHE["expires_at"] > now:
        print("⚡ Usando catálogo cacheado")
        return CATALOG_CACHE["data"]

    print("📦 Descargando catálogo completo...")

    token = get_token()

    if not token:
        return []

    headers = {
        "Authorization": f"Bearer {token}"
    }

    all_products = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        try:
            response = requests.post(API_URL, json={
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
            }, headers=headers)

            result = response.json()

            catalog = result["data"]["distribuitorProductCatalog"]

            total_pages = catalog["totalPages"]

            all_products.extend(catalog["data"])

            print(f"📦 Página {page} de {total_pages}")

            page += 1

        except Exception as e:
            print(f"❌ Error en página {page}:", e)
            break

    # 🔥 Guardar cache (10 minutos)
    CATALOG_CACHE = {
        "data": all_products,
        "expires_at": now + 600
    }

    return all_products


# =========================
# GROUP BY CATEGORY
# =========================
def group_by_category(products):
    categories = {}

    for item in products:
        model = item.get("productModel", {})
        variants = item.get("variants", [])

        if not variants:
            continue

        variant = variants[0]

        category = (
            model.get("filters", {}).get("familyFilterable")
            or "OTROS"
        )

        try:
            price = float(variant["pricing"]["priceMx"][0]["amount"])
        except:
            price = 0

        product = {
            "sku": variant.get("sku"),
            "name": model.get("nameProductModel"),
            "price": price,
            "image": (model.get("media", {}).get("mainImages") or [None])[0],
            "color": variant.get("color"),
        }

        categories.setdefault(category, []).append(product)

    return categories