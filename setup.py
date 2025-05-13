from setuptools import setup, find_packages

setup(
    name="dst_airlines",
    version="1.1.0",
    author="Sanou",
    packages=find_packages(),
    install_requires=[
        "colorlog>=6.7.0",
        # Ajoutez ici vos autres dépendances
    ],
    python_requires=">=3.7",
)
