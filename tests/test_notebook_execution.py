"""
Test that the student's assignment notebook executes without errors and 
that their get_depth_at_location function works correctly.

This test runs the entire notebook and verifies:
- No syntax errors
- No runtime errors  
- All code cells execute successfully
- The student's function returns correct depths at known locations
"""

import pytest
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path
import tempfile
import shutil
import re


def test_notebook_executes_without_errors():
    """Test that the assignment notebook runs completely without errors."""
    notebook_path = Path("../src/assignment.ipynb")
    assert notebook_path.exists(), "Assignment notebook not found"
    
    # Load the notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    # Create a temporary directory for execution
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Copy notebook to temp directory
        temp_notebook = temp_path / "assignment.ipynb"
        with open(temp_notebook, 'w') as f:
            nbformat.write(nb, f)
        
        # Copy required files
        for src_dir in ["data", "modules"]:
            src_path = Path(f"../{src_dir}")
            if src_path.exists():
                dst_path = temp_path / src_dir
                shutil.copytree(src_path, dst_path)
        
        # Create figures directory
        figures_dir = temp_path / "figures"
        figures_dir.mkdir(exist_ok=True)
        
        # Execute the notebook
        ep = ExecutePreprocessor(timeout=300, kernel_name='python3')
        
        try:
            ep.preprocess(nb, {'metadata': {'path': str(temp_path)}})
            print("✓ Notebook executed successfully")
        except Exception as e:
            pytest.fail(f"Notebook execution failed: {str(e)}")


def test_function_works_correctly():
    """Test that the student's get_depth_at_location function returns correct depths."""
    notebook_path = Path("../src/assignment.ipynb")
    if not notebook_path.exists():
        pytest.skip("Assignment notebook not found")
    
    # Load and execute notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Setup temporary environment
        temp_notebook = temp_path / "assignment.ipynb"
        with open(temp_notebook, 'w') as f:
            nbformat.write(nb, f)
        
        # Copy required files
        for src_dir in ["data", "modules"]:
            src_path = Path(f"../{src_dir}")
            if src_path.exists():
                shutil.copytree(src_path, src_path.name, dirs_exist_ok=True)
        
        (temp_path / "figures").mkdir(exist_ok=True)
        
        # Execute notebook
        ep = ExecutePreprocessor(timeout=300, kernel_name='python3')
        
        try:
            ep.preprocess(nb, {'metadata': {'path': str(temp_path)}})
            
            # Extract the final execution namespace to test the function
            # We'll do this by adding a test cell and executing it
            test_code = '''
# Test the student's function with known locations
test_locations = [
    (64.51, -30.00, -2246.5, 50.0, "Center of domain"),
    (65.79, -25.01, -68.1, 20.0, "Shallowest area"),  
    (63.06, -32.84, -2893.3, 50.0, "Deepest area"),
    (66.00, -35.00, -326.6, 50.0, "Northwest region"),
    (63.01, -25.01, -546.1, 50.0, "Southeast region")
]

function_test_results = []

if 'get_depth_at_location' in locals() and callable(get_depth_at_location):
    for lat, lon, expected_depth, tolerance, description in test_locations:
        try:
            actual_depth = get_depth_at_location(bathymetry_subset, lat, lon)
            depth_diff = abs(actual_depth - expected_depth)
            
            if depth_diff <= tolerance:
                function_test_results.append(f"PASS: {description}")
            else:
                function_test_results.append(f"FAIL: {description} - expected {expected_depth:.1f}m, got {actual_depth:.1f}m")
        except Exception as e:
            function_test_results.append(f"ERROR: {description} - {str(e)}")
else:
    function_test_results.append("ERROR: get_depth_at_location function not found or not callable")

print("Function test results:", function_test_results)
'''
            
            # Add test cell and execute it
            test_cell = nbformat.v4.new_code_cell(test_code)
            nb.cells.append(test_cell)
            
            ep.preprocess(nb, {'metadata': {'path': str(temp_path)}})
            
            # Check the results from the test cell
            if nb.cells[-1].outputs:
                for output in nb.cells[-1].outputs:
                    if output.output_type == 'stream' and 'Function test results:' in output.text:
                        results_text = output.text
                        
                        # Verify that all tests passed
                        if 'ERROR:' in results_text:
                            pytest.fail(f"Function has errors: {results_text}")
                        elif 'FAIL:' in results_text:
                            pytest.fail(f"Function returns incorrect values: {results_text}")
                        else:
                            print("✓ Student function works correctly at all test locations")
                            return
            
            pytest.fail("Could not verify function test results")
            
        except Exception as e:
            pytest.fail(f"Failed to test student function: {str(e)}")


def test_function_exists_and_callable():
    """Test that the student defined a callable get_depth_at_location function."""
    notebook_path = Path("../src/assignment.ipynb")
    if not notebook_path.exists():
        pytest.skip("Assignment notebook not found")
    
    with open(notebook_path) as f:
        notebook_content = f.read()
    
    # Check that function is defined
    function_pattern = r'def\s+get_depth_at_location\s*\('
    assert re.search(function_pattern, notebook_content), "get_depth_at_location function not defined"
    
    # Check that NotImplementedError was removed from function
    # Find the function definition
    lines = notebook_content.split('\n')
    in_function = False
    function_lines = []
    
    for line in lines:
        if 'def get_depth_at_location' in line:
            in_function = True
        elif in_function and line.strip().startswith('def '):
            break  # Next function started
        elif in_function:
            function_lines.append(line)
    
    function_body = '\n'.join(function_lines)
    assert 'NotImplementedError' not in function_body, "Function still contains NotImplementedError - not implemented"
    
    print("✓ Function is properly defined and implemented")


def test_notebook_removes_notimplementederror():
    """Test that student removed all NotImplementedError statements."""
    notebook_path = Path("../src/assignment.ipynb")
    if not notebook_path.exists():
        pytest.skip("Assignment notebook not found")
    
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    # Check that no code cells contain NotImplementedError
    remaining_errors = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and 'NotImplementedError' in cell.source:
            remaining_errors.append(f"Cell {i+1}")
    
    assert len(remaining_errors) == 0, f"NotImplementedError still present in cells: {', '.join(remaining_errors)}"
    print("✓ All NotImplementedError statements removed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])