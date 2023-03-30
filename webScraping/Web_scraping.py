from bs4 import BeautifulSoup
import requests
import csv
from colorama import Fore, Back, Style

# Open a CSV file for writing
SOURCE_FILE = "rental_properties.csv"
with open(SOURCE_FILE, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price/PLN','Utility Price','Availability', 'Bedrooms', 'Area/m2', 'Location/Warsaw']) # this is the header of the data

    # Iterate over all pages

    print(Fore.LIGHTYELLOW_EX + "\nLOADING..")
    print(0, "%", flush=True, end="\r")

    data_tag = []  # an empty list to store the requested data
    #REQUESTING DATA FROM rentflatpoland WEBSITE
    for page_num in range(1, 8):
        url = f'https://rentflatpoland.com/advanced-search-2/page/{page_num}/?advanced_city=warsaw&advanced_area&no-rooms&no-bedrooms&min-m2&property-id&keywords&price_low=1000&price_max=25000&sf_paged=2'
        page = requests.get(url) # REQUESTING FROM THE SERVER
        soup = BeautifulSoup(page.content, 'html.parser')
        data_tag += soup.findAll('div', class_="property_listing") #storing a certain part of the soup data in the list
        print(int((page_num / 7) * 100), "%", flush=True, end="\r")

    # Loop over the rental property data_tag(property_listing) on this page and write the data to the CSV file
    info = []
    print(Fore.LIGHTYELLOW_EX + "\n\nDONE")
    print(Style.RESET_ALL)
    c=0
    for data in data_tag:
        pricing_data = data.find('div', class_="listing_unit_price_wrapper")
        bills_span = pricing_data.findAll('span')[1]
        bills = pricing_data.findAll('span')[1].text.replace("+", "").strip()
        bills_span.extract()
        if bills in ["", "all in", "per month", "all in with bills included", "a month", "with all bills", "with bills"]:
            bills = "Bills Included"
        else:
            bills = "Bills not included"
        price = pricing_data.text.replace('\n', '').replace("PLN", "").replace(',','').strip()
        try:
            available = data.find('div', class_="ribbon-inside").text.replace('\n', '').replace('Available from ','').strip()
        except Exception:
            available = "N/A"
        area = data.find('span', class_="infosize").text.replace('\n', '').replace(' m2','').strip()
        location = data.find('div', class_="property_location_image").text.replace('\n', '').replace("Warsaw", "").replace(",", "").strip()
        try:
            bed = data.find('span', class_="inforoom").text.replace('\n', '').strip()
        except Exception:
            bed = "N/A"

        info.append([int(price),bills,available, bed, area,location])
        
    sorted_info = sorted(info, key=lambda x: x[0], reverse=True)
    writer.writerows(sorted_info)

    print(Fore.GREEN + Back.WHITE + f" ALL {len(data_tag)} DATA LINES SAVED INTO A FILE NAMED: [ {SOURCE_FILE} ]", end="")
    print(Style.RESET_ALL)