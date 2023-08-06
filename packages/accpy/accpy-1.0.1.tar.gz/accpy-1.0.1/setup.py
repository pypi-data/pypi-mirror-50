import setuptools

with open("readme.md", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="accpy",
    version="1.0.1",
    author="台灣.屏東大學.周國華老師",
    author_email="ckhmike@gmail.com",
    description="愛客派，會計派，會計人一起來吃派吧！",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.ais.nptu.edu.tw/PythonCode/accpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy'],
)
