import pytest
import parseanything.reading_order

def test_reading_order_module_exists():
    # Verify reading_order module loads properly without error
    assert parseanything.reading_order is not None
