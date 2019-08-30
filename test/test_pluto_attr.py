# Copyright (C) 2019 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from nose.tools import assert_equal
from parameterized import parameterized, parameterized_class

import unittest
import math
import numpy as np
import random
import iio
from adi import Pluto

dev_checked = False
found_dev = False


def check_pluto():
    # Try USB contexts first
    contexts = iio.scan_contexts()
    for c in contexts:
        if "PlutoSDR" in contexts[c]:
            return True
    # Try auto discover
    try:
        iio.Context("ip:pluto.local")
        return True
    except Exception as e:
        print(e)
        return False


def check_dev():
    global dev_checked
    global found_dev
    if not dev_checked:
        found_dev = check_pluto()
        dev_checked = True
    return found_dev


scalar_properties = [
    {"attr": "tx_hardwaregain", "start": -89.75, "stop": 0.0, "step": 0.25},
    {"attr": "rx_lo", "start": 70000000, "stop": 6000000000, "step": 1, "tol": 8},
    {"attr": "tx_lo", "start": 70000000, "stop": 6000000000, "step": 1, "tol": 8},
    {"attr": "sample_rate", "start": 2084000, "stop": 30720000, "step": 1, "tol": 4},
]


@parameterized_class(scalar_properties)
@unittest.skipUnless(check_dev(), "PlutoSDR not attached")
class TestPlutoAttr(unittest.TestCase):
    tol = 0.0000001

    def test_pluto_attribute_single_value(self):
        sdr = Pluto()
        # Pick random number in operational range
        numints = int((self.stop - self.start) / self.step)
        ind = random.randint(0, numints + 1)
        val = self.start + self.step * ind
        # Check hardware
        setattr(sdr, self.attr, val)
        rval = float(getattr(sdr, self.attr))
        if abs(val - rval) > self.tol:
            print("Failed to set: " + self.attr)
            print("Set: " + str(val))
            print("Got: " + str(rval))
        self.assertTrue(abs(val - rval) <= self.tol)


if __name__ == "__main__":
    unittest.main()
