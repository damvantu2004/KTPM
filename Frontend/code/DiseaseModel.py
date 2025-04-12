import xgboost as xgb
import pandas as pd
import numpy as np

class DiseaseModel:
    def __init__(self):
        self._symptoms_df = None
        self._desc_df = None
        self._precautions_df = None
        self._all_symptoms = None
        self.symptoms = None
        self.pred_disease = None
        self.model = xgb.XGBClassifier()
        self._diseases = None

    @property
    def symptoms_df(self):
        if self._symptoms_df is None:
            self._symptoms_df = pd.read_csv('data/clean_dataset.tsv', sep='\t')
        return self._symptoms_df

    @property
    def desc_df(self):
        if self._desc_df is None:
            self._desc_df = pd.read_csv('data/symptom_Description.csv')
            self._desc_df = self._desc_df.apply(lambda col: col.str.strip())
        return self._desc_df

    @property
    def precautions_df(self):
        if self._precautions_df is None:
            self._precautions_df = pd.read_csv('data/symptom_precaution.csv')
            self._precautions_df = self._precautions_df.apply(lambda col: col.str.strip())
        return self._precautions_df

    @property
    def all_symptoms(self):
        if self._all_symptoms is None:
            self._all_symptoms = self.symptoms_df.columns[:-1]  # exclude 'Disease' column
        return self._all_symptoms

    @property
    def diseases(self):
        if self._diseases is None:
            y_data = self.symptoms_df.iloc[:,-1]
            y_data = y_data.astype('category')
            self._diseases = y_data.cat.categories
        return self._diseases

    def load_xgboost(self, model_path):
        self.model.load_model(model_path)

    def save_xgboost(self, model_path):
        self.model.save_model(model_path)

    def predict(self, X):
        self.symptoms = X
        disease_pred_idx = self.model.predict(self.symptoms)
        self.pred_disease = self.diseases[disease_pred_idx].values[0]
        disease_probability_array = self.model.predict_proba(self.symptoms)
        disease_probability = disease_probability_array[0, disease_pred_idx[0]]
        return self.pred_disease, disease_probability

    def describe_disease(self, disease_name):
        if disease_name not in self.diseases:
            return "That disease is not contemplated in this model"
        return self.desc_df[self.desc_df['Disease'] == disease_name]['Description'].values[0]

    def describe_predicted_disease(self):
        if self.pred_disease is None:
            return "No predicted disease yet"
        return self.describe_disease(self.pred_disease)

    def disease_precautions(self, disease_name):
        if disease_name not in self.diseases:
            return "That disease is not contemplated in this model"
        return self.precautions_df[self.precautions_df['Disease'] == disease_name].filter(regex='Precaution').values.tolist()[0]

    def predicted_disease_precautions(self):
        if self.pred_disease is None:
            return "No predicted disease yet"
        return self.disease_precautions(self.pred_disease)
