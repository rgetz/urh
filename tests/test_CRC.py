import sys
import unittest

import sip
from PyQt5.QtWidgets import QApplication

from urh.signalprocessing.encoder import Encoder
from urh.util.crc import crc_generic

class TestCRC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        sip.delete(cls.app)
    # Testmethode muss immer mit Präfix test_* starten
    def test_crc(self):
        # http://depa.usst.edu.cn/chenjq/www2/software/crc/CRC_Javascript/CRCcalculation.htm
        # CRC-16: polynomial="16_standard", start_value = False, final_xor = False, reverse_polynomial=False, reverse_all=False
        # CRC-16-CCITT: polynomial="16_ccitt", start_value = False, final_xor = False, reverse_polynomial=False, reverse_all=False

        # http://www.lammertbies.nl/comm/info/crc-calculation.html <- Fehler
        # CRC-16: polynomial="16_standard", start_value = False, final_xor = False, reverse_polynomial=False, reverse_all=False
        c = crc_generic(polynomial="8_en")
        e = Encoder()

        bitstr = ["010101010110100111011010111011101110111011100110001011101010001011101110110110101101",
                  "010101010110101001101110111011101110111011100110001011101010001011101110110111100101",
                  "010101010110100111010010111011101110111011100110001011101010001011101110110110100101"]

        expected = ["0x78", "0xc9", "0xf2"]

        for value, expect in zip(bitstr, expected):
            nv = ""
            for i in range(0, len(value)):
                if value[i] == "1":
                    nv += "0"
                else:
                    nv += "1"

            self.assertEqual(e.bit2hex(c.crc(e.str2bit(value[4:-8]))), expect)

    def test_reverse_engineering(self):
        c = crc_generic(polynomial="16_standard", start_value=False, final_xor=False,
                        reverse_polynomial=False, reverse_all=False, lsb_first=False, little_endian=False)
        bitstring_set = [
            "1110001111001011100010000101010100000010110111000101100010100100111110111101100110110111011001010010001011101010",
            "1110010011001011100010000101010100000010110111000101100010100100111110111101100110110111011001010010001011101010",
            "1110010111001011100010000101010100000010110111000101100010100100111110111101100110110111011001010010001011101010",
            "1110011011001011100010000101010100000010110111000101100010100100111110111101100110110111011001010010001011101010"]
        bitset = []
        crcset = []

        for i in bitstring_set:
            tmp = c.str2bit(i)
            bitset.append(tmp)
            crcset.append(c.crc(tmp))

        # print(c.guess_standard_parameters(bitset[0], crcset[0]))
        polynomial = c.reverse_engineer_polynomial(bitset, crcset)
        if polynomial:
            self.assertEqual(c.bit2str(polynomial), "1000000000000101")
            self.assertEqual(c.bit2hex(polynomial), "0x8005")
