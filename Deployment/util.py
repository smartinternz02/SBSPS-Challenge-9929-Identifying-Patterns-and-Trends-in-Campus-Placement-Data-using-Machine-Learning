import numpy as np
import requests
import warnings
warnings.filterwarnings('ignore')

API_KEY = "jGwxgHaMTFkIvdPyph06O8zeKMnjPDRThbQB-d7z8SEa"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

__data_columns=["ssc_p", "hsc_p", "degree_p", "etest_p", "mba_p", "gender_f", "gender_m", "hsc_s_arts", "hsc_s_commerce", "hsc_s_science", "degree_t_comm&mgmt", "degree_t_others", "degree_t_sci&tech", "workex_no", "workex_yes", "specialisation_mkt&fin", "specialisation_mkt&hr"]
payload={}

def column(gender,ssc_p,hsc_p,hsc_s,degree_p,degree_t,workex,etest_p,specialisation,mba_p):
    try:       
        gender_i=__data_columns.index(gender.lower())
        hsc_s_i=__data_columns.index(hsc_s.lower())
        degree_t_i=__data_columns.index(degree_t.lower())
        specialisation_i=__data_columns.index(specialisation.lower())
        workex_i=__data_columns.index(workex.lower())
    except:
        gender_i=-1
        hsc_s_i=-1
        degree_t_i=-1
        specialisation_i=-1
        workex_i=-1
    x=np.zeros(17)
    x[0]=ssc_p
    x[1]=hsc_p
    x[2]=degree_p
    x[3]=etest_p
    x[4]=mba_p
    if gender_i>=0:
        x[gender_i]=1
    if hsc_s_i>=0:
        x[hsc_s_i]=1
    if degree_t_i>=0:
        x[degree_t_i]=1
    if specialisation_i>=0:
        x[specialisation_i]=1
    if workex_i>=0:
        x[workex_i]=1
    payload_scoring = {"input_data": [{"fields": __data_columns, "values": [list(x)]}]}
    global payload
    payload = payload_scoring
    print(payload)

def predict_salary():
    salary_response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/08ec754f-3154-41f5-9980-520c9bf49eff/predictions?version=2021-05-01', json=payload, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(salary_response_scoring.json())
    salary_predictions = salary_response_scoring.json()
    salary=salary_predictions['predictions'][0]['values'][0][0]
    return round(salary/100000,2)
   
def predict_status():
    status_response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5532712e-20d0-4cc6-801a-5886f037640d/predictions?version=2021-05-01', json=payload, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(status_response_scoring.json())
    status_predictions = status_response_scoring.json()
    return status_predictions['predictions'][0]['values'][0][0]

# column('gender_M',67.00,91.00,'hsc_s_Commerce',58.00,'degree_t_Sci&Tech','workex_No',55.0,'specialisation_Mkt&HR',58.80)
# predict_status()
# predict_salary()
# column('gender_M',56.00,52.00,'hsc_s_Science',52.00,'degree_t_Sci&Tech','workex_No',66.0,'specialisation_Mkt&HR',58.80)
# predict_status()
# predict_salary()
