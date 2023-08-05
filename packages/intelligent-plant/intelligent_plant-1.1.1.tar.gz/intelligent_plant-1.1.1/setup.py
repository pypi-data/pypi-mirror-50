from setuptools import setup

setup(
   name='intelligent_plant',
   url="https://www.intelligentplant.com/",
   version='1.1.1',
   description='A wrapper for the Intellinget Plant API',
   author='Intelligent Plant',
   author_email="support@intelligentplant.com",
   packages=['intelligent_plant'],
   install_requires=['requests', 'pandas']
)