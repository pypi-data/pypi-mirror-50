from setuptools import setup,find_packages

setup(
    name='bilibili-moqin',
    version="0.0.1",
    description=(
        "python package which could get bilibili's data"
    ),
    long_description=open('README.md').read(),
    author='xuqingyi',
    author_email='374221195@qq.com',
    maintainer='xuqingyi',
    maintainer_email='374221195@qq.com',
    license='MIT',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/jimmy-moqin/mypy',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'requests','bs4'
    ]
)