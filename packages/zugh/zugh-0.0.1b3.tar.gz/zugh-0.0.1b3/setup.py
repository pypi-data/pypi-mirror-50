

import setuptools

with open(r"/home/kell/projects/ZUGH/zugh/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zugh",
    version="0.0.1b3",
    author="StephenKwen",
    author_email="hyuncankun@outlook.com",
    description="Access to database flexibly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StephenKwen/zugh",
    license='MIT',
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'test*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: SQL",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['SQL', 'MySQL'],
    install_requires=['PyMySQL>=0.9.3'],
    python_requires='>=3.6',

)
