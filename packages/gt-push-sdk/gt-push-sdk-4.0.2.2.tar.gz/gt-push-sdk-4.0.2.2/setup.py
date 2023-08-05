import setuptools


setuptools.setup(
    name="gt-push-sdk",
    version="4.0.2.2",
    description="Getui\'s officially supported Python2 client library",
    keywords=['GeTui', 'GTPush API', 'Android Push', 'iOS Push'],
    license='MIT License',

    author="GeTui",
    author_email="support@getui.com",
    url="http://docs.getui.com/getui/server/python/start/",

    packages=setuptools.find_packages(),
    platforms='any',
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)