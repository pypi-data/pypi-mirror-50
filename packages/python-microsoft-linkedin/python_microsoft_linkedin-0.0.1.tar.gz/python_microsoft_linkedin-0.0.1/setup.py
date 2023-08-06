from setuptools import setup, find_packages

setup(
    name='python_microsoft_linkedin',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/alisterion/python-microsoft-linkedin',
    license='MIT',
    author='Alex Vorobiov',
    author_email='a.vorobyov@bvblogic.com',
    description='Microsoft Linkedin Api Wrapper on python 3.6',
    keywords='python linkedin v2',
    install_requires=[
        'requests',
    ],
)
