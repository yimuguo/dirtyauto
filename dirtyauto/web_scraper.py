import bs4
import numpy as np
import pandas as pd
from urllib.request import urlopen as uReq
import requests
from bs4 import BeautifulSoup as soup
import csv



class DigikeyPartInfo(object):
    def __init__(self, partn):
        """
        :param part_list: list of the part numbers
        """
        self.partn = partn
        self.soup = self.get_soup(self.partn)

    def getSoup(self, part_num):
        """
        gets the soup of a part number as if
        searched directly on digikey
        """
        url_pt_1 = "https://www.digikey.com/products/en?keywords="
        my_url = url_pt_1 + part_num
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")

        return page_soup

    def getSoup_2(self, my_url):
        """
        given a url, this function gets the soup of that webpage
        """
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")

        return page_soup

    # opening up connection, grabbing the page
    def parse_pricing_table(self, soup):
        """
        goes through the pricing table and extracts the
        price breaks and unit prices
        """
        p_break_table = []
        p_table = []
        if soup.find('table', id='product-dollars'):       # if a price table is found
            tbl = soup.find('table', id='product-dollars')
            rows = tbl.find_all('tr')   # find all of the table rows
            for row in range(1, len(rows)):
                cols = rows[row].find_all('td') # finds all of the table data
                price_break = str(cols[0].text)
                price_break = price_break.strip()

                unit_price = str(cols[1].text)
                unit_price = unit_price.strip()

                prince_b = price_break.replace(',', '')
                unit_p = unit_price.replace(',', '')

                p_b_row = int(prince_b)
                p_row = float(unit_p)
                p_table.append(p_row)
                p_break_table.append(p_b_row)
            return p_break_table, p_table  # returns price breaks and unit prices
        else:
            return "No Price", "Obsolete"   # if no price table is found then return No Price, Obsolete

    def parse_mpn(self, soup):
        """
        parse manufacturer part number to dict:info
        """
        mpn = soup.find('h1', {"itemprop": "model"}).text
        mpn = ''.join(mpn.split())
        return mpn

    def parse_qty(self, soup):
        """
        parse available quantity to dict:info
        """
        if soup.find('span', id='dkQty'):
            qty = soup.find('span', id='dkQty').text
        else:
            qty = 0
        return qty

    def parse_manufacturer(self, soup):
        """
        parse current manufacturer to dict:info
        """
        manu = soup.find('span', {"itemprop": "name"}).text
        return manu

    def get_productlnk_from_productTable(self, soup):
        """
        :return: return list with product links from product search table
        """
        links = []
        row_soup = soup.find_all('td', {"class": "tr-mfgPartNumber"})
        for item in row_soup:
            int_lnk = item.find('a').get('href')
            links.append("https://www.digikey.com" + int_lnk)
        return links

    def parse_prod_attr(self, soup):
        """
        goes through the product attribute table and extracts the part status
        and packaging of the part
        """
        table = soup.find('table', id='prod-att-table')

        rows = table.find_all('tr') # find all table rows

        table_headers = []
        table_data = []
        for tr in range(0, len(rows)):
            if rows[tr].find('th'): # in all the rows find all table headers
                header = rows[tr].find('th')
                r = header.text
                table_headers.append(r.strip()) # add this header into a list

                if rows[tr].find('td'): # if we found a header in that row, then find the table data in that row
                    data = rows[tr].find('td')
                    d = data.text
                    table_data.append(d.strip()) # 

        pk_value = "-"

        if "Packaging" in table_headers:
            location = table_headers.index("Packaging")
            pk_value = table_data[location]

        part_status_location = table_headers.index("Part Status")
        ps_value = table_data[part_status_location]

        return ps_value, pk_value

    def _find_product_link(self, soup_, searchtxt):
        if soup_.find('a', href=True, text=searchtxt):
            tree_lnk = soup_.find(
                'a', href=True, text=searchtxt)
            product_table_lnk = "https://www.digikey.com" + \
                                tree_lnk.get('href')

            _page = requests.get(product_table_lnk)
            soup_ = soup(_page.content, 'html.parser')
            return True, product_table_lnk
        else:
            return False

    def get_product_link(self, soup_, searchtxt):
        if soup_.find('a', href=True, text=searchtxt):
            tree_lnk = soup_.find(
                'a', href=True, text=searchtxt)
            product_table_lnk = "https://www.digikey.com" + \
                                tree_lnk.get('href')

            return product_table_lnk

    partn = "error"

    def page_type(self, soup):
        """
        :return: return string with type
        """
        if soup.find('table', id="productTable"):
            return "productTable"
        elif soup.find('table', id='product-dollars'):
            return "productPage"
        elif 'No Results Found | DigiKey Electronics' in soup.title.string:
            return "No Results"
        elif self._find_product_link(soup, 'Clock/Timing - Clock Generators, PLLs, Frequency Synthesizers'):
            return "searchPage", self._find_product_link(soup,
                                                    'Clock/Timing - Clock Generators, PLLs, Frequency Synthesizers')
        elif self._find_product_link(soup, 'Clock/Timing - Clock Buffers, Drivers'):
            return "searchPage", self._find_product_link(soup, 'Clock/Timing - Clock Buffers, Drivers')
        elif self._find_product_link(soup, 'Programmable Oscillators'):
            return "searchPage", self._find_product_link(soup, 'Programmable Oscillators')




