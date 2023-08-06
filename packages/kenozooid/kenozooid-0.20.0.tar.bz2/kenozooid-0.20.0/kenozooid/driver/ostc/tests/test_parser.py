#
# Kenozooid - dive planning and analysis toolbox.
#
# Copyright (C) 2009-2019 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
OSTC driver binary parser routines tests.
"""

import bz2
import base64
import unittest

import kenozooid.driver.ostc.parser as ostc_parser
import kenozooid.uddf as ku

from . import data as od


class ParserTestCase(unittest.TestCase):
    """
    OSTC binary data parsing tests.
    """
    def test_data_parsing(self):
        """Test OSTC data parsing (< 1.91)
        """
        dump = ostc_parser.get_data(od.RAW_DATA_OSTC)

        self.assertEqual(b'\xaa' * 5 + b'\x55', dump.preamble)

        # first dive is deleted one so no \xfa\xfa
        self.assertEqual(b'\xfa\x20', dump.profiles[:2])

        self.assertEqual(4142, dump.voltage)

        # ver. 1.26
        self.assertEqual(1, dump.ver1)
        self.assertEqual(26, dump.ver2)

        self.assertEqual(32768, dump.profiles)


    def test_data_parsing(self):
        """Test OSTC data parsing (>= 1.91)
        """
        dump = ostc_parser.get_data(od.RAW_DATA_OSTC_MK2_194)

        self.assertEqual(b'\xaa' * 5 + b'\x55', dump.preamble)

        self.assertEqual(4221, dump.voltage)

        # ver. 1.94
        self.assertEqual(1, dump.ver1)
        self.assertEqual(94, dump.ver2)
        
        self.assertEqual(65536, len(dump.profiles))


    def test_eeprom_parsing(self):
        """Test EEPROM data parsing
        """
        dump = ostc_parser.get_data(od.RAW_DATA_OSTC)
        eeprom = dump.eeprom

        self.assertEqual(155, eeprom.serial)
        self.assertEqual(23, eeprom.dives)
        self.assertEqual(252, len(eeprom.data))


    def test_data_get(self):
        """
        Test OSTC data getting (< 1.91)
        """
        dump = ostc_parser.get_data(od.RAW_DATA_OSTC)
        profile = tuple(ostc_parser.profiles(dump.profiles))
        # five dives expected
        self.assertEqual(5, len(profile))
        for header, block in profile:
            self.assertEqual(b'\xfa\xfa', header[:2])
            self.assertEqual(0x20, header[2])
            self.assertEqual(b'\xfb\xfb', header[-2:])
            self.assertEqual(47, len(header))
            self.assertEqual(b'\xfd\xfd', block[-2:])


    def test_data_get_191(self):
        """
        Test OSTC data getting (>= 1.91)
        """
        dump = ostc_parser.get_data(od.RAW_DATA_OSTC_MK2_194)
        profile = tuple(ostc_parser.profiles(dump.profiles))
        # five dives expected
        self.assertEqual(9, len(profile))
        for i, (header, block) in enumerate(profile):
            self.assertEqual(b'\xfa\xfa', header[:2])
            if i < 2:
                self.assertEqual(0x20, header[2])
                self.assertEqual(47, len(header))
            else:
                self.assertEqual(0x21, header[2])
                self.assertEqual(57, len(header))
            self.assertEqual(b'\xfb\xfb', header[-2:])
            self.assertEqual(b'\xfd\xfd', block[-2:])


    def test_dive_profile_header_parsing(self):
        """
        Test dive profile header parsing (< 1.91)
        """
        dump = ostc_parser.get_data(od.RAW_DATA_OSTC)
        profile = tuple(ostc_parser.profiles(dump.profiles))
        header = ostc_parser.header(profile[0][0])
        self.assertEqual(0x20, header.version)
        self.assertEqual(1, header.month)
        self.assertEqual(31, header.day)
        self.assertEqual(9, header.year)
        self.assertEqual(23, header.hour)
        self.assertEqual(41, header.minute)
        self.assertEqual(7500, header.max_depth)
        self.assertEqual(32, header.dive_time_m)
        self.assertEqual(9, header.dive_time_s)
        self.assertEqual(275, header.min_temp)
        self.assertEqual(1025, header.surface_pressure)
        self.assertEqual(920, header.desaturation)
        self.assertEqual(21, header.gas1_o2)
        self.assertEqual(32, header.gas2_o2)
        self.assertEqual(21, header.gas3_o2)
        self.assertEqual(21, header.gas4_o2)
        self.assertEqual(21, header.gas5_o2)
        self.assertEqual(32, header.gas6_o2)
        self.assertEqual(0, header.gas1_he)
        self.assertEqual(0, header.gas2_he)
        self.assertEqual(0, header.gas3_he)
        self.assertEqual(0, header.gas4_he)
        self.assertEqual(0, header.gas5_he)
        self.assertEqual(0, header.gas6_he)
        self.assertEqual(1, header.gas)
        self.assertEqual(1, header.ver1)
        self.assertEqual(26, header.ver2)
        self.assertEqual(4066, header.voltage)
        self.assertEqual(10, header.sampling)
        self.assertEqual(38, header.div_temp)
        self.assertEqual(38, header.div_deco)
        self.assertEqual(32, header.div_gf)
        self.assertEqual(48, header.div_ppo2)
        self.assertEqual(0, header.div_deco_debug)
        self.assertEqual(0, header.div_cns)
        self.assertEqual(0, header.salnity)
        self.assertEqual(0, header.max_cns)


    def test_dive_profile_header_parsing_191(self):
        """
        Test dive profile header parsing (>= 1.91)
        """
        dump = ostc_parser.get_data(od.RAW_DATA_OSTC_MK2_194)
        profiles = tuple(ostc_parser.profiles(dump.profiles))
        header = ostc_parser.header(profiles[8][0])
        self.assertEqual(0x21, header.version)
        self.assertEqual(7, header.month)
        self.assertEqual(28, header.day)
        self.assertEqual(11, header.year)
        self.assertEqual(22, header.hour)
        self.assertEqual(31, header.minute)
        self.assertEqual(6016, header.max_depth)
        self.assertEqual(64, header.dive_time_m)
        self.assertEqual(4, header.dive_time_s)
        self.assertEqual(57, header.min_temp)
        self.assertEqual(975, header.surface_pressure)
        self.assertEqual(248, header.desaturation)
        self.assertEqual(21, header.gas1_o2)
        self.assertEqual(47, header.gas2_o2)
        self.assertEqual(100, header.gas3_o2)
        self.assertEqual(12, header.gas4_o2)
        self.assertEqual(17, header.gas5_o2)
        self.assertEqual(10, header.gas6_o2)
        self.assertEqual(0, header.gas1_he)
        self.assertEqual(0, header.gas2_he)
        self.assertEqual(0, header.gas3_he)
        self.assertEqual(45, header.gas4_he)
        self.assertEqual(37, header.gas5_he)
        self.assertEqual(50, header.gas6_he)
        self.assertEqual(4, header.gas)
        self.assertEqual(1, header.ver1)
        self.assertEqual(93, header.ver2)
        self.assertEqual(4066, header.voltage)
        self.assertEqual(4, header.sampling)
        self.assertEqual(47, header.div_temp)
        self.assertEqual(47, header.div_deco)
        self.assertEqual(16, header.div_gf)
        self.assertEqual(48, header.div_ppo2)
        self.assertEqual(144, header.div_deco_debug)
        self.assertEqual(16, header.div_cns)
        self.assertEqual(100, header.salnity)
        self.assertEqual(36, header.max_cns)
        self.assertEqual(2085, header.avg_depth)
        self.assertEqual(4123, header.dive_time_total_s)
        self.assertEqual(10, header.gf_lo)
        self.assertEqual(85, header.gf_hi)
        self.assertEqual(5, header.deco_type)
        self.assertEqual(0, header.reserved1)
        self.assertEqual(0, header.reserved2)
        self.assertEqual(0, header.reserved3)


    def test_dive_profile_block_parsing(self):
        """
        Test dive profile data block parsing
        """
        dump = ostc_parser.get_data(od.RAW_DATA_OSTC)
        profiles = tuple(ostc_parser.profiles(dump.profiles))
        h, p = profiles[0]
        header = ostc_parser.header(h)
        dive = tuple(ostc_parser.dive_data(header, p))
        # 217 samples, but dive time is 32:09 (sampling 10)
        self.assertEqual(193, len(dive))

        self.assertAlmostEqual(3.0, dive[0].depth, 3)
        self.assertFalse(dive[0].alarm)
        self.assertAlmostEqual(23.0, dive[1].depth, 3)
        self.assertFalse(dive[1].alarm)

        self.assertAlmostEqual(29.5, dive[5].temp, 3)
        self.assertEqual(5, dive[5].alarm)
        self.assertEqual(2, dive[5].current_gas)
        self.assertEqual(0, dive[5].deco_depth)
        self.assertEqual(7, dive[5].deco_time)

        self.assertAlmostEqual(29.0, dive[23].temp, 3)
        self.assertFalse(dive[23].alarm)
        self.assertFalse(dive[23].current_gas)
        self.assertEqual(3, dive[23].deco_depth)
        self.assertEqual(1, dive[23].deco_time)


    def test_sample_data_parsing(self):
        """
        Test sample data parsing
        """
        from struct import unpack

        # temp = 50 (5 degrees)
        # deco = NDL/160
        data = b'\x2c\x01\x84\x32\x00\x00\xa0'
        v = ostc_parser.sample_data(data, 3, 8, 4, 2)
        self.assertEqual(50, unpack('<H', v)[0])

        # 5th sample and divisor sampling == 4 => no data
        v = ostc_parser.sample_data(data, 3, 5, 4, 2)
        self.assertFalse(v)

        d, t = ostc_parser.sample_data(data, 5, 8, 4, 2)
        self.assertEqual(0, d)
        self.assertEqual(0xa0, t)


    def test_divisor(self):
        """
        Test getting divisor information
        """
        divisor, size = ostc_parser.divisor(38)
        self.assertEqual(6, divisor)
        self.assertEqual(2, size)

        divisor, size = ostc_parser.divisor(32)
        self.assertEqual(0, divisor)
        self.assertEqual(2, size)

        divisor, size = ostc_parser.divisor(48)
        self.assertEqual(0, divisor)
        self.assertEqual(3, size)


    def test_flag_byte_split(self):
        """
        Test splitting profile flag byte
        """
        size, event = ostc_parser.flag_byte(132)
        self.assertEqual(4, size)
        self.assertEqual(1, event)

        size, event = ostc_parser.flag_byte(5)
        self.assertEqual(5, size)
        self.assertEqual(0, event)


    def test_invalid_profile(self):
        """
        Test parsing invalid profile
        """
        data = tuple(ostc_parser.profiles(ku._dump_decode(od.DATA_OSTC_BROKEN)))
        assert 32 == len(data)

        # dive no 31 is broken (count from 0)
        h, p = data[30]
        header = ostc_parser.header(h)
        dive_data = ostc_parser.dive_data(header, p)
        self.assertRaises(ValueError, tuple, dive_data)


    def test_date_bug(self):
        """
        Test OSTC date bug
        """
        data = tuple(ostc_parser.profiles(ku._dump_decode(od.DATA_OSTC_DATE_BUG)))
        d1 = data[16]
        d2 = data[17]

        # dive 17 and 18 - incorrect month information
        header = ostc_parser.header(d1[0])
        self.assertEqual(1, header.month)

        header = ostc_parser.header(d2[0])
        self.assertEqual(1, header.month)



# vim: sw=4:et:ai
