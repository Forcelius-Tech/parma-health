import pytest
import pandas as pd
from parma_health.connectors import CSVConnector


def test_csv_connector_read(tmp_path):
    """Verify CSVConnector can read data in chunks."""
    # Create valid CSV
    df = pd.DataFrame({'col1': range(10), 'col2': range(10, 20)})
    csv_path = tmp_path / "test.csv"
    df.to_csv(csv_path, index=False)

    # Read with small chunksize
    connector = CSVConnector(str(csv_path), chunksize=4)
    chunks = list(connector.read())

    assert len(chunks) == 3  # 10 rows / 4 = 3 chunks (4, 4, 2)
    reconstructed_df = pd.concat(chunks)
    pd.testing.assert_frame_equal(df, reconstructed_df.reset_index(drop=True))


def test_csv_connector_write(tmp_path):
    """Verify CSVConnector can write data from chunks."""
    # Create chunks
    df1 = pd.DataFrame({'col1': [0, 1], 'col2': [10, 11]})
    df2 = pd.DataFrame({'col1': [2, 3], 'col2': [12, 13]})

    def data_gen():
        yield df1
        yield df2

    csv_path = tmp_path / "output.csv"
    connector = CSVConnector(str(csv_path))
    connector.write(data_gen())

    # Verify output
    result = pd.read_csv(csv_path)
    expected = pd.concat([df1, df2]).reset_index(drop=True)
    pd.testing.assert_frame_equal(result, expected)


def test_read_nonexistent_file():
    """Verify error raised for missing file."""
    connector = CSVConnector("nonexistent.csv")
    with pytest.raises(FileNotFoundError):
        next(connector.read())
