import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()

files = ["utils/templating/templates/base/*"]

setuptools.setup(
    name='reportlib',
    version='3.1.2',
    author="nhat.nv",
    author_email="nhat.nv@teko.vn",
    description="Generator HTML from pandas via Jinja2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.teko.vn/data/libs/reportlib",
    packages=setuptools.find_packages(),
    package_data={'reportlib': files},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
)
