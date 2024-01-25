""" Test script executing all the necessary unit tests for the functions in analytic_tools/utilities.py module
    which is a part of the analytic_tools package
"""

# Include the necessary packages here
from pathlib import Path
import pytest

# This should work if analytic_tools has been installed properly in your environment
from analytic_tools.utilities import (
    get_dest_dir_from_csv_file,
    get_diagnostics,
    is_gas_csv,
    merge_parent_and_basename,
)


@pytest.mark.task12
def test_get_diagnostics(example_config):
    """Test functionality of get_diagnostics in utilities module

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
                                     from Figure 1 in assignment2.md

    Returns:
    None
    """
    # Remove if you implement this task
    #raise NotImplementedError("Remove me if you implement this mandatory task")
    dir = get_diagnostics(example_config)

    assert dir["subdirectories"] == 5
    assert dir["files"] == 10
    assert dir[".csv files"] == 8
    assert dir[".txt files"] == 0
    assert dir[".npy files"] == 2
    assert dir[".md files"] == 0
    assert dir["other files"] == 0


@pytest.mark.task12
@pytest.mark.parametrize(
    "exception, dir",
    [
        (NotADirectoryError, "Not_a_real_directory"),
        
        # add more combinations of (exception, dir) here
    ],
)
def test_get_diagnostics_exceptions(exception, dir):
    """Test the error handling of get_diagnostics function

    Parameters:
        exception (concrete exception): The exception to raise
        dir (str or pathlib.Path): The parameter to pass as 'dir' to the function

    Returns:
        None
    """
    # Remove if you implement this task
    #raise NotImplementedError("Remove me if you implement this mandatory task")
    with pytest.raises(exception):
        get_diagnostics(dir)


@pytest.mark.task22
def test_is_gas_csv():
    """Test functionality of is_gas_csv from utilities module

    Parameters:
        None

    Returns:
        None
    """
    # Remove if you implement this task
    #raise NotImplementedError("Remove me if you implement this mandatory task")
    dir = Path(__file__).parent / "pollution_data/by_src/src_airtraffic/N2O_DZA.csv"    
    assert is_gas_csv(dir) == False

@pytest.mark.task22
@pytest.mark.parametrize(
    "exception, path",
    [
        (ValueError, Path(__file__).parent.absolute()),
        (ValueError, Path(__file__).parent / "pollution_data/by_src/src_industry"),
        (ValueError, Path(__file__).parent / "pollution_data/by_src/src_industry/XLxgn_1542.txt"),
        (TypeError, 31),
        # Add more combinations of (exception, path) here
    ],
)
def test_is_gas_csv_exceptions(exception, path):
    """Test the error handling of is_gas_csv function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'path' to function

    Returns:
        None
    """
    with pytest.raises(exception):
        is_gas_csv(path)


@pytest.mark.task24
def test_get_dest_dir_from_csv_file(example_config):
    """Test functionality of get_dest_dir_from_csv_file in utilities module.

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
            from Figure 1 in assignment2.md

    Returns:
        None
    """
    # Remove if you implement this task
    #raise NotImplementedError("Remove me if you implement this mandatory task")
    path = Path(example_config)
    dest_parent = path / "pollution_data_restructured/by_gas"
    dest_parent.mkdir(parents=True)

    # Create a sample original gas .csv file
    original_file = path / "pollution_data/by_src/src_agriculture"/"H2.csv"

    # Get the destination directory using the function
    dest_dir = get_dest_dir_from_csv_file(dest_parent, original_file)

    # Check if the destination directory exists
    assert dest_dir.is_dir()
    assert dest_dir.name == "gas_H2"


@pytest.mark.task24
@pytest.mark.parametrize(
    "exception, dest_parent, file_path",
    [
        (ValueError, Path(__file__).parent.absolute(), "foo.txt"),
        # add more combinations of (exception, dest_parent, file_path) here
    ],
)
def test_get_dest_dir_from_csv_file_exceptions(exception, dest_parent, file_path):
    """Test the error handling of get_dest_dir_from_csv_file function

    Parameters:
        exception (concrete exception): The exception to raise
        dest_parent (str or pathlib.Path): The parameter to pass as 'dest_parent' to the function
        file_path (str or pathlib.Path): The parameter to pass as 'file_path' to the function

    Returns:
        None
    """
    # Remove if you implement this task
    #raise NotImplementedError("Remove me if you implement this mandatory task")
    with pytest.raises(exception):
        get_dest_dir_from_csv_file(dest_parent, file_path)


@pytest.mark.task26
def test_merge_parent_and_basename():
    """Test functionality of merge_parent_and_basename from utilities module

    Parameters:
        None

    Returns:
        None
    """
    # Remove if you implement this task
    #raise NotImplementedError("Remove me if you implement this mandatory task")
    dir = "assignment2/pollution_data/by_src/src_agriculture/CO2.csv"
    something = merge_parent_and_basename(dir) 
    assert something == 'src_agriculture_CO2.csv'
    


@pytest.mark.task26
@pytest.mark.parametrize(
    "exception, path",
    [
        (TypeError, 33),
        (ValueError, 'filename.txt')
        # add more combinations of (exception, path) here
    ],
)
def test_merge_parent_and_basename_exceptions(exception, path):
    """Test the error handling of merge_parent_and_basename function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'pass' to the function

    Returns:
        None
    """
    # Remove if you implement this task
    #raise NotImplementedError("Remove me if you implement this mandatory task")
    with pytest.raises(exception):
        merge_parent_and_basename(path)
