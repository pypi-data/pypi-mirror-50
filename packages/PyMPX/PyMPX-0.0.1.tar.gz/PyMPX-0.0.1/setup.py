from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()
    
setup(
    name="PyMPX",
    version="0.0.1",
    author="Metapraxis Ltd.",
    author_email="pympx@metapraxis.com",
    description="Metapraxis Empower python driver",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    project_urls={"Documentation":"https://api.metapraxis.com/python/current"},
    packages=find_packages(),
    #package_dir={'':r'pympx/importer_scripts'},   # tell distutils where the importer scripts distributed with this package are kept
    include_package_data=True,
    #####eager_resources=['pympx/importer_scripts/*.eimp'],
    #data_files = [('export_all_eimp', ['eimp/index.html'])],
    #package_data={
    #    # If any package contains empower importer files, include them:
    #    'export_all_eimp': ['importer_scripts/ExportAllDimensionElements.eimp'],
    #},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Office/Business :: Financial"
    ],
    zip_safe=False,
)
