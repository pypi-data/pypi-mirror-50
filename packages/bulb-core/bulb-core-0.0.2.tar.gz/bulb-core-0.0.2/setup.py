import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bulb-core",
    version="0.0.2",
    author="Lilian Cruanes",
    author_email="cruaneslilian@gmail.com",
    description="Neo4j integration for Django, and much more tools for deployment of consequent websites...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LilianCruanes/bulb",
    packages=setuptools.find_packages(),
    install_requires=['neo4j', "Pillow-SIMD", "requests", "paramiko", "pysftp", "django-compressor", "bcrypt"],
    # bcrypt: for password hashing,
    # requests: for CDNs purge requests,
    # pysftp: for sftp content saving,
    # django-compressor & django-libsass: for sass/scss support during bundle operations,
    # Pillow-SIMD: for images compression and optimization.
    # paramiko: for SSH handling
    extras_require={"django-libsass": ["django-libsass"]},
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Natural Language :: English",
        "Topic :: Database",
        "Topic :: Internet :: File Transfer Protocol (FTP)",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Topic :: Internet :: WWW/HTTP :: WSGI"
    ],
)
