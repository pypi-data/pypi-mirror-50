import setuptools

with open("README.md", "r",encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="PythonZyjTools",
    version="0.0.1",
    author="yongjian zhang",
    author_email="frank_yongjian@163.com",
    description="python工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/echozyj/PythonZyjTools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	python_requires='>=3',
	install_requires=[
       'paramiko>=2.4.2',
        'PyMySQL>=0.9.3',
        'paramiko>=2.4.2',
        'openpyxl>=2.5.6',
        'xlrd>=1.1.0'
	]
)