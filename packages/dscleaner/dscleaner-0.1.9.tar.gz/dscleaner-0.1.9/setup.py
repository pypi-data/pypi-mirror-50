import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt","r") as req:
    inst_req = req.read()
setuptools.setup(
    name='dscleaner',
    version='0.1.9',
    author='Manuel Pereira',
    author_email='afonso.pereira4525@gmail.com',
    packages=['dscleaner',],
    project_urls={
        "Documentation": "https://dscleaner.rtfd.io/",
        "Source code": "https://gitlab.com/ManelPereira/dscleaner",
    },
    license='The MIT License',
    description='Added batch resample function to cli',
    long_description=long_description,
    install_requires=inst_req,
)