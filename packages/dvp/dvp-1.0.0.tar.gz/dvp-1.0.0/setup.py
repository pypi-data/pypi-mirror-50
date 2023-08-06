import setuptools

PYTHON_SRC = 'src/main/python'

install_requires = [
  "dvp-common == 1.0.0",
  "dvp-libs == 1.0.0",
  "dvp-platform == 1.0.0",
  "dvp-tools == 1.0.0",
]

setuptools.setup(name='dvp',
                 version='1.0.0',
                 install_requires=install_requires,
                 package_dir={'': PYTHON_SRC},
                 packages=setuptools.find_packages(PYTHON_SRC),
)
