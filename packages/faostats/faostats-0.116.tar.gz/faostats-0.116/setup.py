from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
     name='faostats',
     version='0.116',
     author="Daniel Risi",
     author_email="risi.dj@gmail.com",
     description="A package to download faostat data to a postgres database and then analyse it",
     long_description=readme(),
     long_description_content_type="text/markdown",
     url="https://github.com/daniel-risi/faostats",
     packages=['faostats'],
     install_requires=['pandas', 'sqlalchemy'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent"],
     test_suite = 'nose.collector',
     tests_require = ['nose'],
     include_package_data=True,
     zip_safe=False)















