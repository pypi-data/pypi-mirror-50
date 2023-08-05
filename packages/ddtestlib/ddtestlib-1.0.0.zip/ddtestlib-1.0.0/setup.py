
# from distutils.core import setup
from setuptools import setup

def readme_file():
      with open("README.rst",encoding="utf-8") as rf:
            return rf.read()

setup(name="ddtestlib", version="1.0.0", description="this is a niubi lib",
      packages=["ddtestlib"], py_modules=["Tool"], author="dd", author_email="3425296552@qq.com",
      long_description=readme_file(),
      url="https://github.com/dongdong2019/Python_code", license="MIT")