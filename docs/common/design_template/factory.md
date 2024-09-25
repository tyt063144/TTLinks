# `factory.py` Module Documentation

## Overview

The `factory.py` module contains the Factory classes, which is an abstract base class following the **Factory Method** design pattern. This pattern defines a method for creating objects (products), but allows subclasses to determine the specific type of object that will be created. The module provides a flexible and extensible structure for creating different types of products without modifying the core logic.

---

## Class

### 1. `Factory`

#### Description

The `Factory` class is an abstract base class (ABC) that defines the structure for creating products. It provides a blueprint for concrete factories to implement the product creation logic by overriding the `create_product` method. This class is designed to be extended, allowing developers to create specific factories that produce various products.

#### Methods

##### 1. `create_product(self, *args, **kwargs)`
```python
@abstractmethod
def create_product(self, *args, **kwargs):
```
- This method is an abstract factory method that must be implemented by subclasses. It is responsible for creating and returning a product instance.
  
- **Parameters**:
    - `*args`: Variable-length argument list for passing positional arguments to the product creation logic.
    - `**kwargs`: Arbitrary keyword arguments for passing additional parameters to the product creation logic.
  
- **Returns**:
    - The concrete product instance created by the factory. The specific type of product depends on the subclass implementation.
  
- **Abstract**: This method must be implemented by any concrete subclass that inherits from `Factory`.

---

## Example Usage

Here’s an example of how you might use the `Factory` class to create specific factories for different products:

```python
class CarFactory(Factory):
    def create_product(self, model, year):
        return Car(model, year)

class Car:
    def __init__(self, model, year):
        self.model = model
        self.year = year

    def __str__(self):
        return f"Car Model: {self.model}, Year: {self.year}"

# Example usage
factory = CarFactory()
car = factory.create_product(model="Sedan", year=2022)
print(car)  # Output: Car Model: Sedan, Year: 2022
```

In this example:
- The `CarFactory` class inherits from `Factory` and implements the `create_product` method to create a `Car` instance.
- The `Car` class represents the product created by the factory.

---

## Design Pattern

- **Factory Method**: The `Factory` class is part of the Factory Method design pattern, which allows subclasses to define how products are created while keeping the core logic flexible and extensible.

---

