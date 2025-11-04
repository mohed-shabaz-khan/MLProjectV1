from setuptools import setup, find_packages
setup(
    name='ml_date_classifier',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
    'numpy', 'pandas', 'scikit-learn', 'joblib', 'fastapi', 'uvicorn'
    ],
    python_requires='>=3.8'
)