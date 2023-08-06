# @Author: yican.kz
# @Date: 2019-08-02 11:41:33
# @Last Modified by:   yican.kz
# @Last Modified time: 2019-08-02 11:41:33

from __future__ import absolute_import
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torch_buddy",
    version="0.0.5",
    author="鲲(China)",
    author_email="972775099@qq.com",
    description="pytorch toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NickYi1990/torch_buddy",
    install_requires=["pandas-summary>=0.0.5"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
