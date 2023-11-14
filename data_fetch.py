import csv
import requests 
import pandas as pd
import os
from datetime import date

c_date = str(date.today())
os.mkdir(f'data/{c_date}')

urls =["http://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv","https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv",
"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv","https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv",
"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv"]
f_names=["ARKK","ARKQ","ARKW","ARKG","ARKF"]

for url,f_name in zip(urls,f_names):
    response = requests.get(url)
    
    with open(os.path.join(f"data/{c_date}",f'{f_name}.csv'),'wb') as f:
        f.write(response.content)


