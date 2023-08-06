import setuptools

setuptools.setup(
    name='littlenv',
    version='0.1.3',
    author="Oscar Mendez Aguirre",
    author_email="oscfrayle@gmail.com",
    description="A simple script for manage .env in django",
    long_description="A simple script for manage .env in django, is very easy, you just have to import this library in your manage.py",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/oscfrayle/littlenv",
    download_url="https://gitlab.com/oscfrayle/littlenv/-/tags/0.1.2",
    packages=['littlenv'],
    keywords=['deploy', 'env', '.env'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
