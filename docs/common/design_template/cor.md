# `cor.py` Module Documentation

## Overview

The `cor.py` module provides a flexible framework for implementing the **Chain of Responsibility (CoR)** design pattern. This pattern allows a series of handlers to process a request, either by handling it or passing it along the chain. The module includes both unidirectional and bidirectional handler classes, offering flexibility in how the chain is constructed and traversed.

- **`CoRHandler`**: The abstract base class for all handlers in the chain.
- **`SimpleCoRHandler`**: A unidirectional handler that passes requests to the next handler in the chain.
- **`BidirectionalCoRHandler`**: A bidirectional handler that allows traversal of the chain in both directions (next and previous).

The module is designed to provide flexibility in how requests are handled and propagated through the chain, depending on the requirements of the specific application.

---

## Classes

### 1. `CoRHandler`

#### Description

The `CoRHandler` class is an abstract base class that defines the core interface for handlers in the Chain of Responsibility pattern. It requires concrete subclasses to implement methods for setting the next handler in the chain and handling a request. The class itself cannot be instantiated but serves as the foundation for other handler classes.

#### Methods

- **`set_next(self, h: CoRHandler) -> CoRHandler`**:
    - Abstract method to set the next handler in the chain.
    - **Parameters**:
        - `h` (`CoRHandler`): The next handler to link in the chain.
    - **Returns**: The next handler, allowing method chaining.
    - **Abstract**: Must be implemented by concrete subclasses.

- **`handle(self, request)`**:
    - Abstract method to handle the request or pass it to the next handler.
    - **Parameters**:
        - `request`: The request that needs to be handled. The type of the request is determined by the specific implementation.
    - **Abstract**: Must be implemented by concrete subclasses.

---

### 2. `SimpleCoRHandler`

#### Description

`SimpleCoRHandler` is a unidirectional handler that forwards requests to the next handler in the chain if it cannot process the request itself. This class is suitable for simple, forward-only chains where requests are passed from one handler to the next.

#### Methods

- **`__init__(self)`**:
    - Initializes the handler with no reference to the next handler.

- **`set_next(self, h: CoRHandler) -> CoRHandler`**:
    - Sets the next handler in the chain and returns the handler for chaining.
    - **Parameters**:
        - `h` (`CoRHandler`): The next handler to link.
    - **Returns**: The next handler, allowing method chaining.
    - **Raises**: 
        - `TypeError`: If `h` is not an instance of `CoRHandler`.

- **`get_next(self) -> CoRHandler`**:
    - Returns the next handler in the chain.
    - **Returns**: The next handler in the chain.

- **`handle(self, request)`**:
    - Abstract method for processing the request or passing it to the next handler.
    - **Parameters**:
        - `request`: The request to handle. Subclasses must implement this method.

#### Example Usage

```python
class ConcreteHandlerX(SimpleCoRHandler):
    def handle(self, request):
        if request == "X":
            print("Handler X processed the request")
        elif self.get_next():
            self.get_next().handle(request)

handler_x = ConcreteHandlerX()
handler_y = ConcreteHandlerX()

handler_x.set_next(handler_y)

handler_x.handle("Y")  # Passed to handler_y
```

---

### 3. `BidirectionalCoRHandler`

#### Description

`BidirectionalCoRHandler` extends the Chain of Responsibility pattern by allowing handlers to maintain references to both the next and previous handlers in the chain. This is useful in situations where requests may need to be passed backward as well as forward.

#### Methods

- **`__init__(self)`**:
    - Initializes the handler with no references to the next or previous handlers.

- **`set_next(self, h: CoRHandler) -> CoRHandler`**:
    - Sets the next handler in the chain and also links the previous handler in the chain. This method ensures the chain can be traversed in both directions.
    - **Parameters**:
        - `h` (`CoRHandler`): The next handler to link.
    - **Returns**: The next handler, allowing method chaining.
    - **Raises**: 
        - `TypeError`: If `h` is not an instance of `CoRHandler`.

- **`get_next(self) -> CoRHandler`**:
    - Returns the next handler in the chain.
    - **Returns**: The next handler in the chain.

- **`get_previous(self) -> CoRHandler`**:
    - Returns the previous handler in the chain.
    - **Returns**: The previous handler in the chain.

- **`handle(self, request)`**:
    - Abstract method for processing the request or passing it forward or backward.
    - **Parameters**:
        - `request`: The request to handle. Subclasses must implement this method.

#### Example Usage

```python
class ConcreteHandlerA(BidirectionalCoRHandler):
    def handle(self, request):
        if request == "A":
            print("Handler A processed the request")
        elif self.get_next():
            self.get_next().handle(request)

class ConcreteHandlerB(BidirectionalCoRHandler):
    def handle(self, request):
        if request == "B":
            print("Handler B processed the request")
        elif self.get_next():
            self.get_next().handle(request)

handler_a = ConcreteHandlerA()
handler_b = ConcreteHandlerB()

handler_a.set_next(handler_b)

handler_a.handle("B")  # Passed to handler_b
print(handler_b.get_previous().__class__.__name__)  # Returns handler_a
```
Expected Output:
```
Handler B processed the request
ConcreteHandlerA
```

---

## Design Pattern

The `cor.py` module implements the **Chain of Responsibility** design pattern, allowing requests to be passed along a chain of handlers. Each handler in the chain can either process the request or pass it along to the next handler. The module supports both unidirectional and bidirectional chains, providing flexibility in how requests are handled and propagated.

- **Unidirectional Chain**: Implemented through `SimpleCoRHandler`, where handlers only maintain a reference to the next handler.
- **Bidirectional Chain**: Implemented through `BidirectionalCoRHandler`, where handlers maintain references to both the next and previous handlers, allowing for forward and backward traversal.

---
