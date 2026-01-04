# Evaluating Internal Representation Metrics for Dimensionality Reduction

This project evaluates two internal representation metrics (RankMe and CLID) on three dimensionality reduction methods (PCA, t-SNE, UMAP) across four benchmark datasets.

## Project Structure

- `report.pdf` - Final research report (12 pages)
- `report.tex` - LaTeX source for the report
- `evaluation.ipynb` - Jupyter notebook with all experiments and analysis
- `evaluation_collapsible.html` - HTML export of the notebook
- `transfer.py` - Data transfer utility script

### Results Directories

- `Wine/` - Results for Wine dataset (3 classes, 178 samples)
- `Breast_Cancer/` - Results for Breast Cancer dataset (2 classes, 569 samples)
- `Digits/` - Results for Digits dataset (10 classes, 1797 samples)
- `Olivetti_Faces/` - Results for Olivetti Faces dataset (40 classes, 400 samples)

Each directory contains:
- Correlation analysis plots
- Scatter plots for RankMe and CLID metrics
- Within-method correlation visualizations

## Key Findings

1. **RankMe is reliable for PCA**: Strong positive correlation across all datasets (ρ=0.737–0.996, p<0.005)
2. **Nonlinear methods show complex patterns**: t-SNE exhibits negative correlations, UMAP varies by dataset
3. **CLID performance degrades with class complexity**: Effective for 3 classes (Wine, ρ=0.88) but fails with 10-40 classes

## Requirements

### Python Dependencies
- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn
- scipy
- umap-learn

### LaTeX
- TinyTeX or full TeX Live distribution
- Required packages: amsmath, graphicx, booktabs, hyperref, float

## Running the Analysis

1. Open `evaluation.ipynb` in Jupyter
2. Configure experiment parameters in the first cell:
   - `RANDOM_STATE_LIST`: Random seeds for reproducibility (12 seeds used)
   - `DATASET_N_CLUSTERS`: Dataset-specific cluster counts
3. Run all cells to reproduce the analysis

## Compilation

To compile the PDF report:
```bash
cd "Evaluating representations"
latexmk -pdf report.tex
```

## Author

Liuxi Mei  
Department of Computer and Information Science  
Linköping University  
liume102@student.liu.se

## Date

January 2026
