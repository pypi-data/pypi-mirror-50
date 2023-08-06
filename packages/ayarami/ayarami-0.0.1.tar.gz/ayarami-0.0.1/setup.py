import setuptools

setuptools.setup(
    name="ayarami",
    version="0.0.1",
    license="MIT",
    author="Umut Karcı",
    author_email="cediddi@gmail.com",
    description="Simple settings object implementation, just like the one in Django.",
    url="https://gitlab.com/cediddi/ayarami",
    packages=setuptools.find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
