# Exercise 2: Bathymetry Mapping

## Overview

This exercise teaches students to work with bathymetry data and create professional oceanographic maps using Python. Students will learn to visualize seafloor topography using both matplotlib and cartopy, and understand geographic coordinate systems and map projections.

## Learning Objectives

Students will:
- Load and manipulate bathymetry data using xarray and netCDF4
- Create contour plots of seafloor topography using matplotlib
- Generate cartographically accurate maps using cartopy and map projections
- Add geographic features, annotations, and proper styling to maps
- Understand ocean depth conventions and bathymetric data interpretation
- Apply appropriate color scales for oceanographic data visualization

## Required Packages

- matplotlib
- numpy
- xarray
- netCDF4
- cartopy (optional, for enhanced mapping)
- cmocean (optional, for better ocean color scales)

## Data Files

- `data/bathymetry_subset.nc`: Real ETOPO bathymetry data for the North Atlantic region
- `modules/bathymetry.py`: Helper functions for bathymetry data processing

## Expected Outputs

Students should generate three figures:
1. `ex2fig1-[StudentName]-Messfern.png`: Basic matplotlib contour map
2. `ex2fig2-[StudentName]-Messfern.png`: Cartopy map with geographic projection  
3. `ex2fig3-[StudentName]-Messfern.png`: Enhanced map with annotations and styling

## Assessment

- Data loading and manipulation (3 points)
- Figure 1: Basic matplotlib mapping (3 points)
- Figure 2: Cartopy projection mapping (3 points) 
- Figure 3: Enhanced map with annotations (5 points)
- Analysis questions (3 points)
- Code quality and documentation (1 point)

**Total: 18 points**

## Instructions for Instructors

This exercise uses real bathymetry data from ETOPO and includes a helper module for data processing. The exercise is designed to be completed in 2-3 hours and builds important skills for oceanographic data visualization.