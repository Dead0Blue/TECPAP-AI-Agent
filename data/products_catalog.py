"""
Catalogue des produits TECPAP
"""

PRODUCTS_CATALOG = [
    {"code": "P001", "name": "Fond plat", "type": "Fond_Plat", "description": "Sac papier standard à fond plat"},
    {"code": "P002", "name": "Fond carré sans poignées", "type": "Fond_Carre_Sans_Poignees", "description": "Sac papier à fond carré, sans poignées"},
    {"code": "P003", "name": "Fond carré poignées plates", "type": "Fond_Carre_Poignees_Plates", "description": "Sac papier à fond carré avec poignées plates"},
    {"code": "P004", "name": "Fond carré poignées torsadées", "type": "Fond_Carre_Poignees_Torsadees", "description": "Sac papier à fond carré avec poignées torsadées"}
]

def get_all_products():
    return PRODUCTS_CATALOG

def get_product_by_code(code):
    for p in PRODUCTS_CATALOG:
        if p["code"] == code: return p
    return None
