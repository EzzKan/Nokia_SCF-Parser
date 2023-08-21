###PCL_ezra
###The code simply parses SCF.xml file to xlsx format for analysis

##Import necessary libraries/Modules
import xml.etree.ElementTree as et
import pandas as pd
import os
import time as dt
from tqdm import tqdm  # tqdm for progress bar

# Record starting time
start = dt.time()

# Namespace for XML elements
namespace = {'ns': 'raml21.xsd'}

### XML and CSV paths
xml_directory = 'C://Users//PCL//Desktop//ALL_TEST//PARSER TEST'
csv_directory = 'C://Users//PCL//Desktop//3G'

###Change working directory to XML directory
os.chdir(xml_directory)

###Parse XML file
tree = et.parse('SCF.xml')
root = tree.getroot()

###Collect unique object names
objs = {MO.get('class') for MO in root.findall('.//ns:managedObject', namespaces=namespace)}

###Record time taken to collect objects
objs_time = dt.time()
print(f'Objects are collected: {round(objs_time - start, 2)}')

###Process objects and parameters
all_names_and_values = []

for mo_class_name in tqdm(objs):  # Iterate over unique object classes
    for o in root.findall(f'.//ns:managedObject[@class="{mo_class_name}"]', namespaces=namespace):
        mo_para_name = o.get('distName')
        mo_para_value = o.get('version')
        para_data = {
            'class': mo_class_name,
            'version': mo_para_value,
            'distName': mo_para_name
        }

        # Iterate over parameters within the object
        for i in o.findall('.//ns:p', namespaces=namespace):
            child_para_name = i.get('name')
            child_para_value = i.text

            if child_para_name and child_para_value:
                para_data[child_para_name] = child_para_value

        all_names_and_values.append(para_data)

# Create DataFrame from collected data
df_mo = pd.DataFrame(all_names_and_values)

###Change working directory to CSV directory
os.chdir(csv_directory)

### Save DataFrame to Excel
df_mo.to_excel('parsed_data1.xlsx', index=False)

### Record ending time
stop = dt.time()
print(f'Processing finished. Elapsed time = {round(stop - start, 2)}')
