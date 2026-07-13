from setuptools import setup, find_packages

setup(
    name="ai-trader-pro-x",
    version="1.0.0",
    description="KI-gestützter Trading Bot für MetaTrader 5",
    author="WarhammerPIOG",
    author_email="your-email@example.com",
    url="https://github.com/WarhammerPIOG/AI-Trader-Pro-X",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "MetaTrader5>=5.0.45",
        "pandas>=2.2.0",
        "numpy>=1.26.4",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "sqlalchemy>=2.0.23",
        "python-telegram-bot>=20.4",
        "python-dotenv>=1.0.0",
        "scikit-learn>=1.4.1",
        "xgboost>=2.0.3",
    ],
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
)
