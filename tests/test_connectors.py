import pytest
from parma_health.connectors import DataConnector


def test_cannot_instantiate_abstract_connector():
    """Verify that DataConnector cannot be instantiated directly."""
    with pytest.raises(TypeError):
        DataConnector()


def test_subclass_must_implement_methods():
    """Verify that subclasses must implement read and write."""
    class IncompleteConnector(DataConnector):
        def read(self):
            pass
        # Missing write()

    with pytest.raises(TypeError):
        IncompleteConnector()


def test_valid_subclass():
    """Verify that a valid subclass can be instantiated."""
    class ValidConnector(DataConnector):
        def read(self):
            yield "data"

        def write(self, data):
            pass

    connector = ValidConnector()
    assert isinstance(connector, DataConnector)
