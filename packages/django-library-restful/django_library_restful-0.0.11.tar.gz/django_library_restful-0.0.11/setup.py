import setuptools

with open("README.md", "r") as file:
    README = file.read()
    pass

setuptools.setup(
    name="django_library_restful",
    version="0.0.11",
    author="mohammad hosein shamsaei",
    author_email="mh.shamsaei.ms@gmail.com",
    description="a django library manager",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MHolger77/django-libraries",
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
