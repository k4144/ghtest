import os
from pathlib import Path
from ghtest.scanner import scan_python_functions

def test_scan_python_functions():
    # Use the testdata directory for testing
    testdata_dir = Path(__file__).parent.parent / "testdata"
    
    # Ensure testdata exists
    assert testdata_dir.exists(), "testdata directory not found"
    
    functions = scan_python_functions(str(testdata_dir))
    
    # Check that we found some functions
    assert len(functions) > 0
    
    # Check for specific functions we know exist in gh_api.py
    qualnames = [f.qualname for f in functions]
    assert "get_commits" in qualnames
    assert "get_repo_data" in qualnames
    assert "create_repo" in qualnames
    
    # Check details of a specific function
    get_commits = next(f for f in functions if f.qualname == "get_commits")
    assert get_commits.module == "gh_api"
    param_names = [p.name for p in get_commits.parameters]
    assert "name" in param_names
    assert "dry_run" in param_names
