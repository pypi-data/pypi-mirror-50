from setuptools import setup, find_packages
from setuptools.command.develop import develop as _develop
from notebook.nbextensions import install_nbextension
from notebook.services.config import ConfigManager
import os

extension_dir = os.path.join(os.path.dirname(__file__), "mlvispy", "static")

class develop(_develop):
    def run(self):
        _develop.run(self)
        install_nbextension(extension_dir, symlink=True,
                            overwrite=True, user=False, destination="mlvispy")
        cm = ConfigManager()
        cm.update('notebook', {"load_extensions": {"mlvispy/index": True } })

setup(name='mlvispy',
      cmdclass={'develop': develop},
      version='0.0.1',
      description='A wrapper around react components for use in jupyter notebooks',
      python_requires='>=3.7',
      url='https://github.com/',
      author='Hong Wang',
      author_email='hongw@uber.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      data_files=[
        ('share/jupyter/nbextensions/mlvispy', [
            'mlvispy/static/index.js'
        ]),
      ],
      install_requires=[
          "ipython",
          "jupyter-react"
        ]
      )
