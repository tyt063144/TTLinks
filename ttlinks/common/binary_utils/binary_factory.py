from __future__ import annotations
from typing import Dict

from ttlinks.common.binary_utils.binary import Octet


class OctetFlyWeightFactory:
    """
    A Flyweight Factory that ensures efficient creation and reuse of Octet instances.
    This factory uses the Singleton pattern to ensure only one instance of the factory exists
    and manages a pool of flyweights (Octet instances). If an Octet instance already exists for
    a given binary string, it will reuse that instance instead of creating a new one.
    """
    __instance: OctetFlyWeightFactory = None
    __flyweights: Dict[str, Octet] = {}

    def __new__(cls):
        """
        Ensures that only one instance of the factory exists.
        If no instance exists, it creates a new one. Otherwise, it returns the existing instance.

        Returns:
            OctetFlyWeightFactory: The singleton instance of the factory.
        """
        if cls.__instance is None:
            cls.__instance = super(OctetFlyWeightFactory, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def get_octet(cls, binary_string: str) -> Octet:
        """
        Retrieves or creates an Octet instance for a given binary string. If the binary string
        already has an associated Octet instance, it will return the existing instance to save
        resources. Otherwise, a new Octet is created and stored for future reuse.

        Args:
            binary_string (str): The binary string for which an Octet is required.

        Returns:
            Octet: The Octet instance associated with the binary string.
        """
        if binary_string not in cls.__flyweights:
            cls.__flyweights[binary_string] = Octet(binary_string)
        return cls.__flyweights[binary_string]

    @classmethod
    def get_flyweights(cls) -> Dict[str, Octet]:
        return cls.__flyweights
