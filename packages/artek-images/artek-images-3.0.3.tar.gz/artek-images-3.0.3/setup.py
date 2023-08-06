from setuptools import setup, find_packages

VERSION = "3.0.3"
setup(
    author="Artek",
    author_email="luca@ahd-creative.com",
    description="an app for managing collections of images associated with a content object",
    name="artek-images",
    version=VERSION,
    url="http://github.com/AHDCreative/artek-images/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "images": []
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=1.11",
        "django-imagekit>=3.2.7",
        "pilkit>=1.1.13",
        "pillow>=3.3.0",
        "pytz>=2016.6.1",
    ],
    tests_require=[
        "django-test-plus>=1.0.11",
        "mock>=2.0.0",
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)