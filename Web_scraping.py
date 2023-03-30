from bs4 import BeautifulSoup
import requests
import csv
from colorama import Fore, Back, Style

# Open a CSV file for writing
SOURCE_FILE= "rental_properties.csv"
with open(SOURCE_FILE, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price', 'Details', 'Bedrooms', 'Area', 'Location'])

    # Iterate over all pages
    lists =[]
    print(Fore.LIGHTYELLOW_EX +"\nLOADING..")
    print(0, "%",flush=True, end="\r")
    for page_num in range(1,8):
        url = f'https://rentflatpoland.com/advanced-search-2/page/{page_num}/?advanced_city=warsaw&advanced_area&no-rooms&no-bedrooms&min-m2&property-id&keywords&price_low=1000&price_max=25000&sf_paged=2'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        lists += soup.findAll('div', class_="property_listing")
        print(int((page_num/7) *100), "%",flush=True, end="\r")

    # Loop over the rental property listings on this page and write the data to the CSV file
    info=[]
    print(Fore.LIGHTYELLOW_EX +"\n\nWRITING..")
    print(Style.RESET_ALL)
    for listing in lists:
        price = listing.find('div', class_="listing_unit_price_wrapper").text.replace('\n', '')
        details = listing.find('div', class_="listing_details the_list_view").text.replace('\n', '')
        area = listing.find('span', class_="infosize").text.replace('\n', '')
        location = listing.find('div', class_="property_location_image").text.replace('\n', '')
        try:
            bed = listing.find('span', class_="inforoom").text.replace('\n', '')
        except Exception:
            bed = "N/A"
       
        info.append( [price, details,bed, area, location])

   
    writer.writerows(info)

    print(Fore.GREEN+ Back.WHITE+ f" ALL {len(lists)} DATA LINES SAVED INTO A FILE NAMED: [ {SOURCE_FILE} ]",end="")
    print(Style.RESET_ALL)
 