import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zappa-manage",
    version="0.0.3",
    author="edX-DevOps",
    author_email="devops@edx.org",
    description="Official Manage Package for edX Zappa Bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edx/zappa-manage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=True,
    python_requires=">=3.6",
    entry_points='''
        [console_scripts]
        zappa_manage=scripts.zappa_manage:cli
    ''',
)
