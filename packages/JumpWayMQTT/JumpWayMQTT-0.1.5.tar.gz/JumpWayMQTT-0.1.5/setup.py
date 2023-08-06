############################################################################################
#
# Software:      iotJumpWay MQTT Python Clients
# Author:        Adam Milton-Barker (AdamMiltonBarker.com)
# License:       Eclipse Public License 2.0
#
# Title:         iotJumpWay MQTT Python JumpWayApp Client
# Description:   An iotJumpWay MQTT Python JumpWayApp Client that allows you to connect
#                to the iotJumpWay.
# Last Modified: 2019-04-07
#
############################################################################################

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='JumpWayMQTT',
    version="0.1.5",
    description="Python MQTT clients for the iotJumpWay",
    url='https://github.com/AdamMiltonBarker/JumpWayMQTT',
    author='Adam Milton-Barker',
    author_email='adammiltonbarker@gmail.com',
    license=' Eclipse Public License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(),
    package_data={'': ['*.pem']},
    install_requires=[
        "paho-mqtt >= 1.2",
    ],
)
