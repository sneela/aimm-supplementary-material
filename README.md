# Supplementary Scripts

This directory contains utility scripts designed to support reproducibility, validation, and educational understanding of the AIMM framework. All scripts are non-proprietary and released for public use.

## Purpose

The supplementary scripts serve three primary functions:

### 1. Schema Validation
Scripts that validate data structure and consistency across datasets and intermediate outputs. These ensure that computed metrics conform to expected formats and that evaluation pipelines receive properly formatted inputs.

### 2. Metrics Computation
Standalone utilities for calculating evaluation metrics, statistical measures, and performance summaries. These can be run independently on validation data to verify metric computation logic outside the main evaluation pipeline.

### 3. Illustrative Demonstration
Scripts that demonstrate core concepts using synthetic, toy data. These are designed for educational purposes—to illustrate how data flows through processing stages and how different components interact—without relying on proprietary models or real market data.

## What Is Not Included

For intellectual property protection and licensing reasons, the following are intentionally excluded:

- **The AIMM Model**: The core attention-based forecasting architecture and its trained weights
- **Feature Engineering Pipeline**: Proprietary feature construction and transformation logic
- **Labels and Ground Truth**: Real market data, price targets, and actual trading signals
- **Hyperparameter Thresholds**: Model-specific tuning parameters and decision boundaries
- **Training Code**: Model training loops, loss functions, and optimization procedures
- **Deployment Infrastructure**: Production serving, API handlers, and monitoring systems

## Non-Proprietary Release

All scripts in this directory are intentionally written to be:
- **Self-contained**: No dependencies on proprietary code or internal systems
- **Reproducible**: Can be executed by third parties with only publicly available Python packages
- **Educational**: Demonstrate concepts without exposing core intellectual property
- **Safe for Publication**: Contain no sensitive information, credentials, or proprietary algorithms

## Toy Data in `toy_demo.py`

The `toy_demo.py` script (if present) uses purely **synthetic data** generated within the script itself. No real market data, actual predictions, or proprietary signals are included. This allows users to understand the structure and flow of computations in a controlled environment.

## Usage

Each script should be run with appropriate documentation and Python dependencies installed. Refer to individual script docstrings and the main project README for dependency installation instructions.

## Citation and Academic Use

These supplementary materials are provided to support research and reproducibility efforts for the AIMM framework. If you use these scripts, extend the evaluation methodology, or compare against the AIMM framework in your work, please cite the associated arXiv paper:

**arXiv Link**: https://arxiv.org/abs/2512.16103

### BibTeX Citation

```bibtex
@misc{neela2025aimmaidrivenmultimodalframework,
      title={AIMM: An AI-Driven Multimodal Framework for Detecting Social-Media-Influenced Stock Market Manipulation},
      author={Sandeep Neela},
      year={2025},
      eprint={2512.16103},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2512.16103},
}
```

### When to Cite

Please cite the AIMM paper if your work:
- Uses or builds upon these supplementary materials
- Compares against the AIMM framework or its evaluation methodology
- Extends the evaluation methodology, risk-scoring concept, or metrics presented here

If these materials are used in academic publications, benchmarks, or derivative research, citation of the AIMM paper is expected.

---

## Running the Supplementary Scripts

The scripts provided in this repository are lightweight, self-contained, and
intended for illustration and interface validation only.

They can be executed using a standard Python 3.9+ environment. No proprietary
models, datasets, or external services are required.

Example:
```bash
python scripts/validate_inputs.py
python scripts/validate_outputs.py
python scripts/compute_metrics.py
python scripts/toy_demo.py

**Note**: These supplementary scripts are provided to facilitate academic understanding and reproducibility verification. For questions about the AIMM framework's core methodology, please refer to the main project documentation.
