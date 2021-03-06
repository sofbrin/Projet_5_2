#! /usr/bin/env python
# coding: utf8

import os
import sys

import django
from django.core.paginator import Paginator

from constants import App_Title, App_Intro, App_Home_Menu, App_Categories_Menu, App_Products_Menu, \
    App_Selected_Product_Menu, App_Suggested_Product_Menu, App_Save_Substitute_Menu, \
    App_DB_Menu, App_DB_Cat_Menu, end_of_App

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "purbeurre2.settings")
django.setup()

from AppPurbeurre2.models import CategoryDb, ProductDb, HistoricDb


def find_or_substitute():
    print(App_Title)
    print(App_Intro)

    while True:
        input_user = input(App_Home_Menu)

        if input_user == '1':
            select_a_category()
        elif input_user == '2':
            substitutes()
        elif input_user == '3':
            print(end_of_App)
            sys.exit()


def select_a_category():

    categories_db = CategoryDb.objects.all().order_by('id')
    p = Paginator(categories_db, 10)
    page_number = 1
    page = p.page(page_number)

    while True:
        for idx, category in enumerate(page.object_list):
            print(idx+1, category.name)

        input_user = input(App_Categories_Menu)

        if input_user == '0':
            return

        elif input_user == 's' and page.has_next():
            page = p.page(page_number+1)
            page_number += 1

        elif input_user == 'p' and page.has_previous():
            page = p.page(page_number-1)
            page_number -= 1

        else:
            try:
                selection = int(input_user)
                if len(page.object_list) >= selection >= 1:
                    select_a_product(page.object_list[selection-1])
            except ValueError:
                continue


def select_a_product(category):

    products_db = ProductDb.objects.filter(category=category).order_by('id')
    p = Paginator(products_db, 10)
    page_number = 1
    page = p.page(page_number)

    while True:
        for idx, product in enumerate(page.object_list):
            print(idx+1, product.name)

        input_user = input(App_Products_Menu)

        if input_user == '0':
            return

        elif input_user == 's' and page.has_next():
            page = p.page(page_number + 1)
            page_number += 1

        elif input_user == 'p' and page.has_previous():
            page = p.page(page_number - 1)
            page_number -= 1

        else:
            try:
                selection = int(input_user)
                if len(page.object_list) >= selection >= 1:
                    display_product(page.object_list[selection-1])
            except ValueError:
                continue


def display_product(product):

    while True:
        input_user = input(App_Selected_Product_Menu)

        if input_user == '1':
            display_product_characteristics(product)

        elif input_user == '2':
            if product.nutriscore == 'a':
                print('\nNous ne pouvons pas vous proposer un substitut de meilleure qualité pour ce produit '
                      'car son indice nutriscore est "A". Veuillez choisir un autre produit à substituter.\n')
                select_a_product(product)
            else:
                suggest_substitutes(product)

        elif input_user == '0':
            return
        else:
            continue


def suggest_substitutes(product):

    print(App_Suggested_Product_Menu)

    substitutes = ProductDb.objects.filter(category=product.category, nutriscore__lt=product.nutriscore).order_by('id')
    p = Paginator(substitutes, 5)
    page_number = 1
    page = p.page(page_number)

    while True:
        for idx, substitute in enumerate(page.object_list):
            print(idx+1, substitute.name)

        input_user = input(App_Products_Menu)

        if input_user == '0':
            return

        elif input_user == 's' and page.has_next():
            page = p.page(page_number + 1)
            page_number += 1

        elif input_user == 'p' and page.has_previous():
            page = p.page(page_number - 1)
            page_number -= 1

        else:
            try:
                selection = int(input_user)
                if len(page.object_list) >= selection >= 1:
                    display_substitute(page.object_list[selection-1], product)
            except ValueError:
                continue


def display_substitute(substitute, product):

    display_product_characteristics(substitute)

    while True:
        input_user = input(App_Save_Substitute_Menu)
        if input_user == '1':
            save_substitutes_in_db(substitute, product)
        elif input_user == '2':
            return
        elif input_user == '0':
            find_or_substitute()
        else:
            continue


def save_substitutes_in_db(substitute, product):

    historic_db = HistoricDb(product_replaceable=substitute, product_original=product)
    historic_db.save()

    print('Le produit ' + product.name + ' et le substitut ' + substitute.name +
          ' ont bien été enregistrés dans votre historique de substitution.')


def display_product_characteristics(product):

    print('\nVoici les caractéristiques du produit ', product.name, '\n')
    print('Catégorie            : ', product.category)
    print('Marque               : ', product.brand)
    print('Origine              : ', product.origin)
    print('Lieux de fabrication : ', product.manufacturing_places)
    print('Pays                 : ', product.countries)
    print('Magasins             : ', product.store)
    print('Indice Nutriscore    : ', product.nutriscore.upper())
    print('\nLIEN vers la fiche du produit ' + product.name + ' sur OpenFoodFacts : ' + product.url, '\n')


def substitutes():

    while True:

        input_user = input(App_DB_Menu)

        if input_user == '1':
            search_by_categories()

        else:
            try:
                if input_user == '0':
                    return
            except ValueError:
                continue


def search_by_categories():

    categories_db = CategoryDb.objects.all().order_by('id')
    p = Paginator(categories_db, 10)
    page_number = 1
    page = p.page(page_number)

    while True:
        for idx, category in enumerate(page.object_list):
            print(idx+1, category.name)

        input_user = input(App_DB_Cat_Menu)

        if input_user == '0':
            return

        elif input_user == 's' and page.has_next():
            page = p.page(page_number+1)
            page_number += 1

        elif input_user == 'p' and page.has_previous():
            page = p.page(page_number-1)
            page_number -= 1

        else:
            try:
                selection = int(input_user)
                if len(page.object_list) >= selection >= 1:
                    show_historic_substitution(page.object_list[selection-1])
            except ValueError:
                continue


def show_historic_substitution(category):

    print('Voici l\'historique de la catégorie :', category, '\n')

    products_db = HistoricDb.objects.filter(product_original__category=category).order_by('id')
    p = Paginator(products_db, 5)
    page_number = 1
    page = p.page(page_number)
    page_ids = []

    while True:
        for product in page.object_list:
            print('Produit n°', product.product_original.id, ':', product.product_original,
                  '; Substitut n°', product.product_replaceable.id, ':', product.product_replaceable)
            page_ids.append(product.product_original.id)
            page_ids.append(product.product_replaceable.id)

        input_user = input(App_Products_Menu)

        if input_user == '0':
            return

        elif input_user == 's' and page.has_next():
            page = p.page(page_number + 1)
            page_number += 1

        elif input_user == 'p' and page.has_previous():
            page = p.page(page_number - 1)
            page_number -= 1

        else:
            try:
                selection = int(input_user)
                if selection in page_ids:
                    display_product_characteristics(ProductDb.objects.get(id=selection))
            except ValueError:
                continue
