from setuptools import setup, find_packages

setup(
    name="stock-valuation-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.30.0",
        "numpy>=1.26.0",
        "plotly>=5.15.0",
        "pandas>=2.1.0",
        "scikit-learn>=1.3.0",
    ],
)
