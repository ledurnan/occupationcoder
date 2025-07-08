import pytest
import time
import pandas as pd
import os
from occupationcoder.coder import coder

@pytest.fixture(scope="module")
def coder_instance():
    return coder.Coder()

@pytest.fixture(scope="module")
def test_data():
    """Load test vacancy data from CSV file."""
    # Get the path to the test data file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(test_dir, 'data', 'test_vacancies.csv')
    
    # Load the CSV data with proper encoding handling
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        # Fallback to latin-1 encoding if utf-8 fails
        df = pd.read_csv(csv_path, encoding='latin-1')
    
    # Convert to list of tuples for easier processing
    test_cases = []
    for _, row in df.iterrows():
        # Clean and handle potential encoding issues
        title = str(row['job_title']).replace('\x92', "'").replace('\x93', '"').replace('\x94', '"')
        description = str(row['job_description']).replace('\x92', "'").replace('\x93', '"').replace('\x94', '"')
        sector = str(row['job_sector']).replace('\x92', "'").replace('\x93', '"').replace('\x94', '"')
        
        test_cases.append((title, description, sector))
    
    return test_cases

def test_single_job_performance(coder_instance):
    """Test performance of coding a single job entry."""
    job_title = "Software Engineer"
    job_description = "Develop applications using Python and JavaScript"
    job_sector = "Technology"
    
    start_time = time.time()
    result = coder_instance.codejobrow(job_title, job_description, job_sector)
    end_time = time.time()
    
    processing_time = end_time - start_time
    
    assert result is not None
    assert hasattr(result, 'SOC_code')
    
    print(f"\n📊 Single Job Performance:")
    print(f"   Processing time: {processing_time:.3f} seconds")
    print(f"   Result: {result['SOC_code'].iloc[0]}")

def test_csv_data_performance(coder_instance, test_data):
    """Test performance of coding all entries from the test CSV file."""
    print(f"\n🚀 Performance Test: Processing {len(test_data)} job entries from CSV")
    
    results = []
    start_time = time.time()
    
    for i, (title, description, sector) in enumerate(test_data):
        try:
            result = coder_instance.codejobrow(title, description, sector)
            soc_code = result['SOC_code'].iloc[0] if result is not None else 'ERROR'
            results.append({
                'job_title': title,
                'soc_code': soc_code,
                'success': True
            })
            
            # Print progress for longer lists
            if len(test_data) > 5 and (i + 1) % max(1, len(test_data) // 5) == 0:
                print(f"   Progress: {i + 1}/{len(test_data)} entries processed...")
                
        except Exception as e:
            results.append({
                'job_title': title,
                'soc_code': 'ERROR',
                'success': False,
                'error': str(e)
            })
            print(f"   ❌ Error processing '{title[:30]}...': {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Calculate performance metrics
    successful_entries = sum(1 for r in results if r['success'])
    failed_entries = len(results) - successful_entries
    entries_per_second = len(test_data) / total_time if total_time > 0 else 0
    avg_time_per_entry = total_time / len(test_data) if len(test_data) > 0 else 0
    
    # Print detailed results
    print(f"\n📈 Performance Results:")
    print(f"   Total entries: {len(test_data)}")
    print(f"   Successful: {successful_entries}")
    print(f"   Failed: {failed_entries}")
    print(f"   Total processing time: {total_time:.2f} seconds")
    print(f"   Average time per entry: {avg_time_per_entry:.3f} seconds")
    print(f"   Processing rate: {entries_per_second:.2f} entries/second")
    
    if successful_entries > 0:
        print(f"\n🎯 Sample Results:")
        for i, result in enumerate(results[:3]):  # Show first 3 results
            if result['success']:
                title_short = result['job_title'][:40] + "..." if len(result['job_title']) > 40 else result['job_title']
                print(f"   {i+1}. '{title_short}' → SOC: {result['soc_code']}")
    
    if failed_entries > 0:
        print(f"\n❌ Failed Entries:")
        for result in results:
            if not result['success']:
                print(f"   - '{result['job_title'][:40]}...': {result.get('error', 'Unknown error')}")
    
    # Performance assertions
    assert total_time > 0, "Processing should take some measurable time"
    assert successful_entries > 0, "At least some entries should be processed successfully"
    assert entries_per_second > 0, "Should process at least some entries per second"
    
    # Log performance benchmark for future reference
    print(f"\n🏆 Performance Benchmark: {entries_per_second:.2f} entries/second")

def test_batch_vs_individual_performance(coder_instance, test_data):
    """Compare performance of batch processing vs individual calls."""
    # Limit to first 5 entries for this comparison test
    sample_data = test_data[:5]
    
    print(f"\n⚡ Batch vs Individual Performance Comparison ({len(sample_data)} entries):")
    
    # Test individual processing
    start_time = time.time()
    individual_results = []
    for title, description, sector in sample_data:
        result = coder_instance.codejobrow(title, description, sector)
        individual_results.append(result)
    individual_time = time.time() - start_time
    
    # For this library, there's no true batch processing, but we can measure
    # the overhead of multiple calls vs a theoretical optimized batch
    individual_rate = len(sample_data) / individual_time if individual_time > 0 else 0
    
    print(f"   Individual processing: {individual_time:.3f} seconds ({individual_rate:.2f} entries/sec)")
    print(f"   Average per entry: {individual_time/len(sample_data):.3f} seconds")
    
    # Note: This library processes one job at a time, so no true batch processing available
    print(f"   Note: This library processes jobs individually (no batch processing available)")
    
    assert individual_time > 0
    assert len(individual_results) == len(sample_data)

if __name__ == "__main__":
    # Allow running this test file directly for performance monitoring
    pytest.main([__file__, "-v", "-s"])
