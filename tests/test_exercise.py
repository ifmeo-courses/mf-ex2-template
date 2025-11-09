"""
Test file for Exercise 2: Bathymetry Mapping

This file contains automated tests to check student submissions.
Tests are run by GitHub Actions when students push their code.

IMPORTANT: This file tests the basic environment setup.
For detailed completion checking, see test_outputs.py
"""

import pytest
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import os


def test_imports_work():
    """Test that required packages can be imported."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import xarray as xr
        import netCDF4
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
    except ImportError as e:
        pytest.fail(f"Failed to import required package: {e}")


def test_notebook_exists():
    """Test that the assignment notebook exists."""
    notebook_path = Path("src/assignment.ipynb")
    assert notebook_path.exists(), "src/assignment.ipynb file not found"


def test_data_files_exist():
    """Test that required data files exist."""
    data_dir = Path("data")
    assert data_dir.exists(), "data directory not found"
    
    bathymetry_file = data_dir / "bathymetry_subset.nc"
    assert bathymetry_file.exists(), "bathymetry_subset.nc file not found in data directory"


def test_modules_exist():
    """Test that required modules exist."""
    modules_dir = Path("modules")
    assert modules_dir.exists(), "modules directory not found"
    
    bathymetry_module = modules_dir / "bathymetry.py"
    assert bathymetry_module.exists(), "bathymetry.py module not found"
    
    init_file = modules_dir / "__init__.py"
    assert init_file.exists(), "__init__.py not found in modules directory"


def test_bathymetry_data_loading():
    """Test that bathymetry data can be loaded and has expected structure."""
    if not Path("data/bathymetry_subset.nc").exists():
        pytest.skip("Bathymetry data file not found")
    
    # Test loading with xarray
    ds = xr.open_dataset("data/bathymetry_subset.nc")
    
    # Check required variables
    assert 'z' in ds.data_vars, "Depth variable 'z' not found in dataset"
    assert 'lat' in ds.coords, "Latitude coordinate not found"
    assert 'lon' in ds.coords, "Longitude coordinate not found"
    
    # Check data properties
    assert len(ds.lat) > 0, "No latitude data found"
    assert len(ds.lon) > 0, "No longitude data found"
    assert ds.z.size > 0, "No depth data found"
    
    # Check that depths are negative (below sea level)
    assert ds.z.max() <= 0, "Bathymetry depths should be negative (below sea level)"
    
    ds.close()


def test_basic_plotting_functions():
    """Test that basic plotting functionality works."""
    # Create sample bathymetry data for testing
    lats = np.linspace(63, 66, 50)
    lons = np.linspace(-35, -25, 80)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # Create synthetic bathymetry (negative depths)
    depths = -1000 - 500 * np.sin(lat_grid * np.pi / 180) * np.cos(lon_grid * np.pi / 180)
    
    # Test matplotlib contour plotting
    fig, ax = plt.subplots(figsize=(10, 8))
    contour = ax.contourf(lons, lats, depths, cmap='viridis')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Test Bathymetry Map')
    
    # Check that plot was created
    assert len(ax.collections) > 0, "No contour plot collections found"
    assert ax.get_xlabel() != '', "X-axis label not set"
    assert ax.get_ylabel() != '', "Y-axis label not set"
    assert ax.get_title() != '', "Title not set"
    
    plt.close(fig)


def test_cartopy_projection():
    """Test that cartopy projections work."""
    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        
        # Test creating a map with projection
        proj = ccrs.Mercator()
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': proj})
        
        # Add basic map features
        ax.coastlines(resolution='50m')
        ax.gridlines(draw_labels=True)
        
        # Check that the projection was set correctly
        assert hasattr(ax, 'projection'), "Axis doesn't have projection attribute"
        
        plt.close(fig)
        
    except ImportError:
        pytest.skip("Cartopy not available for testing")


def test_bathymetry_module_functions():
    """Test that bathymetry module functions work."""
    try:
        from modules.bathymetry import BathymetryDataSingleton, get_bathymetry_subset_data
        
        # Test singleton pattern
        singleton1 = BathymetryDataSingleton()
        singleton2 = BathymetryDataSingleton()
        assert singleton1 is singleton2, "Singleton pattern not working correctly"
        
    except ImportError:
        pytest.skip("Bathymetry module not available for testing")


def test_geographic_coordinates():
    """Test understanding of geographic coordinate systems."""
    # Test coordinate ranges for North Atlantic
    test_lats = np.array([63.0, 64.5, 66.0])
    test_lons = np.array([-35.0, -30.0, -25.0])
    
    # Check latitude range (should be positive for Northern Hemisphere)
    assert np.all(test_lats > 0), "Latitudes should be positive in Northern Hemisphere"
    assert np.all(test_lats < 90), "Latitudes should be less than 90°N"
    
    # Check longitude range (should be negative for Western Hemisphere)
    assert np.all(test_lons < 0), "Longitudes should be negative in Western Hemisphere"
    assert np.all(test_lons > -180), "Longitudes should be greater than -180°"


def test_ocean_depth_concepts():
    """Test understanding of bathymetry and ocean depth concepts."""
    # Typical ocean depth ranges
    shallow_water = -200  # Continental shelf
    deep_water = -3000   # Abyssal plains
    
    # Test depth conventions (negative below sea level)
    assert shallow_water < 0, "Ocean depths should be negative below sea level"
    assert deep_water < shallow_water, "Deep water should be more negative than shallow water"
    
    # Test realistic depth ranges
    depths = np.array([0, -50, -200, -1000, -3000])
    assert depths[0] >= depths[1] >= depths[2], "Depths should decrease with distance from shore"


if __name__ == "__main__":
    pytest.main([__file__])