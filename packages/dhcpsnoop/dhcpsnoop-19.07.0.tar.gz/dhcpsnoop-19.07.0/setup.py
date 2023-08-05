from distutils.core import setup

setup(
    name='dhcpsnoop',
    version='19.07.0',
    url="http://github.com/aijayadams/dhcpsnoop",
    packages=['dhcpsnoop',],
    author="Aijay Adams",
    author_email="aijay.adams@gmail.com",
    licenses='Unlicense',
    long_description=open('README').read(),
    install_requires=[
        "Click",
        "glog",
        "py-august",
        "python-dateutil",
        "python-gflags",
        "PyYAML",
        "requests",
        "scapy",
    ],
)
