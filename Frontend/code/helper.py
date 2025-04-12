import pandas as pd
import numpy as np
from functools import lru_cache

@lru_cache(maxsize=1)
def get_symptoms_columns():
    df = pd.read_csv('data/clean_dataset.tsv', sep='\t')
    return df.columns.tolist()

@lru_cache(maxsize=1)
def get_symptoms_dict():
    columns = get_symptoms_columns()
    return {symptom: idx for idx, symptom in enumerate(columns)}

def prepare_symptoms_array(symptoms):
    symptoms_dict = get_symptoms_dict()
    symptoms_array = np.zeros((1,133))
    
    for symptom in symptoms:
        if symptom in symptoms_dict:
            symptoms_array[0, symptoms_dict[symptom]] = 1
            
    return symptoms_array

@lru_cache(maxsize=100)
def get_disease_description(disease):
    df = pd.read_csv('data/symptom_Description.csv')
    desc = df[df['Disease'] == disease]['Description'].values
    return desc[0] if len(desc) > 0 else "No description available"

@lru_cache(maxsize=100)
def get_disease_precautions(disease):
    df = pd.read_csv('data/symptom_precaution.csv')
    prec = df[df['Disease'] == disease].filter(regex='Precaution').values
    return prec[0] if len(prec) > 0 else []
