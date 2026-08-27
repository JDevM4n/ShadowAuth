from abc import ABC, abstractmethod


class ModelTrainer(ABC):
    """
    Base class for all Machine Learning trainers.
    """

    @abstractmethod
    def train(self):
        """
        Train the machine learning model.
        """
        pass

    @abstractmethod
    def predict(self):
        """
        Predict using the trained model.
        """
        pass