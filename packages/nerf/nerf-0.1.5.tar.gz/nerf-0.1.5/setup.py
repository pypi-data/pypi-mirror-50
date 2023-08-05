from setuptools import setup, find_packages

setup(name="nerf",
      version='0.1.5',
      description='Second test version of NERF',
      long_description='NERF is an interpretation tool for scikit-learn built random forest models'
                       'NERF is designed to capture synergy effect between biological molecule.',
      keywords= ("random forest", "interpretation"),
      author="Yue Zhang",
      author_email="yue.zhang@lih.lu",
      packages=find_packages(),
      include_package_data=True,
      platforms="any",
      install_requires=["numpy", "pandas", "networkx"]

)