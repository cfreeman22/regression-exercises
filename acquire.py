# Telco Data acquisition from the telco_db
# importing the packages 
import env 
import pandas as pd
import numpy as np
import os 

# Initiating a Connection to the MYSQL server with connection info from env.py

def get_db_url(db_name):
    from env import username, host, password
    return f'mysql+pymysql://{username}:{password}@{host}/{db_name}'



def get_telco_data():
    '''
    This function reads csv stored in the computer or the iris data from the Codeup db into a dataframe.
    '''
    filename = "telco_df.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col=0)
    else:
        # read the SQL query into a dataframe
        sql_query = """
                select * from customers
                join contract_types using (contract_type_id)
                join internet_service_types using (internet_service_type_id)
                join payment_types using (payment_type_id)
                """
        df = pd.read_sql(sql_query, get_db_url('telco_churn')) #SQL query , database name, Pandas df

        # Write that dataframe to disk for later. Called "caching" the data for later.
        df.to_csv(filename) 

        # Return the dataframe to the calling code
        return df  