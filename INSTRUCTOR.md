INSTRUCTOR NOTES
================

Maintainers: small reminders for keeping this template working for students and the autograder.

- When you update Python package dependencies, update both:
  - `requirements.txt` (pip installs used by student repos and CI)
  - `environment.yml` (conda-forge packages for reliable binary dependencies)

If you add packages that require compiled system libraries (e.g., `cartopy`, `netcdf4`, `proj`), prefer adding them to `environment.yml` under `dependencies` so conda provides prebuilt binaries.

Ensure `environment.yml` references the correct relative path to `requirements.txt` (currently `- -r requirements.txt`) and that `requirements.txt` is present in the template root.

- Kernel registration: after students create the environment, they may need to register the kernel so VS Code and Jupyter find it. A recommended command (students can run this in the activated environment):

```bash
python -m pip install --upgrade pip ipykernel
python -m ipykernel install --user --name=messfern_env --display-name "Python (messfern_env)"
```

- Use `mamba` for fast, reliable conda installs in CI and for students where available:

```bash
mamba env create -f environment.yml
```

If you want, I can add a short test script that validates the environment by attempting simple imports (numpy, xarray, gsw, netCDF4) to be used during CI or as a local check. Ask and I will add it.
