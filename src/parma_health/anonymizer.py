from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import pandas as pd
from parma_health.primitives import mask_value


class AnonymizationRule(BaseModel):
    """
    Defines a single anonymization rule for a specific field.
    """
    field: str
    action: str
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)


class AnonymizerConfig(BaseModel):
    """
    Configuration for the Anonymizer engine, containing a list of rules.
    """
    rules: List[AnonymizationRule]
    salt: str = "default_salt"


class Anonymizer:
    """
    The core engine that applies anonymization rules to data.
    """
    def __init__(self, config: AnonymizerConfig):
        self.config = config

    def process_chunk(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies configured rules to a DataFrame chunk.
        Returns the modified DataFrame.
        """
        # Work on a copy to avoid side effects
        df_out = df.copy()

        for rule in self.config.rules:
            if rule.field in df_out.columns:
                self._apply_rule(df_out, rule)

        return df_out

    def _apply_rule(self, df: pd.DataFrame, rule: AnonymizationRule) -> None:
        """
        Internal method to dispatch rule actions.
        Currently supports 'suppress' and 'mask' (dummy implementation).
        """
        if rule.action == "suppress":
            df.drop(columns=[rule.field], inplace=True)
        elif rule.action == "mask":
            # Use specific salt if provided in rule params,
            # else global config salt
            salt = rule.params.get("salt", self.config.salt)
            df[rule.field] = df[rule.field].apply(
                lambda x: mask_value(x, salt=salt)
            )
        elif rule.action == "test_transform":
            # For testing purposes
            df[rule.field] = df[rule.field].astype(str) + "_transformed"
