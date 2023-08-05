from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as rf:
    install_requires = rf.read().splitlines()

setup(
    name='wtm',
    license='MIT',
    author='manan',
    version='1.0.1',
    packages=['wtm'],
    scripts=['bin/wtm'],
    long_description=long_description,
    install_requires=install_requires,
    url='https://github.com/mentix02/wtm',
    author_email='manan.yadav02@gmail.com',
    description='Downloads songs from the internet.',
    long_description_content_type='text/markdown',
    keywords='wtm what-the-music music what the music',
    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Programming Language :: Python :: 3',
    ]
)
