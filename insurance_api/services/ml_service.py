import pandas as pd
from sklearn.linear_model import LinearRegression
from insurance_api.core.config import INSURANCE_CSV_PATH

class MLService:
    _model = None
    _features = ['age', 'bmi', 'smoker_yes']

    @classmethod
    def get_model(cls) -> LinearRegression:
        """Returns the trained model, trains it if not already trained."""
        if cls._model is None:
            cls._train_model()
        return cls._model

    @classmethod
    def _train_model(cls):
        """Trains a linear regression model and stores it in the class."""
        print("Training ML model...")
        df = pd.read_csv(INSURANCE_CSV_PATH)
        df = pd.get_dummies(df, columns=['smoker'], drop_first=True, dtype=int)
        
        X = df[cls._features]
        y = df['charges']
        
        model = LinearRegression()
        model.fit(X, y)
        cls._model = model
        print("ML model training complete.")

    @classmethod
    def predict(cls, age: int, bmi: float, is_smoker: bool) -> float:
        """Makes a prediction using the trained model."""
        model = cls.get_model()
        
        smoker_value = 1 if is_smoker else 0
        data = {'age': [age], 'bmi': [bmi], 'smoker_yes': [smoker_value]}
        input_df = pd.DataFrame(data)
        
        prediction = model.predict(input_df)
        return round(prediction[0], 2)

# Instantiate the service
ml_service = MLService()