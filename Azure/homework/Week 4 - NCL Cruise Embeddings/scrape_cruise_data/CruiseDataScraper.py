# Importing the required libraries.
import requests
import re
import sys
import json
from bs4 import BeautifulSoup

class CruiseDataScraper:
    def __init__(self, url_file_name, pickle_file_name, text_file_name, json_file_name):
        self.url_list = self.get_url_list_to_scrape(url_file_name)
        self.pickle_file = open(pickle_file_name, "w")
        self.text_file = open(text_file_name, "w")
        self.json_file = open(json_file_name, "w")                
        
    @staticmethod
    def get_url_list_to_scrape(url_file_name):
        # open file, read each line, return as list
        url_list = []
        f = open(url_file_name, "r")
        for x in f:
            url_list.append(x)
        f.close()
        return url_list
        
    @staticmethod
    def get_json_from_url(url):
        url = url.strip()
        print("Processing url " + url);
        json_list = []
        
        # Requesting the HTML from the web page.
        page = requests.get(url)
        
        # Selecting the data.
        soup = BeautifulSoup(page.content, "html.parser")
        content = soup.find_all(type="application/ld+json")
        content = str(content)
        
        re_data = r'{\s*\"@context\": \"http://schema\.org/\",\s*\"@type\": \"Offer\"[\s\S]*}'
        items_list = re.findall(re_data, content, re.MULTILINE)
        
        if len(items_list) == 0:
            print("info: regex had no matches for url " + url)

        json_list = []
        for item in items_list:
            try:
                json_values = json.loads(item)
                json_list.append(json_values)
            except:
                print("info: exception getting json for url " + url)
        if json_list == []:
            print("info: json_list is empty for url " + url)
            return None
        else:
            return json_list
        
    @staticmethod
    def get_ship(json_values):
        potential_actions = json_values["potentialAction"]
        for action in potential_actions:
            if action["@type"] == "DepartAction":
                if action["instrument"] and action["instrument"]["name"]:
                    return str(action["instrument"]["name"])
                else:
                    return ""
        return ""

    @staticmethod
    def get_departure(json_values):
        potential_actions = json_values["potentialAction"]
        for action in potential_actions:
            if action["@type"] == "DepartAction":
                if action["toLocation"] and action["toLocation"]["name"]:
                    return str(action["toLocation"]["name"])
                else:
                    return ""
        return ""
    
    @staticmethod
    def get_arrival(json_values):
        potential_actions = json_values["potentialAction"]
        for action in potential_actions:
            if action["@type"] == "ArriveAction":
                if action["toLocation"] and action["toLocation"]["name"]:
                    return str(action["toLocation"]["name"])
                else:
                    return ""
        return ""
    
    
    @staticmethod
    def get_ports(json_values):
        potential_actions = json_values["potentialAction"]
        port_list = []
        for action in potential_actions:
            if action["@type"] == "TravelAction":
                if action["toLocation"] and action["toLocation"]["name"]:
                    port_list.append(str(action["toLocation"]["name"]))
        return port_list
    
    @staticmethod
    def get_duration(json_values):
        # Try to use the start of the name field to determine duration
        name = json_values["name"]
        parts = name.split("-")
        leftpart = parts[0]
        if leftpart.isnumeric():
            return leftpart
        else:
            return ""
    
    @staticmethod
    def get_itinerary_code(json_values):
        url = json_values["url"]
        result = re.search(r'-([^-]*)$', url)
        return result.group(1)
        
    @staticmethod
    def get_data_object_from_url(url):
        obj = {}
        json_list = CruiseDataScraper.get_json_from_url(url)
        
        for json_values in json_list:
            obj['name'] = json_values['name']
            obj['departure'] = CruiseDataScraper.get_departure(json_values)
            obj['arrival'] = CruiseDataScraper.get_arrival(json_values)
            obj['ports'] = str(CruiseDataScraper.get_ports(json_values))
            obj['description'] = json_values['description']
            if obj['description'] == '':
                print("info: description is empty for url " + url)
            obj['image'] = json_values['image'] 
            obj['url'] = json_values['url'] 
            obj['ship'] = CruiseDataScraper.get_ship(json_values)
            obj['duration'] = CruiseDataScraper.get_duration(json_values) 
            obj['itinerary_code'] = CruiseDataScraper.get_itinerary_code(json_values)
        
        return obj
        
    @staticmethod
    def write_obj_to_text_file(obj, f, first_file):
        if not first_file:
            f.write("\n")
        f.write("Title: " + obj["name"] + "\n")
        f.write("Departure: " + obj["departure"] + "\n")
        f.write("Arrival: " + obj["arrival"] + "\n")
        f.write("Ports of Call: " + str(obj["ports"]) + "\n")
        f.write("Description: " + obj["description"] + "\n")
        f.write("Hero Image: " + obj["image"] + "\n")
        f.write("URL: " + obj["url"] + "\n")
        f.write("Ship: " + obj["ship"] + "\n")
        f.write("Duration: " + obj["duration"] + " days" + "\n")
        f.write("Itinerary Code: " + obj["itinerary_code"] + "\n")

    @staticmethod
    def write_obj_to_json_file(obj, f, first_file):
        if first_file:
            f.write('{\n')
        f.write(obj["itinerary_code"] + '": {\n')
        f.write('"Title": "' + obj["name"] + '",\n')
        f.write('"Departure": "' + obj["departure"] + '",\n')
        f.write('"Arrival": "' + obj["arrival"] + '",\n')
        f.write('"Ports of Call": "' + obj["ports"] + '",\n')
        f.write('"Description": "' + obj["description"] + '",\n')
        f.write('"Hero Image": "' + obj["image"] + '",\n')
        f.write('"URL": "' + obj["url"] + '",\n')
        f.write('"Ship": "' + obj["ship"] + '",\n')
        f.write('"Duration": "' + obj["duration"] + '",\n')
        f.write('"Itinerary Code": "' + obj["itinerary_code"] + '"\n},\n')

    @staticmethod
    def write_obj_to_python_file(obj, f, first_file):
        if first_file:
            f.write('ITINERARIES = {\n');
        f.write('"' + obj["itinerary_code"] + '": {\n')
        f.write('"Title": "' + obj["name"] + '",\n')
        f.write('"Departure": "' + obj["departure"] + '",\n')
        f.write('"Arrival": "' + obj["arrival"] + '",\n')
        f.write('"Ports of Call": "' + obj["ports"] + '",\n')
        f.write('"Description": "' + obj["description"] + '",\n')
        f.write('"Hero Image": "' + obj["image"] + '",\n')
        f.write('"URL": "' + obj["url"] + '",\n')
        f.write('"Ship": "' + obj["ship"] + '",\n')
        f.write('"Duration": "' + obj["duration"] + '",\n')
        f.write('"Itinerary Code": "' + obj["itinerary_code"] + '"\n},\n')


    def generate_files(self):
        first_file = True
        f = self.text_file

        for url in self.url_list:
#        for url in [self.url_list[0]]:
            try:
                obj = self.get_data_object_from_url(url)
                if obj is None:
                    print("An exception occurred processing " + url)
                else:
                    self.write_obj_to_text_file(obj, f, first_file)
                    self.write_obj_to_json_file(obj, self.json_file, first_file)
                    self.write_obj_to_python_file(obj, self.pickle_file, first_file)
                    if first_file:
                       first_file = False
            except:
                print("An exception occurred processing " + url)

        self.close_all_files()
    
    def close_all_files(self):
        self.pickle_file.write('}')
        self.pickle_file.close()
        self.text_file.close()
        self.json_file.write('}')
        self.json_file.close()
        

if __name__ == "__main__":
    cds = CruiseDataScraper("urls.txt", "cruise_data.py", "cruise_data.txt", "cruise_data.json")
    cds.generate_files()