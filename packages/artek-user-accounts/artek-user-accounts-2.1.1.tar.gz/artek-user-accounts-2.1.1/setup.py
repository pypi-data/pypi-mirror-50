from setuptools import setup, find_packages

setup(
    name="artek-user-accounts",
    version="2.1.1",
    author="DarkArtek",
    author_email="luca@ahd-creative.com",
    description="a Django user account app",
    license="MIT",
    packages=find_packages(),
    url="https://github.com/AHDCreative/django_user_accounts",
    install_requires=[
        "Django>=1.11",
        "django-appconf>=1.0.1",
        "pytz>=2015.6"
    ],
    zip_safe=False,
    package_data={
        "account": [
            "locale/*/LC_MESSAGES/*",
        ],
    },
    extras_require={
        "pytest": ["pytest", "pytest-django"]
    },
    test_suite="runtests.runtest",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ]
)