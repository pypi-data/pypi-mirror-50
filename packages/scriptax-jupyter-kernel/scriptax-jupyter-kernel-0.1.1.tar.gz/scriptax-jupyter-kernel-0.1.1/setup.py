from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='scriptax-jupyter-kernel',
    packages=find_packages(),  # this must be the same as the name above
    version='0.1.1',
    description='Scriptax Jupyter kernel',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shawn Clake',
    author_email='shawn.clake@gmail.com',
    url='https://github.com/Apitax/Scriptax-Jupyter-Kernel',
    keywords=[],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'pytest',
        'scriptax-runtime==0.2.1',
        'jupyter_client',
        'IPython',
        'ipykernel'
    ],

)