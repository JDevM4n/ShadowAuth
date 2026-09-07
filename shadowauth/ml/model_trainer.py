from abc import ABC, abstractmethod


class ModelTrainer(ABC):
    """
    Base interface for ShadowAuth
    Machine Learning trainers.
    """

    @abstractmethod
    def train(
        self,
        x_train,
        y_train,
    ):
        """
        Train the Machine Learning model.
        """
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        x,
    ):
        """
        Generate predictions using
        the trained model.
        """
        raise NotImplementedError