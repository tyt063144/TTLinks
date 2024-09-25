import pytest
from ttlinks.common.binary_utils.binary_factory import OctetFlyWeightFactory
from ttlinks.common.binary_utils.binary import Octet


def test_singleton_factory_instance():
    # Ensure the factory instance is a Singleton
    factory1 = OctetFlyWeightFactory()
    factory2 = OctetFlyWeightFactory()

    assert factory1 is factory2, "Factory instances should be the same (Singleton pattern)."


def test_flyweight_reuse():
    # Get the factory instance
    factory = OctetFlyWeightFactory()

    # Get two Octet instances with the same binary string
    octet1 = factory.get_octet("10101010")
    octet2 = factory.get_octet("10101010")

    # Ensure that both Octet instances are the same (reused)
    assert octet1 is octet2, "Octet instances with the same binary string should be reused."
    assert isinstance(octet1, Octet), "The returned instance should be of type Octet."


def test_flyweight_new_instance():
    # Get the factory instance
    factory = OctetFlyWeightFactory()

    # Get two Octet instances with different binary strings
    octet1 = factory.get_octet("10101010")
    octet2 = factory.get_octet("11110000")

    # Ensure that the instances are different (new instance for different binary strings)
    assert octet1 is not octet2, "Octet instances with different binary strings should not be the same."
    assert isinstance(octet2, Octet), "The returned instance should be of type Octet."


def test_get_flyweights():
    # Get the factory instance
    factory = OctetFlyWeightFactory()

    # Clear the flyweights (optional, depending on the test environment setup)
    factory._OctetFlyWeightFactory__flyweights.clear()

    # Create two Octet instances through the factory
    octet1 = factory.get_octet("10101010")
    octet2 = factory.get_octet("11110000")

    # Get the current flyweights dictionary
    flyweights = factory.get_flyweights()

    # Expected flyweights
    expected_flyweights = {
        "10101010": octet1,
        "11110000": octet2
    }

    # Check that the flyweights dictionary matches the expected one
    assert flyweights == expected_flyweights, "The flyweights dictionary should match the expected dictionary."

    # Optionally, verify the specific contents of the flyweights
    assert flyweights["10101010"] is octet1, "The cached Octet for '10101010' should be octet1."
    assert flyweights["11110000"] is octet2, "The cached Octet for '11110000' should be octet2."

    # Check that the dictionary contains only two entries
    assert len(flyweights) == 2, "There should be exactly two flyweights in the cache."
