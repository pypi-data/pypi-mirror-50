import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
                 name="COCOPLOTS",
                 version="1.0.7",
                 author="A.G.M. Pietrow, G.J.M. Vissers, C. Robustini, M.K. Druett",
                 author_email="Alex.pietrow@astro.su.se",
                 description="COlor COllapsed Plotting software",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/mdruett/COCOPLOT/tree/master/Python",
                 packages=setuptools.find_packages(),
                 classifiers=[
                              "Programming Language :: Python :: 2.7",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              ],
                 )
