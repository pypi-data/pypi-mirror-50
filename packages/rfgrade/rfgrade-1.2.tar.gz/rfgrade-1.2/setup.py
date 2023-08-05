from setuptools import setup

setup(
    name="rfgrade",
    version="1.2",
    description="grader for rf",
    author="refactored",
    author_email="refactored@colaberry.com",
    install_requires=['numpy', 'pandas', 'seaborn'],
    packages=["rfgrade"],
    zip_safe=False,
)
