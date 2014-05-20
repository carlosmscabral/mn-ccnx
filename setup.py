#!/usr/bin/env python

"Setuptools params"

from setuptools import setup, find_packages
from os.path import join

# Get version number from source tree
import sys
sys.path.append( '.' )
from mininet.net import VERSION

SUPPORTED_MN_VERSION = "2.0.0 2.1.0 2.1.0+"

if not VERSION in SUPPORTED_MN_VERSION:
  print 'Mininet version %s is not supported' % VERSION
  print 'Supported versions: %s' % SUPPORTED_MN_VERSION
  quit()

scripts = [ join( 'bin', filename ) for filename in [ 'miniccnx', 'miniccnxedit' ] ]

modname = distname = 'ccnxmn'
CCNXVERSION=1

setup(
    name=distname,
    version=CCNXVERSION,
    description='Process-based OpenFlow emulator with CCNx extension',
    author='Carlos Cabral, PhiHo Hoang',
    author_email='cabral@dca.fee.unicamp.br',
    packages=[ 'ccnxmn' ],
    long_description="""
        Mininet is a network emulator which uses lightweight
        virtualization to create virtual networks for rapid
        prototyping of Software-Defined Network (SDN) designs
        using OpenFlow. http://openflow.org/mininet.
        ccnxmn is an extension for using Content Centric
        Networks based on the NDN model (project CCNx).
        """,
    classifiers=[
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python",
          "Development Status :: 2 - Pre-Alpha",
          "Intended Audience :: Developers",
          "Topic :: Internet",
    ],
    keywords='networking emulator protocol Internet OpenFlow SDN CCNx CCN',
    license='BSD',
    install_requires=[
        'setuptools',
        'networkx'
    ],
    scripts=scripts,
)
