# Script to Prep the TELCO Data

#--------Imports---------
import pandas as pd
import acquire as aqr
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

#--------Functions-------

def telco_raw_summary(df):
    '''
    This function brings in the raw telco data and prints the summary statistics,   columns, info, shape and churn preview
    '''
    print("COLUMNS NAMES OF TELCO DATASET")
    print('')
    print(df.columns)
    print('')
    print('====================================================================================')
    print("THE SHAPE OF TELCO DATASET")
    print('')
    print(f'The Telco dataset has {df.shape[0]} rows and {df.shape[1]} columns')
    print('')
    print('====================================================================================')
    print("TELCO INFO AND DATA TYPES, NEEDS TO EXAMINE TOTAL CHARGES MORE")
    print('')
    print(df.info())
    print('')
    print('====================================================================================')
    print("TELCO SUMMARY STATISTICS")
    print('')
    print(df.describe())
    print('')
    print('====================================================================================')
    print("CHECKING FOR NULLS ....")
    print('')
    print(df.isna().sum())
    print('')
    print('====================================================================================')
    print("VALUE COUNTS OF CHURN AND NO CHURN")
    print('')
    print(df['churn'].value_counts().sort_index())
                   
def viz_churn(df): # this function takes in a data frame and returns a pie chart distribution of churn
    churn = df['churn'].value_counts().sort_index()
    lables = ["Not Churned", "Churned"]
    # plot a pie chart
    plt.pie(churn, labels=lables, autopct="%1.1f%%")
    plt.title("Telco percentage of Churn ")
    plt.show()
    
    
def prep_telco():
    '''
    This function will walk through all of the cleaning and data prep 
    process needed to explore and model the Telco data set
    '''
    df = aqr.get_telco_data()                            # Using Acquire function to bring in telco data
    
    df = df.drop_duplicates()                           # Dropping Duplicates
    
    df.total_charges = df.total_charges.str.strip()     # Removing white space
    df.total_charges = df.total_charges.replace('', 0)  # Replacing total_charges empty cells with 0 due to tenure = 0
    df.total_charges = df.total_charges.astype('float64') # Convert from obj to 

    to_replace={'Yes': 1, 'No': 0, 
                'No internet service': 0, 
                'No phone service': 0}                  # Encoding (Changing Yes to 1 and No to 0)
    df = df.replace(to_replace)                         # Encoding
    
    columns_to_rename = {'contract_type': 'contract',
                   'internet_service_type': 'internet'} # Renaming columns
    df = df.rename(columns=columns_to_rename)           # Renaming

    dummy_df = pd.get_dummies(df[['gender', 'contract','internet', 'payment_type']])
    df = pd.concat([df, dummy_df], axis=1)              # Creating dummy variables and concating

    columns_to_drop = ['payment_type_id', 'internet_service_type_id', 
                        'contract_type_id']
    df = df.drop(columns=columns_to_drop)               # Dropping three columns
     
    columns_to_rename = {'gender_Female': 'female',
                   'gender_Male': 'male',
                    'contract_Month-to-month': 'monthly_contract',
                    'contract_One year': 'one_yr_contract',
                    'contract_Two year': 'two_yr_contract',
                    'internet_DSL': 'dsl',
                    'internet_Fiber optic': 'fiber',
                    'internet_None': 'no_internet',
                    'payment_type_Bank transfer (automatic)': 'bank_transfer',
                    'payment_type_Credit card (automatic)': 'credit_card',
                    'payment_type_Electronic check': 'electronic_check',
                    'payment_type_Mailed check': 'mailed_check'}
    df = df.rename(columns=columns_to_rename) # More columns to rename
     
    return df

def split_telco(df):

    '''
    Takes in a dataframe and return train, validate, test subset dataframes
    '''
    train, test = train_test_split(df, test_size = .2, random_state=123, stratify=df.churn)
    train, validate = train_test_split(train, test_size=.3, random_state=123, stratify=train.churn)
    print(f'train_encoded, shape: {train.shape}')
    print(f'validate_encoded, shape: {validate.shape}')
    print(f'test_encoded, shape: {test.shape}')
    return train, validate, test