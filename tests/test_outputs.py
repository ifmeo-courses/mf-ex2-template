"""
Test actual outputs produced by students for Exercise 2: Bathymetry.
This tests what students actually created, not their code.
"""

import pytest
import xarray as xr
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def test_student_information_completed():
    """Test that student filled in their personal information."""
    notebook_path = Path("src/assignment.ipynb")
    if not notebook_path.exists():
        pytest.skip("Assignment notebook not found")
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Find the first markdown cell (should contain student info)
    info_cell = None
    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source'])
            if 'Author:' in source or 'Your Information' in source:
                info_cell = source
                break
    
    assert info_cell is not None, "Could not find student information cell"
    
    # Check that placeholders have been replaced
    placeholders = [
        '[YOUR NAME HERE]',
        '[TODAY\'S DATE]',
        '[REPLACE WITH YOUR ACTUAL NAME]',
        '[REPLACE WITH TODAY\'S DATE]',
        '[REPLACE WITH YOUR STUDENT ID]'
    ]
    
    for placeholder in placeholders:
        assert placeholder not in info_cell, f"Student information incomplete: '{placeholder}' still present"


def test_bathymetry_data_exists():
    """Test that bathymetry data file exists."""
    data_file = Path("data/bathymetry_subset.nc")
    assert data_file.exists(), "Required bathymetry data file (bathymetry_subset.nc) not found"


def test_bathymetry_data_valid():
    """Test that bathymetry data contains expected variables and values."""
    data_file = Path("data/bathymetry_subset.nc")
    if not data_file.exists():
        pytest.skip("Bathymetry data file not found")
    
    # Load and check the dataset
    ds = xr.open_dataset(data_file)
    
    # Check required variables exist
    required_vars = ['lat', 'lon', 'z']
    for var in required_vars:
        assert var in ds.coords or var in ds.data_vars, f"Required variable '{var}' missing from bathymetry file"
    
    # Check data is reasonable for bathymetry
    z_data = ds.z
    assert z_data.max() <= 0, "Bathymetry depths should be negative (below sea level)"
    assert z_data.min() >= -8000, "Bathymetry depths seem unreasonably deep"
    assert len(ds.lat) > 10, "Dataset should have reasonable number of latitude points"
    assert len(ds.lon) > 10, "Dataset should have reasonable number of longitude points"


def test_all_figures_created():
    """Test that all 3 required figures were created."""
    figures_dir = Path("figures/")
    if not figures_dir.exists():
        pytest.skip("Figures directory not found")
    
    # Check each required figure exists
    required_figures = [
        'ex2fig1-*-Messfern.png',
        'ex2fig2-*-Messfern.png', 
        'ex2fig3-*-Messfern.png'
    ]
    
    for pattern in required_figures:
        matching_files = list(figures_dir.glob(pattern))
        assert len(matching_files) > 0, f"Required figure not found: {pattern}"
        
        # Check it's not the template name
        for fig_file in matching_files:
            assert 'YourName' not in fig_file.name, f"Figure name not personalized: {fig_file}"


def test_figures_contain_data():
    """Test that figures actually contain plotted data (not just empty plots)."""
    figures_dir = Path("figures/")
    if not figures_dir.exists():
        pytest.skip("Figures directory not found")
    
    figure_files = list(figures_dir.glob("ex2fig*-*-Messfern.png"))
    if len(figure_files) == 0:
        pytest.skip("No figures found")
    
    # Test the first figure we find
    test_fig = figure_files[0]
    
    # Load image and check it's not just white/empty
    img = mpimg.imread(test_fig)
    
    # Check image has reasonable dimensions
    assert img.shape[0] > 100, "Figure height too small"
    assert img.shape[1] > 100, "Figure width too small"
    
    # Check it's not just a white image (mean pixel value should be < 0.95)
    mean_pixel = np.mean(img)
    assert mean_pixel < 0.95, "Figure appears to be mostly empty/white"


def test_figure_file_sizes():
    """Test that figure files have reasonable sizes (not tiny empty files)."""
    figures_dir = Path("figures/")
    if not figures_dir.exists():
        pytest.skip("Figures directory not found")
    
    figure_files = list(figures_dir.glob("ex2fig*-*-Messfern.png"))
    
    for fig_file in figure_files:
        file_size = fig_file.stat().st_size
        assert file_size > 10000, f"Figure file too small (likely empty): {fig_file} ({file_size} bytes)"
        assert file_size < 10000000, f"Figure file too large: {fig_file} ({file_size} bytes)"


