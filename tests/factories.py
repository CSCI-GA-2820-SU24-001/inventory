"""
Test Factory to make fake objects for testing
"""

import factory
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
    # price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    price = factory.Faker("pyfloat", left_digits=3, right_digits=2, positive=True)
    product_id = factory.Faker("random_int", min=1, max=100)
    restock_level = factory.Faker("random_int", min=0, max=50)
    condition = factory.Faker("random_element", elements=("new", "open box", "used"))
