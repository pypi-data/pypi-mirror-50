"""
The Distro data. Names, versions, and any other information.

The DATA variable is a Python LIST of DICTs, each dict is required, at a minimum:

- a 'name' key of type String
- either a 'version' key of type String OR a 'versions' key of type List (of strings)

If no 'flavour' key is provided, the default will be 'Linux'

Any other key/value pair will be added as is to the Distro object
"""

DATA = [
    # Ubuntu (source: http://releases.ubuntu.com/)
    {'name': 'precise', 'versions': ['12.04', '12.04.5'], 'full_name': 'Precise Pangolin', 'flavour': 'Ubuntu'},
    {'name': 'trusty', 'versions': ['14.04', '14.04.6'], 'full_name': 'Trusty Thar', 'flavour': 'Ubuntu'},
    {'name': 'xenial', 'versions': ['16.04', '16.04.6'], 'full_name': 'Xenial Xerus', 'flavour': 'Ubuntu'},
    {'name': 'bionic', 'versions': ['18.04', '18.04.2'], 'full_name': 'Bionic Beaver', 'flavour': 'Ubuntu'},
    {'name': 'cosmic', 'versions': ['18.10'], 'full_name': 'Cosmic Cuttlefish', 'flavour': 'Ubuntu'},
    {'name': 'disco', 'versions': ['19.04'], 'full_name': 'Disco Dingo', 'flavour': 'Ubuntu'},

    # Debian (source: https://www.debian.org/releases/)
    {'name': 'squeeze', 'version': '6', 'flavour': 'Debian'},
    {'name': 'wheezy', 'version': '7', 'flavour': 'Debian'},
    {'name': 'jessie', 'version': '8', 'flavour': 'Debian'},
    {'name': 'stretch', 'version': '9', 'flavour': 'Debian'},
    {'name': 'buster', 'version': '10', 'flavour': 'Debian'},

    # Mint (source: https://en.wikipedia.org/wiki/Linux_Mint_version_history)
    {'name': 'ada', 'version': '1.0', 'flavour': 'Mint'},
    {'name': 'barbara', 'version': '2.0', 'flavour': 'Mint'},
    {'name': 'bea', 'version': '2.1', 'flavour': 'Mint'},
    {'name': 'bianca', 'version': '2.2', 'flavour': 'Mint'},
    {'name': 'cassandra', 'version': '3.0', 'flavour': 'Mint'},
    {'name': 'celena', 'version': '3.1', 'flavour': 'Mint'},
    {'name': 'daryna', 'version': '4', 'flavour': 'Mint'},
    {'name': 'elyssa', 'version': '5', 'flavour': 'Mint'},
    {'name': 'felicia', 'version': '6', 'flavour': 'Mint'},
    {'name': 'gloria', 'version': '7', 'flavour': 'Mint'},
    {'name': 'helena', 'version': '8', 'flavour': 'Mint'},
    {'name': 'isadora', 'version': '9', 'flavour': 'Mint'},
    {'name': 'julia', 'version': '10', 'flavour': 'Mint'},
    {'name': 'katya', 'version': '11', 'flavour': 'Mint'},
    {'name': 'lisa', 'version': '12', 'flavour': 'Mint'},
    {'name': 'maya', 'version': '13', 'flavour': 'Mint'},
    {'name': 'nadia', 'version': '14', 'flavour': 'Mint'},
    {'name': 'olivia', 'version': '15', 'flavour': 'Mint'},
    {'name': 'petra', 'version': '16', 'flavour': 'Mint'},
    {'name': 'qiana', 'version': '17', 'flavour': 'Mint'},
    {'name': 'rebecca', 'version': '17.1', 'flavour': 'Mint'},
    {'name': 'rafaela', 'version': '17.2', 'flavour': 'Mint'},
    {'name': 'rosa', 'version': '17.3', 'flavour': 'Mint'},
    {'name': 'sarah', 'version': '18', 'flavour': 'Mint'},
    {'name': 'serena', 'version': '18.1', 'flavour': 'Mint'},
    {'name': 'sonya', 'version': '18.2', 'flavour': 'Mint'},
    {'name': 'sylvia', 'version': '18.3', 'flavour': 'Mint'},
    {'name': 'tara', 'version': '19', 'flavour': 'Mint'},
    {'name': 'tessa', 'version': '19.1', 'flavour': 'Mint'},
    {'name': 'tina', 'version': '19.2', 'flavour': 'Mint'},
]
