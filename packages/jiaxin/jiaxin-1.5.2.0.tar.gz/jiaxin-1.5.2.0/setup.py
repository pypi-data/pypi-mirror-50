import setuptools

with open("README.md","r") as fh:
    ld = fh.read()

setuptools.setup(
        name = "jiaxin",
        version = "1.5.2.0",
        author = "yugong",
        author_email = "923601132@qq.com",
        description="i love jiaxin",
        long_description = ld,
        long_description_content_type = "text/markdown",
        url = "https://jiaxin.com",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
)