class MultiPartDigikey(DigikeyPartInfo):
    """
    Processing multiple parts
    """

    def __init__(self, csv_filepath):
        self._part_list = None
        self.csv_filepath = csv_filepath

    def get_Relevant_Info(self, soup, part):
        """
        given a soup and the part, this function retrieves all the info that would populate
        one row in the output CSV file
        """
        row_content = []
        price_headers_content = []
        row_headers = ["Root (Input) Number", 'Part Number', 'Manufacturer', "Quantity", "Part Status", "Packaging"]

        row_content.append(part)
        row_content.append(self.parse_mpn(soup))
        row_content.append(self.parse_manufacturer(soup))
        row_content.append(self.parse_qty(soup))
        row_content.append(self.parse_prod_attr(soup)[0])
        row_content.append(self.parse_prod_attr(soup)[1])
        if self.parse_pricing_table(soup)[0] != "No Price":
            price_headers_content.append(self.parse_pricing_table(soup)[0])
            prices = self.parse_pricing_table(soup)[1]
            for value in prices:
                row_content.append(value)

            for price_break in price_headers_content[0]:
                row_headers.append(price_break)

        row_data = []
        row_data.append(row_content)
        row_df = pd.DataFrame(data=row_data)

        row_df.columns = row_headers

        return row_df


    def get_part_names_from_csv(self):
        """
        This function goes through a CSV column, assuming that the part names are
        in the first column, of the file, and collects them into a list to be used
        by the scraper
        """
        parts = []
        with open(self.csv_filepath, 'r') as f:  # opens up the csv file
            reader = csv.reader(f)

            for row in reader:
                parts.append(row[0])

        del parts[0] # deletes first element because this is usually the column header,
                     # and not an actual part number

        return parts




    def get_dataframes(self, parts):
        """
        Given a list of parts, this function returns a list of dataframes, with
        each dataframe
        """
        data_frames = []
        for part in parts:
            prt = str(part)
            soup_t = self.getSoup(part)

            page_typ = self.page_type(soup_t)

            # depending on which of the page types a part search falls under, the appropriate steps are taken
            # to collect all the necessary information about the part
            if page_typ == "productPage":
                row = self.get_Relevant_Info(soup_t, prt)
                data_frames.append(row)
            elif page_typ == "productTable":
                lnk = self.get_productlnk_from_productTable(soup_t)
                for part in lnk:
                    s_soup_t = self.getSoup_2(part)
                    row = self.get_Relevant_Info(s_soup_t, prt)
                    data_frames.append(row)

            elif page_typ[0] == "searchPage":
                # print("option 2")
                lnk = page_typ[1][1]
                s_soup = self.getSoup_2(lnk)
                lnks_2 = self.get_productlnk_from_productTable(s_soup)
                for part in lnks_2:
                    s_soup_t = self.getSoup_2(part)
                    # print(qty_list)
                    row = self.get_Relevant_Info(s_soup_t, prt)
                    data_frames.append(row)
            elif page_typ == "No Results":
                activity = [[part, "Inactive (Not on Digi-Key)"]]
                inactive_df = pd.DataFrame(data=activity, columns=["Root (Input) Number", "Part Status"])
                data_frames.append(inactive_df)

        return data_frames



    def dataframes_to_csv(self, data_frames):
        """
        Given a list of dataframes, this function appends them all into one dataframe,
        rearranges it into a desirable orientation, and creates the output CSV file
        """
        part_table_df = pd.DataFrame(data_frames[0])

        for i in range(0, len(data_frames)):
            part_table_df = part_table_df.append(data_frames[i])

        new_column_list = []
        column_list = list(part_table_df)
        re_ordering_cols = ["Root (Input) Number", "Part Number", "Manufacturer", "Quantity", "Part Status", "Packaging"]
        for col in re_ordering_cols:
            column_list.remove(col)
            new_column_list.append(col)

        column_list.sort()
        for col in column_list:
            new_column_list.append(col)

        part_table_df = part_table_df[new_column_list]

        csv_file = part_table_df.to_csv('part_info.csv', index=False, header=True)

        return csv_file


digi_class = MultiPartDigikey('C:/Users/robal/Documents/part_numbers_copy.csv')

part_names = digi_class.get_part_names_from_csv()

data_frames = digi_class.get_dataframes(part_names)

part_csv_output = digi_class.dataframes_to_csv(data_frames)