import setuptools

setuptools.setup(
    name="lock_with_timeout",
    version="0.1.7",
    url="https://github.com/fx-kirin/lock_with_timeout",

    author="fx-kirin",
    author_email="fx.kirin@gmail.com",

    description="Theading lock with timeout",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