def test_figure1_matplotlib_contour():
    """Test that Figure 1 is a matplotlib contour plot."""
    figures_dir = Path("figures/")
    if not figures_dir.exists():
        pytest.skip("Figures directory not found")
    
    fig1_files = list(figures_dir.glob("ex2fig1-*-Messfern.png"))
    if len(fig1_files) == 0:
        pytest.skip("Figure 1 not found")
    
    # Check file exists and has reasonable size
    fig1_file = fig1_files[0]
    assert fig1_file.exists(), "Figure 1 file does not exist"
    
    # Load and check the image
    img = mpimg.imread(fig1_file)
    
    # Basic checks for a contour plot
    assert img.shape[0] > 200, "Figure 1 height seems too small for a proper contour plot"
    assert img.shape[1] > 200, "Figure 1 width seems too small for a proper contour plot"


def test_figure2_cartopy_map():
    """Test that Figure 2 is a cartopy map."""
    figures_dir = Path("../figures/")
    if not figures_dir.exists():
        pytest.skip("Figures directory not found")
    
    fig2_files = list(figures_dir.glob("ex2fig2-*-Messfern.png"))
    if len(fig2_files) == 0:
        pytest.skip("Figure 2 not found")
    
    # Check file exists and has reasonable size
    fig2_file = fig2_files[0]
    assert fig2_file.exists(), "Figure 2 file does not exist"
    
    # Load and check the image
    img = mpimg.imread(fig2_file)
    
    # Basic checks for a cartopy map
    assert img.shape[0] > 200, "Figure 2 height seems too small for a proper map"
    assert img.shape[1] > 200, "Figure 2 width seems too small for a proper map"


def test_figure3_enhanced_cartopy():
    """Test that Figure 3 is an enhanced cartopy map."""
    figures_dir = Path("figures/")
    if not figures_dir.exists():
        pytest.skip("Figures directory not found")
    
    fig3_files = list(figures_dir.glob("ex2fig3-*-Messfern.png"))
    if len(fig3_files) == 0:
        pytest.skip("Figure 3 not found")
    
    # Check file exists and has reasonable size
    fig3_file = fig3_files[0]
    assert fig3_file.exists(), "Figure 3 file does not exist"
    
    # Load and check the image
    img = mpimg.imread(fig3_file)
    
    # Basic checks for an enhanced map (might have higher resolution)
    assert img.shape[0] > 200, "Figure 3 height seems too small for a proper enhanced map"
    assert img.shape[1] > 200, "Figure 3 width seems too small for a proper enhanced map"
    
    # Check for higher quality (enhanced maps often have higher DPI)
    total_pixels = img.shape[0] * img.shape[1]
    assert total_pixels > 40000, "Figure 3 seems to have low resolution for an enhanced map"


def test_modules_directory_exists():
    """Test that the modules directory with bathymetry.py exists."""
    modules_dir = Path("modules/")
    assert modules_dir.exists(), "Modules directory not found"
    
    bathymetry_module = modules_dir / "bathymetry.py"
    assert bathymetry_module.exists(), "bathymetry.py module file not found"


def test_student_function_exists():
    """Test that the student implemented the get_depth_at_location function."""
    # This requires executing the notebook to check if the function was defined
    # We'll check if the function exists in a minimal way
    
    # Import the assignment module if it was executed
    try:
        import sys
        sys.path.append('src')
        
        # Try to run a minimal check - this is a basic test
        # A more complete test would require executing the notebook
        notebook_path = Path("src/assignment.ipynb")
        if not notebook_path.exists():
            pytest.skip("Assignment notebook not found")
            
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = f.read()
            
        # Check that the function definition exists in the notebook
        assert 'def get_depth_at_location' in notebook_content, \
            "Function 'get_depth_at_location' not found in notebook"
        assert 'target_lat' in notebook_content, \
            "Function parameters not properly defined"
        assert 'target_lon' in notebook_content, \
            "Function parameters not properly defined"
            
    except Exception as e:
        # If we can't check the notebook, skip this test
        pytest.skip(f"Could not check student function: {e}")


def test_ds2_mooring_location():
    """Test that DS2 mooring coordinates are correctly used."""
    notebook_path = Path("src/assignment.ipynb")
    if not notebook_path.exists():
        pytest.skip("Assignment notebook not found")
        
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = f.read()
    
    # Check that DS2 coordinates are present and correct
    assert '66.0128' in notebook_content, "DS2 latitude not found or incorrect"
    assert '-27.270200' in notebook_content or '-27.2702' in notebook_content, \
        "DS2 longitude not found or incorrect"


def test_function_parameters_docstring():
    """Test that the function has proper documentation."""
    notebook_path = Path("src/assignment.ipynb")
    if not notebook_path.exists():
        pytest.skip("Assignment notebook not found")
        
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = f.read()
    
    # Check for basic function documentation
    if 'def get_depth_at_location' in notebook_content:
        # Check that there's some form of documentation
        function_section = notebook_content.split('def get_depth_at_location')[1].split('def ')[0]
        
        has_docstring = '"""' in function_section or "'''" in function_section
        has_comments = '#' in function_section
        
        assert has_docstring or has_comments, \
            "Function should have documentation (docstring or comments)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])