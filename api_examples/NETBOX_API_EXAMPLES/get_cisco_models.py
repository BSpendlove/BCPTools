## pip install pandas
## This script doesn't work at all....

import pandas as pd
import json
from pprint import pprint

cisco_catalyst_products = "https://www.cisco.com/c/en/us/products/switches/catalyst-{0}-series-switches/models-comparison.html"

table_data = pd.read_html((cisco_catalyst_products.format("3560")),header=0)

model_variable = ''

if('Model' in table_data[0]):
    model_variable = 'Model'
elif('Models' in table_data[0]):
    model_variable = 'Models'
    

#Not all cisco model compare pages have the same Column
tdata = pd.DataFrame(table_data[0],columns=[model_variable])
test = tdata.to_json()



