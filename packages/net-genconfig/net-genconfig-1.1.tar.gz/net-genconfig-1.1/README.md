net-genconfig
=============

This package generates configurations for network devices based on two sources
of information:

* templates -- these Jinja2 files form the basis of a configuration file and
  exist for each different device role (core router, edge switch, etc.)

* inventory -- this is a big database of device details (including the role for
  a particular device) and associated information, such as VLANs, subnets,
  interfaces, etc.
