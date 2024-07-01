from setuptools import setup, find_packages

setup(
    name="test",
    version="0.0.0",
    packages=find_packages(),
    install_requires=["llvmlite"],
    entry_points="""
    [console_scripts]
    test=finn:finn
    """
)