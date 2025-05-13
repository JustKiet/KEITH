from abc import ABC, abstractmethod

class BaseParser(ABC):
    """
    A base class for parsers.
    """

    @abstractmethod
    def parse(self):
        """
        Parse the given data and return a structured response.

        Returns:
            A structured response containing the parsed data.
        """
        raise NotImplementedError