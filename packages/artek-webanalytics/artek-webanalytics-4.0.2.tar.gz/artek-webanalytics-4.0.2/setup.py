from setuptools import find_packages, setup

VERSION = "4.0.2"
setup(
    author="AHD Creative",
    author_email="hello@ahd-creative.com",
    description="web analytics and metrics integration for Django",
    name="artek-webanalytics",
    version=VERSION,
    url="http://github.com/AHDCreative/artek-webanalytics",
    license="MIT",
    packages=find_packages(),
    package_data={
        "artek.webanalytics": [
            "templates/artek/webanalytics/_adwords_conversion.html",
            "templates/artek/webanalytics/_gauges.html",
            "templates/artek/webanalytics/_google.html",
            "templates/artek/webanalytics/_mixpanel.html",
        ]
    },
    install_requires=[
        "django>=1.11",
    ],
    test_suite="runtests.runtests",
    tests_require=[
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
