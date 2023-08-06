from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='spamfilter_avcourt',
    version='0.1.0',
    description='Simple Bayesian Spamfilter',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='avcourt',
    author_email='andrew.vcourt@gmail.com',
    url='https://github.com/avcourt',
    # license=license,
    # packages=find_packages(exclude=('tests', 'docs'))
)