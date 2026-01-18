from unittest import TestCase

from django_erd_generator.contrib.dialects import Dialect
from django_erd_generator.definitions.fields import Relationship
from .models import Order
from .utils import ModelArray


class RelationshipTestCase(TestCase):
    def test_init_relationship_definition(self):
        field = Order._meta.get_field("customer")
        relationship = Relationship(field, "one_to_many")
        self.assertEqual(relationship.to_model, "tests_Order")
        self.assertEqual(relationship.from_model, "tests_Customer")
        self.assertEqual(relationship.rel, "one_to_many")

    def test_relationship_definition_dialect_render(self):
        field = Order._meta.get_field("customer")

        dialects = {
            Dialect.MERMAID: 'tests_Order ||--|{ tests_Customer: ""',
            Dialect.PLANTUML: "tests_Order::customer_id ||--|{ tests_Customer::id",
            Dialect.DBDIAGRAM: "Ref: tests_Order.customer_id < tests_Customer.id",
        }

        for dialect, expected in dialects.items():
            rel_definition = Relationship(field, "one_to_many", dialect=dialect)
            self.assertEqual(expected, rel_definition.to_string().strip())


class RelationshipArrayTestCase(TestCase):
    def test_relationship_array_dialect_render(self):
        dialects = {
            Dialect.MERMAID: 'tests_Order }|--|| tests_Customer: ""\ntests_Order }|--|| tests_Product: ""',
            Dialect.PLANTUML: "tests_Order::customer_id }|--|| tests_Customer::id\ntests_Order::product_id }|--|| tests_Product::id",
            Dialect.DBDIAGRAM: "Ref: tests_Order.customer_id > tests_Customer.id\nRef: tests_Order.product_id > tests_Product.id",
        }

        for dialect, expected in dialects.items():
            model = ModelArray.get_models("tests", dialect=dialect)[2]
            relationships = model.relationships.to_string()
            self.assertEqual(relationships, expected)
