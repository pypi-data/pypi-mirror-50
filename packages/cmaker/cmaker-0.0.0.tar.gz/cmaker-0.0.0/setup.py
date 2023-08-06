import setuptools

setuptools.setup(
    name="cmaker",
    version="0.0.0",
    description="Recursive make-operation for sprawling C++ projects.",
    url="https://github.com/ychnlgy/Cmaker",
    author="Yuchen Li",
    author_email="ychnlgy@gmail.com",
    license="MIT",
    scripts=["makerc.py"],
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True
)
