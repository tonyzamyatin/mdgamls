## Setup
1. Create environment and install packages: `conda env create -f environment.yml`
2. Activate environment: `conda activate tu_mdg`
3. Open project in PyCharm IDE (download from [JetBrains Toolbox](https://www.jetbrains.com/de-de/toolbox-app/))
4. Open a Juypter notebook (`*.ipynb` file extension))
5. Execute any code cell and PyCharm should take care of starting the Jupyter server in the background

## Juypter Notebook in PyCharm (all you need to know)
- Always execute the first cell with all the imports first
- It is not possible to run multiple notebooks simultaneously. If you execute a code cell from another notebook, the automatically managed Jupyter server will likely crash. To execute a different notebook:
    1. Navigate to the Jupyter server tab in PyCharm (bottom left corner in the side bar)
    2. First Stop the Jupyter server (press the red stop button)
    3. Restart the Jupyter server (press the green start button)
    4. Execute code cells in the other notebook you want to run
- Restarting the Jupyter server will wipe the memory of the server, meaining that all cells have to be executed again every time you work on a notebook.
