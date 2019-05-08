# -*- coding: utf-8 -*-
from django.shortcuts import render
import requests
import urllib.request
import time
from bs4 import BeautifulSoup


def getData(key):
	url = 'https://www.zalando.fr/homme/?q='+key
	headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
	response = requests.get(url)
	if response.status_code == 200:
		

		soup = BeautifulSoup(response.text, "html.parser")
		
		quotes =[]  # a list to store quotes 
	  
		table = soup.find('z-grid', attrs = {'class':'cat_catArticles-2Pxh7'}) 
		compt = 1
		for row in table.findAll('z-grid-item', attrs = {'class':'cat_articleCard-1r8nF cat_normalWidth-tz8JR'}): 
		    quote = {} 
		    
		    quote['url'] = 'http://127.0.0.1:8000/detail'+row.a['href'].replace('.html', '')
		    quote['img'] = row.img['src'] 
		    quote['id'] = row.a['href'].replace('.html', '')
		    quote['desc'] = row.find('div', attrs = {'class':'cat_articleName--arFp cat_ellipsis-MujnT'}).text 
		    prix = row.find('div', attrs = {'class':'cat_prices-2-Zhx'}).text.split(',')
		    quote['prix'] = prix[0]
		    quote['titre'] = row.find('div', attrs = {'class':'cat_brandName-2XZRz cat_ellipsis-MujnT'}).text
		    
		    quotes.append(quote)

		    compt += 1

		return quotes
	else:
		return quotes


def getDetail(url):
	
	r = requests.get(url)
	c = r.content.decode('utf-8')
	soup = BeautifulSoup(c,"html.parser")

	return soup

	



def home(req):
	
	quotes = getData('chemises')

	return render(req, 'home-page.html', {'liens':quotes})


def detail(req, liens):
	keis = liens
	liens = 'https://www.zalando.fr/'+liens+'.html'

	donnes = getDetail(liens)
	imgc = donnes.find('img',attrs={"id":"galleryImage-0"})
	img = imgc['src']

	titre = donnes.find('h2',attrs={"class":"h-text h-color-black detail h-p-bottom-xs h-bold"}).text
	desc = donnes.find('h1',attrs={"class":"h-text h-color-black title-typo h-clamp-2"}).text
	recprix = donnes.find('div',attrs={"class":"h-text h-color-black title-typo h-p-top-m"}).text.split(',')
	prix = (int(recprix[0]) + 1) * 650 
	return render(req, 'pages/product-page.html', {'key':keis, 'titre':titre, 'desc':desc, 'recprix':prix, 'img':img})


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