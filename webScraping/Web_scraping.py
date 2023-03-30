from bs4 import BeautifulSoup
import requests
import csv
from colorama import Fore, Back, Style

# Open a CSV file for writing
SOURCE_FILE = "rental_properties.csv"
with open(SOURCE_FILE, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price/PLN','Utility Price','Availability', 'Bedrooms', 'Area/m2', 'Location']) # this is the header of the data

    # Iterate over all pages

    print(Fore.LIGHTYELLOW_EX + "\nLOADING..")
    print(0, "%", flush=True, end="\r")

    data_tag = []  # an empty list to store the requested data
    # REQUESTING DATA FROM rentflatpoland WEBSITE
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
    for data in data_tag:
        pricing_data = data.find('div', class_="listing_unit_price_wrapper")
        bills_span = pricing_data.findAll('span')[1]
        bills = pricing_data.findAll('span')[1].text.replace("+", "").strip()
        bills_span.extract()
        price = pricing_data.text.strip().replace('\n', '').replace("PLN", "").replace(',','')
        try:
            available = data.find('div', class_="ribbon-inside").text.replace('\n', '').replace('Available from ','')
        except Exception:
            available = "N/A"
        #details = data.find('div', class_="listing_details the_list_view").text.replace('\n', '')
        area = data.find('span', class_="infosize").text.replace('\n', '').replace(' m2','')
        location = data.find('div', class_="property_location_image").text.replace('\n', '')
        try:
            bed = data.find('span', class_="inforoom").text.replace('\n', '')
        except Exception:
            bed = "N/A"

        info.append([price,bills,available, bed, area,location])

    writer.writerows(info)

    print(Fore.GREEN + Back.WHITE + f" ALL {len(data_tag)} DATA LINES SAVED INTO A FILE NAMED: [ {SOURCE_FILE} ]", end="")
    print(Style.RESET_ALL)