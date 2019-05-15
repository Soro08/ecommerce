# -*- coding: utf-8 -*-
from django.shortcuts import render

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import random

from scraper.models import Recherche
from scraper.models import Articles

def saveArticle(a_desc,a_titre,aprix,acouleur,tail,a_id,key, url, aimg):

	try:
		is_article = Articles.objects.get(aliens=a_id)
	except Articles.DoesNotExist:
		is_article = 0

	if is_article != 0:
		
		# Modifier
		is_article.emarque = a_desc
		is_article.adescription = a_titre
		is_article.aprix = aprix
		is_article.acouleur = 'Red Black'
		is_article.atail = '30 35 38'
		is_article.aliens=a_id
		is_article.acles=key 
		is_article.asource=url
		is_article.aimg=aimg
		# Enregistrer
		is_article.save()

	else:

		# Ajouter
		articles = Articles(emarque=a_desc,adescription=a_titre,aprix=aprix,acouleur='Bleu Red',atail='M XL',aliens=a_id,acles=key, asource=url, aimg=aimg)
		# Enregistrer
		articles.save()


def getData(key):
	url = 'https://www.zalando.fr/homme/?q='+key+'&p=94'
	headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		
		soup = BeautifulSoup(response.text, "html.parser")
		
		quotes =[]  # a list to store quotes 
		try:

			table = soup.find('z-grid', attrs = {'class':'cat_catArticles-2Pxh7'}) 
			compt = 1
			for row in table.findAll('z-grid-item', attrs = {'class':'cat_articleCard-1r8nF cat_normalWidth-tz8JR'}): 
				quote = {} 
				
				a_url = 'http://127.0.0.1:8000/detail'+row.a['href'].replace('.html', '')
				quote['url'] = a_url
					
				a_img = row.img['src'] 
				quote['img'] = a_img

				a_id = row.a['href'].replace('.html', '')
				quote['id'] = a_id

				a_desc = row.find('div', attrs = {'class':'cat_articleName--arFp cat_ellipsis-MujnT'}).get_text() 
				quote['desc'] = a_desc


				prix = row.find('div', attrs = {'class':'cat_prices-2-Zhx'}).text.split(',')
				

				a_titre = row.find('div', attrs = {'class':'cat_brandName-2XZRz cat_ellipsis-MujnT'}).text
				quote['titre'] = a_titre
				
				if prix[0].isdigit() :
					quote['prix'] = nanPrix(prix[0])
					quotes.append(quote)
					saveArticle(a_desc,a_titre,nanPrix(prix[0]),'Bleu Red','M XL',a_id,key,url,a_img) 
					
				compt += 1

			recherche = Recherche(rmot=key, rsite='https://www.zalando.fr/homme/')
			recherche.save()
			return quotes
		except:
			all_articles = Articles.objects.filter(acles__contains=key)
			for articles in all_articles:

				quote = {} 
				quote['prix'] = articles.aprix
				quote['url'] = articles.aliens
				quote['img'] = articles.aimg
				quote['id'] = articles.aliens
				quote['desc'] = articles.emarque
				quote['titre'] = articles.adescription
				quotes.append(quote)

			recherche = Recherche(rmot=key, rsite='https://www.zalando.fr/homme/')
			recherche.save()
			return quotes

	else:

		return quotes


def getDetail(url):
	
	r = requests.get(url)
	c = r.content.decode('utf-8')
	soup = BeautifulSoup(c,"html.parser")

	return soup

	



def home(req):
	mot = 'chemises'
	foo = ['Sneakers', 'Chemises', 'Costumes', 'Skate shoes', 'Derbies & Richelieu', 'Baskets']
	motchoix = random.choice(foo)
	quotes = getData(motchoix)
	return render(req, 'home-page.html', {'liens':quotes})


def detail(req, liens):
	keis = liens
	quote = []
	liens = 'https://www.zalando.fr/'+liens+'.html'
	try:

		donnes = getDetail(liens)
		imgc = donnes.find('img',attrs={"id":"galleryImage-0"})
		img = imgc['src']

		titre = donnes.find('h2',attrs={"class":"h-text h-color-black detail h-p-bottom-xs h-bold"}).text
		desc = donnes.find('h1',attrs={"class":"h-text h-color-black title-typo h-clamp-2"}).text
		recprix = donnes.find('div',attrs={"class":"h-text h-color-black title-typo h-p-top-m"}).text.split(',')
		prix = (int(recprix[0]) + 1) * 650 

		quote = {} 
		quote['recprix'] = prix
		quote['url'] = liens
		quote['img'] = img
		quote['key'] = keis
		quote['desc'] = desc
		quote['titre'] = titre
		quotes.append(quote)

	except:
		try:
			articles = Articles.objects.get(aliens=keis)
			quote = {}
			quote['url'] = articles.aliens
			quote['recprix'] = articles.aprix
			quote['img'] = articles.aimg
			quote['key'] = articles.aliens
			quote['desc'] = articles.emarque
			quote['titre'] = articles.adescription
			quotes.append(quote)
		except Articles.DoesNotExist:
			quote = {}
	return render(req, 'pages/product-page.html', {'detail':quotes})
	
def checkout(req):
	return render(req, 'pages/checkout-page.html')



def result(req):

	q  = req.GET.get('q')
	if (q):
		message = getData(q)
	else:
		message = 'costumes'

	
	return render(req, 'pages/result-page.html', {'resultats':message})




def about(req):
	return render(req, 'pages/about.html')


def contact(req):
	return render(req, 'pages/contact.html')


def nanPrix(prix_euro):
	taux = 50
	pct = 100
	apli_taux = 1

	taux_cfa = 656

	montaux = apli_taux + (taux/pct)

	prix_fin = (prix_euro * taux_cfa) * montaux

	return prix_fin