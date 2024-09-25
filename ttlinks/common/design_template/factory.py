from abc import ABC, abstractmethod


class Factory(ABC):
    """
    Abstract base class for a Factory that defines a factory method for creating products.
    Subclasses are required to implement the create_product method to provide the actual product creation logic.
    This class is part of the Factory Method design pattern, providing a template for factories that produce products.
    """
    @abstractmethod
    def create_product(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses for creating and returning a product.

        Parameters:
        *args: Variable length argument list for product creation.
        **kwargs: Arbitrary keyword arguments for product creation.

        Returns:
        Product: The product instance created by the factory.

        This method should be overridden by concrete subclasses to define specific creation logic for the product.
        """
        pass
