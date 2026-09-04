from setuptools import setup, find_packages

setup(
    name="commerceiq-analytics",
    version="1.0.0",
    description="CommerceIQ E-Commerce Analytics Platform",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.15.0",
        "streamlit>=1.30.0",
        "scipy>=1.11.0",
        "pyarrow>=14.0.0",
        "huggingface-hub>=0.20.0",
    ],
)
