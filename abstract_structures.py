from abc import ABC, abstractmethod


class AbelianGroup(ABC):
    """Abstract class of an abelian group.
    Implements __init__, __add__, __neg__, __sub__, __eq__,
    and all the r- variations.
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __radd__(self, other):
        pass

    @abstractmethod
    def __neg__(self):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __rsub__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass


class Ring(AbelianGroup):
    """Abstract class of a ring. Inherits AbelianGroup.
    Implements __mul__ and __rmul__.
    """
    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __rmul__(self, other):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is int:
            return True
        return NotImplemented


class Field(Ring):
    """Abstract class of a field. Inherits Ring.
    Implements __truediv__ and __rtruediv__.
    """
    @abstractmethod
    def __truediv__(self, other):
        pass

    @abstractmethod
    def __rtruediv__(self, other):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is float:
            return True
        return NotImplemented
