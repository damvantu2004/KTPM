import joblib
import xgboost as xgb

class ModelManager:
    _instance = None
    _models = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance
    
    def load_model(self, name, path):
        if name not in self._models:
            self._models[name] = joblib.load(path)
        return self._models[name]
    
    def clear_models(self):
        self._models.clear()