from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="bardolph",
    version="0.0.2",
    author="Al Fontes",
    author_email="bardolph@fontes.org",
    description="Simple script interpreter for LIFX light bulbs",
    url="https://github.com/al-fontes/bardolph",
    license = 'Apache License 2.0', 
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['controller', 'parser', 'lib', 'web', 'tests'],
    install_requires=['lifxlan'],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'lsc=controller:lsc.main',
            'run=controller:run.main',
            'snapshot=controller:snapshot.main',
            'all_tests=tests:all_tests.main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
)
