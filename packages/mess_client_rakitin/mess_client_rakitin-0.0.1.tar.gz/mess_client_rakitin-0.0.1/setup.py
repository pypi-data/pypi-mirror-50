from setuptools import setup, find_packages

setup(name="mess_client_rakitin",
      version="0.0.1",
      description="message_server",
      author="Alexey Rakitin",
      author_email="amrakitin@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
