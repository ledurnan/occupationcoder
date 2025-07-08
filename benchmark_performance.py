#!/usr/bin/env python3
"""
Performance monitoring script for occupationcoder library.
Run this script to get a quick performance benchmark.
"""

import time
import sys
import os

# Add the current directory to the path so we can import the library
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from occupationcoder.coder import coder

def benchmark_performance():
    """Run a quick performance benchmark."""
    print("🚀 OccupationCoder Performance Benchmark")
    print("=" * 50)
    
    # Initialize coder
    print("Initializing coder...")
    c = coder.Coder()
    
    # Test cases
    test_jobs = [
        ("Software Engineer", "Develop applications using Python and JavaScript", "Technology"),
        ("Data Scientist", "Analyze large datasets and build machine learning models", "Technology"),  
        ("Teacher", "Educate students in mathematics and science", "Education"),
        ("Nurse", "Provide healthcare services to patients", "Healthcare"),
        ("Accountant", "Manage financial records and prepare tax returns", "Finance"),
    ]
    
    print(f"\nTesting with {len(test_jobs)} sample job entries...")
    
    # Warm-up run (first run is often slower due to initialization)
    print("Performing warm-up run...")
    c.codejobrow("Test Job", "Test description", "Test sector")
    
    # Actual benchmark
    print("\nRunning performance benchmark...")
    start_time = time.time()
    
    results = []
    for i, (title, description, sector) in enumerate(test_jobs, 1):
        print(f"  Processing job {i}/{len(test_jobs)}: {title}")
        
        job_start = time.time()
        try:
            result = c.codejobrow(title, description, sector)
            job_time = time.time() - job_start
            soc_code = result['SOC_code'].iloc[0] if result is not None else 'ERROR'
            
            results.append({
                'title': title,
                'soc_code': soc_code,
                'time': job_time,
                'success': True
            })
            print(f"    → SOC: {soc_code} (took {job_time:.2f}s)")
            
        except Exception as e:
            job_time = time.time() - job_start
            results.append({
                'title': title,
                'soc_code': 'ERROR',
                'time': job_time,
                'success': False,
                'error': str(e)
            })
            print(f"    → ERROR: {e} (took {job_time:.2f}s)")
    
    total_time = time.time() - start_time
    
    # Calculate metrics
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    avg_time = total_time / len(test_jobs)
    entries_per_second = len(test_jobs) / total_time
    
    # Display results
    print("\n" + "=" * 50)
    print("📊 PERFORMANCE RESULTS")
    print("=" * 50)
    print(f"Total jobs processed: {len(test_jobs)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per job: {avg_time:.2f} seconds")
    print(f"Processing rate: {entries_per_second:.2f} jobs/second")
    
    print(f"\n🎯 DETAILED RESULTS:")
    for result in results:
        status = "✅" if result['success'] else "❌"
        title_short = result['title'][:30] + "..." if len(result['title']) > 30 else result['title']
        print(f"{status} {title_short:<35} → {result['soc_code']:<6} ({result['time']:.2f}s)")
    
    if failed > 0:
        print(f"\n❌ ERRORS:")
        for result in results:
            if not result['success']:
                print(f"   {result['title']}: {result.get('error', 'Unknown error')}")
    
    # Performance rating
    print(f"\n🏆 PERFORMANCE RATING:")
    if entries_per_second > 1.0:
        rating = "🚀 Excellent"
    elif entries_per_second > 0.5:
        rating = "👍 Good"
    elif entries_per_second > 0.2:
        rating = "👌 Acceptable"
    else:
        rating = "🐌 Slow"
    
    print(f"   {rating} ({entries_per_second:.2f} jobs/second)")
    
    print(f"\n💡 SYSTEM INFO:")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   Platform: {sys.platform}")
    
    return {
        'total_jobs': len(test_jobs),
        'successful': successful,
        'failed': failed,
        'total_time': total_time,
        'avg_time': avg_time,
        'entries_per_second': entries_per_second,
        'results': results
    }

if __name__ == "__main__":
    try:
        benchmark_performance()
    except KeyboardInterrupt:
        print("\n\n⏹️  Benchmark interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Benchmark failed: {e}")
        sys.exit(1)
