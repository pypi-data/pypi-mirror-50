from setuptools import setup, find_packages

setup(name="messenger_client",
      version="0.0.1",
      description="Messenger_Client",
      author="Ilia Niyazof",
      author_email="mihail.pendyurin@rt.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
