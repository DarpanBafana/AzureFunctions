from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os

def get_secret_from_key_vault(key):
    try:
        client = get_key_vault_secret_client()
        value = client.get_secret(key).value
        return value
    except Exception as e:
        raise Exception(f'get_secret_from_key_vault failed, error message: {str(e)}\n')
    
def get_key_vault_secret_client():
    try:
        client_KEY_VAULT_URL = os.environ['client_KEY_VAULT_URL']
        credential = DefaultAzureCredential()
        return SecretClient(vault_url=client_KEY_VAULT_URL, credential=credential)    
    except Exception as e:
        raise Exception(f'get_key_vault_secret_client failed, error message: {str(e)}\n')
    
def ignore_exception(IgnoreException=Exception,DefaultVal=None):
    """ Decorator for ignoring exception from a function """
    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal
        return _dec
    return dec

def transorm_excel_header(df):
    # get new names based on the values of a previous named column
    new_column_names = []
    counter = 0
    for col_name in df.columns:
        if (col_name[:7].strip()=="Unnamed"):
            new_column_names.append("F"+str(counter+1))
        else:
            base_name = col_name
            new_column_names.append(base_name)
        counter +=1
        
    # convert to dict key pair
    dictionary = dict(zip(df.columns.tolist(),new_column_names))
    # rename columns
    df = df.rename(columns=dictionary)
    # drop first column
    df = df.iloc[1:].reset_index(drop=True)
    return df