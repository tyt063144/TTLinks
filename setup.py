from setuptools import setup, find_packages

setup(
    name='ttlinks',
    version='0.1.0',
    packages=find_packages(),
    license='MIT',
    description='TTLinks Network Service Packages',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='TTLinks LLC.',
    author_email='dorisjingjing531@gmail.com',
    url='https://github.com/tyt063144/TTLinks.git',
    install_requires=[
        'inflect'
    ],
    keywords=['network', 'ttlinks', 'networking', 'automation', 'ip', 'mac', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Telecommunications Industry",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Networking",
    ]
)