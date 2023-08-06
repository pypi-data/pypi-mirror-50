from setuptools import setup, find_packages


def read_requirements(filename):
    with open(filename) as f:
        return [
            line.strip()
            for line in f
        ]


def read_long_description():
    with open("README.md") as f:
        return f.read()


setup(
    name="hackernewslib",
    version="0.1.0",
    author="Panagiotis Matigakis",
    author_email="pmatigakis@gmail.com",
    description="Hackernews client library",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/pmatigakis/hackernewslib",
    packages=find_packages(include=["hackernewslib"]),
    install_requires=read_requirements("requirements.txt"),
    setup_requires=read_requirements("requirements-setup.txt"),
    tests_require=read_requirements("requirements-test.txt"),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent'
    ]
)
