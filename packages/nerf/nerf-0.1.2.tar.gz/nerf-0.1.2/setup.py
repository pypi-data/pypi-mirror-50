from setuptools import setup, find_packages

setup(name="nerf",
      version='0.1.2',
      description='Second test version of NERF',
      keywords= ("random forest", "interpretation"),
      author="Yue Zhang",
      author_email="yue.zhang@lih.lu",
      packages=find_packages(),
      include_package_data=True,
      platforms="any",
      install_requires=["numpy", "pandas","networkx"]

)