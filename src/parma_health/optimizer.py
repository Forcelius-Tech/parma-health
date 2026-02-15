from typing import List, Dict, Any, Union
import pandas as pd
import json

class Optimizer:
    """
    The Optimizer engine converts structured data (e.g. DataFrames, Dicts) 
    into TOON (Token-Oriented Object Notation) format to minimize token usage for LLM training.
    """

    def to_toon(self, data: Union[pd.DataFrame, List[Dict[str, Any]]]) -> str:
        """
        Converts the input data to a TOON-formatted string.
        
        TOON Strategy used here:
        1. Extract the schema (keys) from the first record/column headers.
        2. Represent the schema as a compact list.
        3. Represent each record as a values-only list, matching the schema order.
        4. Use a minimal separator.

        Args:
            data: A pandas DataFrame or a list of dictionaries.

        Returns:
            A string containing the TOON representation.
        """
        if isinstance(data, pd.DataFrame):
            return self._dataframe_to_toon(data)
        elif isinstance(data, list):
            return self._list_of_dicts_to_toon(data)
        else:
            raise ValueError("Unsupported data type. Expected pandas DataFrame or list of dicts.")

    def _dataframe_to_toon(self, df: pd.DataFrame) -> str:
        # 1. Get Schema (Columns)
        columns = df.columns.tolist()
        
        # 2. Get Values
        # orient='values' gives a list of lists
        values = df.values.tolist()
        
        # 3. Construct TOON object
        toon_structure = {
            "s": columns,  # "s" for schema/structure
            "d": values    # "d" for data
        }
        
        # 4. Dump to compact JSON-like string (but we call it TOON for this context)
        # Using separators to remove whitespace
        return json.dumps(toon_structure, separators=(',', ':'))

    def _list_of_dicts_to_toon(self, data: List[Dict[str, Any]]) -> str:
        if not data:
            return ""

        # 1. Infer Schema from first item
        # Note: This assumes all dicts have the same keys. 
        # For a robust implementation, we might want to unify keys across all certs.
        schema = list(data[0].keys())
        
        # 2. Extract Values
        values = []
        for item in data:
            row = [item.get(k) for k in schema]
            values.append(row)
            
        # 3. Construct TOON object
        toon_structure = {
            "s": schema,
            "d": values
        }
        
        return json.dumps(toon_structure, separators=(',', ':'))
