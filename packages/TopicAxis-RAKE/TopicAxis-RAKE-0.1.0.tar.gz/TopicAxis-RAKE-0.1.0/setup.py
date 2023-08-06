from setuptools import setup, find_packages


def read_long_description():
    with open("README.md") as f:
        return f.read()


setup(
    name="TopicAxis-RAKE",
    version="0.1.0",
    author="Panagiotis Matigakis",
    author_email="pmatigakis@gmail.com",
    description="Text keyword extraction library",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/topicaxis/RAKE",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent'
    ]
)
