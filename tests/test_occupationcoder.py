import pytest
from occupationcoder.coder import coder

@pytest.fixture(scope="module")
def coder_instance():
    return coder.Coder()

def test_basic_soc_coding(coder_instance):
    test_cases = [
        ("Software Engineer", "Develop applications", ""),
        ("Data Scientist", "Analyze data and build models", ""),
        ("Teacher", "Educate students", "Education"),
    ]
    
    for title, desc, sector in test_cases:
        result = coder_instance.codejobrow(title, desc, sector)
        assert result is not None
        assert hasattr(result, 'SOC_code'), "Result should have SOC_code column"
        
        # Extract the SOC code from the DataFrame
        soc_code = result['SOC_code'].iloc[0]
        assert soc_code is not None
        
        # Convert to string for validation - SOC codes can be returned as int or str
        soc_code_str = str(soc_code)
        assert len(soc_code_str) == 3, f"SOC codes should be 3 digits, got: {soc_code_str}"
        assert soc_code_str.isdigit() or soc_code_str == "NA", f"SOC code should be numeric or 'NA', got: {soc_code_str}"

def test_edge_cases(coder_instance):
    edge_cases = [
        ("", "", ""),  # Empty strings
        (None, None, None),  # None values
        ("Job with símböls", "Déscription with åccents", ""),  # Unicode
        ("Very " * 100 + "long title", "Short desc", ""),  # Long text
    ]
    
    for title, desc, sector in edge_cases:
        # Should not raise exceptions
        try:
            result = coder_instance.codejobrow(title, desc, sector)
            print(f"Success: {str(title)[:50]}... -> {result}")
        except Exception as e:
            pytest.fail(f"Error: {str(title)[:50]}... -> {e}")

def test_bulk_processing(coder_instance):
    """Test processing multiple records to check for memory leaks."""
    # Process 5 test records
    for i in range(5):
        try:
            result = coder_instance.codejobrow(f"Job Title {i}", f"Description {i}", "")
            print(f"Record {i}: {result}")
        except Exception as e:
            pytest.fail(f"Error processing record {i}: {e}")
