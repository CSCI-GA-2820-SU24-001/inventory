"""
Test Factory to make fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from service.models import InventoryItem


class InventoryItemFactory(factory.Factory):
    """Creates fake inventory items"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = InventoryItem

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    quantity = factory.Faker("random_int", min=0, max=100)
    price = FuzzyDecimal(0.01, 999.99, precision=2)
    product_id = factory.Faker("random_int", min=1, max=100)
    restock_level = factory.Faker("random_int", min=0, max=50)
    condition = FuzzyChoice(choices=["new", "open box", "used"])
