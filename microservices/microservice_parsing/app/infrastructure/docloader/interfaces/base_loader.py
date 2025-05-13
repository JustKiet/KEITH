from abc import ABC, abstractmethod

class BaseLoader(ABC):
    """
    Abstract base class for data loaders.
    """

    @abstractmethod
    def load(self):
        """
        Load data from the specified path.

        Args:
            path (str): The path to the data file.

        Returns:
            Any: The loaded data.
        """
        raise NotImplementedError("Subclasses must implement this method.")