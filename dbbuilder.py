#! /usr/bin/env python
# coding: utf8

import os

import django
import requests as requests
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "purbeurre2.settings")
django.setup()

from AppPurbeurre2.models import CategoryDb, ProductDb


def select_categories():
    r_categories = requests.get('https://fr.openfoodfacts.org/categories.json')
    response = r_categories.json()
    categories = response['tags']

    selected_categories = []

    categories = sorted(categories, key=lambda x: x['products'], reverse=True)
    for category in categories:
        selected_categories.append(category)
        save_categories_in_db(category)
        print('\nLa catégorie "' + category['name'] + '" vient d\'être ajoutée dans la base de données')
        select_products(category)
        if len(selected_categories) == 5:
            break


def select_products(category):
    selected_products = []
    page = 1

    while len(selected_products) < 5:
        r_products = requests.get(category['url'] + '/{}.json'.format(page))
        response = r_products.json()
        products = response['products']

        for product in products:
            if 'product_name' in product and product['product_name'] != '' and product['product_name'] != 'inconnue' \
                    and 'brands' in product and product['brands'] != '' and product['brands'] != 'inconnue' \
                    and 'origins' in product and product['origins'] != '' and product['origins'] != 'inconnue' \
                    and 'manufacturing_places' in product and product['manufacturing_places'] != '' \
                    and product['manufacturing_places'] != 'inconnue' \
                    and 'countries' in product and product['countries'] != '' and product['countries'] != 'inconnue' \
                    and 'stores' in product and product['stores'] != '' and product['stores'] != 'inconnue' \
                    and 'nutrition_grades' in product and product['nutrition_grades'] != '' \
                    and product['nutrition_grades'] != 'inconnue':
                selected_products.append(product)
                save_products_in_db(product, category)
                print('Le produit "' + product['product_name'] + '" vient d\'être ajouté dans cette catégorie.')
            if len(selected_products) == 5:
                break
        page += 1


def save_categories_in_db(category):
    category_db = CategoryDb(name=category['name'])
    category_db.save()
    """try:
        category_db = CategoryDb.objects.get(name=category['name'])
    except ObjectDoesNotExist:
        category_db = CategoryDb(name=category['name'])
        category_db.save()"""

def save_products_in_db(product, category):
    category_db = CategoryDb.objects.get(name=category['name'])

    product_db = ProductDb(name=product['product_name'], category=category_db, brand=product['brands'],
                           origin=product['origins'], manufacturing_places=product['manufacturing_places'],
                           countries=product['countries'], store=product['stores'],
                           nutriscore=product['nutrition_grades'], url=product['url'])
    product_db.save()


if __name__ == '__main__':
    select_categories()
