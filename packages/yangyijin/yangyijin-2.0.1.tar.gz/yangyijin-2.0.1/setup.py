import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
        long_description = fh.read()

setuptools.setup(
        name="yangyijin",
        version="2.0.1",
        author="yangyijin",
        author_email="15000733231@163.com",
        description="This is a test model",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/wistbean/learn_python3_spider",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
)
