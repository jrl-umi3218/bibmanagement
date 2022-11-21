#!/usr/bin/env python3

import sys
import websitePubli

if len(sys.argv) < 2:
    print("{} <path to jrl-publi> <path to jrl-umi3218.github.com>".format(sys.argv[0]))
    sys.exit(1)

websitePubli.generateYamlJRL(sys.argv[1], sys.argv[2], True)
