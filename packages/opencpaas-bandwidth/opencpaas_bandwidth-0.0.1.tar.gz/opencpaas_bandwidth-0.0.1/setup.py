import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opencpaas_bandwidth",
    version="0.0.1",
    author="Perri Smith",
    author_email="dx@bandwidth.com",
    description="A Bandwidth implementation of OpenCpaas, an SDK that allows flexibility between CPaaS providers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bandwidth/OpenCpaas/",
    packages=['opencpaas_bandwidth'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
