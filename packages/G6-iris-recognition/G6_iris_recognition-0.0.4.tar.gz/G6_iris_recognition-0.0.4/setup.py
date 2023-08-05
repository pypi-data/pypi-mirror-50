from setuptools import setup, find_packages

requirements = [
    'opencv-python',
    'opencv-contrib-python',
    'scikit-image',
    'scipy',
    'numpy',
    'matplotlib',
    'imutils',
]


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="G6_iris_recognition",
    version="0.0.4",
    description="A Python package to iris recognition.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Gate6",
    # author_email="gate6.info@gate6.com",
    author_email="vijay.bharati@gate6.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3",

    ],
    # packages=find_packages(),
    packages=["G6_iris_recognition"],
    include_package_data=True,
    install_requires=requirements,
    # install_requires=["requests"],
    entry_points={
        'console_scripts': [
            'G6_iris_recognition=G6_iris_recognition.main:main',
        ]
    },
)
