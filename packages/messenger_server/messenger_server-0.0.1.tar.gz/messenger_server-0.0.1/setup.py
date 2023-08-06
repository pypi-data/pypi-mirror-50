from setuptools import setup, find_packages

setup(name="messenger_server",
      version="0.0.1",
      description="Messenger_Server",
      author="Ilia Niyazof",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
