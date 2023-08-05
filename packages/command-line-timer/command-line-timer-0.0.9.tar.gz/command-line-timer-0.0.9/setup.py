import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="command-line-timer",
    version="0.0.9",
    author="Andy Klier",
    author_email="andyklier@gmail.com",
    description="count down from HH:MM:SS and then sound an alarm (la cucaracha!).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/shindagger/command-line-timer",
    packages = ['timer'],
    include_package_data=True,
    install_requires= ['setuptools', 'pygame'],
    entry_points = {
        'console_scripts': ['timer=timer.main:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
