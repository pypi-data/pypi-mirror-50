
from setuptools import setup

def get_requirements():
    with open("requirements.txt") as fp:
        return fp.read()

setup(
    name="tf_reader",
    py_modules=['tf_reader'],
    version=0.02,
    description="functions to read tfrecord file as python values.",
    author="Ilya Kamenshchikov",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    license="MIT",
    # install_requires=get_requirements(),
    python_requires=">=3.6",
)