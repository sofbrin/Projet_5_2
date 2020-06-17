#! /usr/bin/env python
# coding: utf8

import os

import django
import requests as requests
from django.core.exceptions import ObjectDoesNotExist
from dbsearch import find_or_substitute

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "purbeurre2.settings")
django.setup()

from AppPurbeurre2.models import CategoryDb, ProductDb


def select_categories():
    if CategoryDb.objects.all().count() != 0:
        return
    r_categories = requests.get('https://fr.openfoodfacts.org/categories.json')
    response = r_categories.json()
    categories = response['tags']

    selected_categories = []

    categories = sorted(categories, key=lambda x: x['products'], reverse=True)
    for category in categories:
        try:
            CategoryDb.objects.get(url=category['url'])
        except ObjectDoesNotExist:
            selected_categories.append(category)
            save_categories_in_db(category)
            print('\nLa catégorie "' + category['name'] + '" vient d\'être ajoutée dans la base de données')
            select_products(category)
            if len(selected_categories) == 20:
                break


def select_products(category):
    selected_products = []
    page = 1

    while len(selected_products) < 20:
        r_products = requests.get(category['url'] + '/{}.json'.format(page))
        response = r_products.json()
        products = response['products']

        for product in products:
            try:
                ProductDb.objects.get(url=product['url'])
            except ObjectDoesNotExist:
                if 'product_name' in product and product['product_name'] != '' \
                        and 'brands' in product and product['brands'] != '' \
                        and 'origins' in product and product['origins'] != '' \
                        and 'manufacturing_places' in product and product['manufacturing_places'] != '' \
                        and 'countries' in product and product['countries'] != '' \
                        and 'stores' in product and product['stores'] != '' \
                        and 'nutrition_grades' in product and product['nutrition_grades'] != ''\
                        and 'url' in product and product['url'] != '':
                    selected_products.append(product)
                    save_products_in_db(product, category)
                    print('Le produit "' + product['product_name'] + '" vient d\'être ajouté dans cette catégorie.')
                if len(selected_products) == 20:
                    break
        page += 1


def save_categories_in_db(category):
    category_db = CategoryDb(url=category['url'], name=category['name'])
    category_db.save()


def save_products_in_db(product, category):
    category_db = CategoryDb.objects.get(url=category['url'])

    product_db = ProductDb(name=product['product_name'].encode(encoding='UTF-8'), category=category_db,
                           brand=product['brands'].encode(encoding='UTF-8'),
                           origin=product['origins'].encode(encoding='UTF-8'),
                           manufacturing_places=product['manufacturing_places'].encode(encoding='UTF-8'),
                           countries=product['countries'], store=product['stores'].encode(encoding='UTF-8'),
                           nutriscore=product['nutrition_grades'],
                           url=product['url'].encode(encoding='UTF-8'))
    product_db.save()


if __name__ == '__main__':
    select_categories()
    find_or_substitute()
