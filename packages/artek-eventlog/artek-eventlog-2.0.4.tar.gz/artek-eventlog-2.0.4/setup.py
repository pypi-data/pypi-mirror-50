from setuptools import find_packages, setup

VERSION = "2.0.4"
setup(
    auhor="AHDCreative",
    author_email="hello@ahd-creative.com",
    description="an event logger for Django projects",
    name="artek-eventlog",
    version=VERSION,
    url="http://github.com/AHDCreative/artek-eventlog/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "eventlog": []
    },
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
    install_requires=[
        "django>=1.11",
        "jsonfield>=2.0.2"
    ],
    tests_require=[
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)
