#!/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

from configparser import ConfigParser
from itertools import chain
from os import getenv
import json

class GeorchestraConfig:
    def __init__(self):
        self.sections = dict()
        self.datadirpath = getenv('georchestradatadir', '/etc/georchestra')
        parser = ConfigParser()
        with open(f"{self.datadirpath}/default.properties") as lines:
            lines = chain(("[section]",), lines)  # This line does the trick.
            parser.read_file(lines)
        self.sections['default'] = parser['section']
        self.sections['default']['datadirpath'] = self.datadirpath
        with open(f"{self.datadirpath}/mapstore/geostore.properties") as lines:
            lines = chain(("[section]",), lines)  # This line does the trick.
            parser.read_file(lines)
        self.sections['mapstoregeostore'] = parser['section']
        with open(f"{self.datadirpath}/security-proxy/targets-mapping.properties") as lines:
            lines = chain(("[section]",), lines)  # This line does the trick.
            parser.read_file(lines)
        self.sections['secproxytargets'] = parser['section']
        self.sections['urls'] = dict()
        with open(f"{self.datadirpath}/mapstore/configs/localConfig.json") as file:
            s = file.read()
            localconfig = json.loads(s)
            # used to find geonetwork entry in sec-proxy targets
            try:
                localentry = localconfig["initialState"]["defaultState"]["catalog"]["default"]["services"]["local"]
                self.sections['urls']['localgn'] = localentry['url'].split('/')[1]
            except:
                # safe default value
                self.sections['urls']['localgn'] = 'geonetwork'
            try:
                localentry = localconfig["initialState"]["defaultState"]["catalog"]["default"]["services"]["localgs"]
                self.sections['urls']['localgs'] = localentry['url'].split('/')[1]
            except:
                # safe default value
                self.sections['urls']['localgs'] = 'geoserver'

    def get(self, key, section='default'):
        if section in self.sections:
            return self.sections[section].get(key, None)
        else:
            return None
