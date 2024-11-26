## Approach
1. Implement the functions in seperate `.py` files named `partX.py`,
2. Call the functions in the notebook `solution.ipynb`,
3. Then do all the printing and visualization in the notebook,
4. Finally, answer the questions (a-f) and document your thoughts in the notebook.

When we're finished with all parts of the assignment we can use the `nbconvert` library to convert the Jupyter notebook to a PDF for us.
1. Start Jupyter server with 
   ```
   jupyter notebook --no-browser
   ```
2. Tag cells to exclude from PDF with `exclude`-tag. In PyCharm: Right-click on cell -> Add Cell Tag -> enter "exclude"
3. Execute all cells, so that the output will be visible in the PDF
4. Convert the notebook to a PDF be running
    ```
    jupyter nbconvert solution.ipynb --to pdf --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="['exclude']"
    ```