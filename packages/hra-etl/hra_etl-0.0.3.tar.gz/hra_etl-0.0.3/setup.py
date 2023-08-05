import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hra_etl",
    version="0.0.3",
    author="Gyanendra Kumar Patro",
    author_email="gyanendrapatro02@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.dell.com/corporate/hr-data-lake/ETL/etl-architecture",
    packages=setuptools.find_packages(),
    keywords = ['ETL', 'PYTHONETL','PYTHON'],   # Keywords that define your package best
    install_requires=['pyodbc','pandas','gnupg','chardet','threading','shutil','logging','datetime','configparser','subprocess','csv'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
