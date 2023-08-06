import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="worksheet",
    version="0.0.1-alpha.0",
    entry_points="""
        [console_scripts]
        worksheet=main:cli
    """,
    install_requires=["SQLAlchemy", "tabulate", "Click", "xdg"],
    author="Dongsheng Cai",
    author_email="d@tux.im",
    classifiers=[],
    description="Time tracking tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/dcai/worksheet",
)
