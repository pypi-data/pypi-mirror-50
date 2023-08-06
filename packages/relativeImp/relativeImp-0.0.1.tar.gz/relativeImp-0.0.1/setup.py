
import setuptools

setuptools.setup(
    name='relativeImp',
    version='0.0.1',
    author='Dan Yang',
    author_email='dyang4@gmail.com',
    packages=['relativeImp'],
    license='LICENSE.txt',
    description='relativeImp is a Python package to conduct the key driver analysis and generate relative importance by driver.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires=">=3.5",
    install_requires=['pandas', 'numpy'],
)