import pytest
import pandas as pd
import json
from parma_health.optimizer import Optimizer

def test_optimizer_dataframe_to_toon():
    df = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'age': [30, 25]
    })
    
    optimizer = Optimizer()
    toon_output = optimizer.to_toon(df)
    
    # Verify it's valid JSON
    data = json.loads(toon_output)
    
    assert data['s'] == ['name', 'age']
    assert data['d'] == [['Alice', 30], ['Bob', 25]]

def test_optimizer_list_of_dicts_to_toon():
    data_list = [
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25}
    ]
    
    optimizer = Optimizer()
    toon_output = optimizer.to_toon(data_list)
    
    data = json.loads(toon_output)
    
    assert data['s'] == ['name', 'age']
    assert data['d'] == [['Alice', 30], ['Bob', 25]]

def test_optimizer_empty_list():
    optimizer = Optimizer()
    assert optimizer.to_toon([]) == ""
