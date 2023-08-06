import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bomdia",
    version="0.0.1",
    author="Rafael Rayes",
    author_email="rafa@rayes.com.br",
    description="Pacote que te fala bom dia",
    long_description='Pacote que te fala bom dia',

    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

