#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module:
***

 Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
 This file is owned exclusively by Smart Arcs Ltd.
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
 Written by Dan Cvrcek <support@smartarchitects.co.uk>, 2019
"""
__author__ = "Dan Cvrcek"
__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@smartarchitects.co.uk'
__status__ = 'Development'

import re


# noinspection PyPep8
class PythonPostsignum(object):
    """
    A test implementation of PostSignum cards
    """
    # postsignum doesn't do applet select at all
    memory = [
        {
            "item":"xxxxx",
            "response": "xxxx",
            "data": [
                {
                    "item": "00A4040010A0000000770103000610000000000002",
                    "response": "9000",
                    "mffile": [
                        {
                            "item": "00A408000414009002",
                            "response": "9000",
                            "data": [
                                {
                                    "item": "0022F303",  # manage security environment - RESTORE
                                    "response": "9000"
                                },
                                {
                                    "item": "0022F1B80383010E",  # MSE set B8 03 83 01 0e - no hash alg, just alg = RSA2048
                                    "response": "9000"
                                },
                                {
                                    # PSO: hash 80 - plaintext data, 86 - padding byte included '00', padding itself - part 1
                                    "item": "102A808681000001FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00",
                                    "response": "9000"  # hash - plain value https://www.openecard.org/en/ecard-api-framework/cardinfo/test-specification/
                                },
                                {
                                    # PSO: HASH -part 2 - the rest of data itself- it's - chaining
                                    "item": "002A808680FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF003031300D060960864801650304020105000420A67F58C63826176D74484D257231289513E79E03882157B926D594D10D7736A900",
                                    "response": "3D8F8E09589325859321C5BF85C11459CC58BE056B2EC1D9A975EA4F6B9B43333B23CCA0A51EA4D8C8F8FA0E604C459C0330271558502FFD459C409CFCA13B3ECC5375EC411047CC1FB6E826671E0C427D5408ECFB76421C1B7A7A1FAEB13D0EAEA0D1E9C3E00F32C584EA632C4A5624FECFF66667EE0CC54C59D408DB698393FB26664406E4D5B2053F2BC68BA6E58095E1C900D3B70E3DC250FE80AB9B156CA890934D0E892A7C26ED9FE63F72FBC180BC58048EEE641CC076B34501776ECF878F2108D967B65C93641BD05685A5A5B28A38B031C1A51FD38E93E9B4D7A7440505B6BEA1D32100B6A24D85ABBD5803B4ED2785F3AC4F4886255CFBD9BA924E9000"
                                }
                            ]
                        },
                        {
                            "item": "00A408000410001003",
                            "response": "9000",
                            "data": [
                                {
                                    "item": "00B0000010",
                                    "response": "323434343133343030303030353332329000"
                                }
                            ]
                        },
                        {
                            "item": "00A408000411001101",
                            "response": "9000",
                            "data": [
                                {
                                    "item": "00B0000001",
                                    "response": "009000"
                                }
                            ]
                        },
                        {
                            "item": "00A40800023F01",
                            "response": "9000",
                            "data": [
                                {
                                    "item": "00B2010403",
                                    "response": "6A83"
                                }
                            ]
                        },
                        {
                            "item": "00A40800041400900200",
                            "response": "6F358102007F8203380000830290028501018609FF1010FFFFFFFF10FFCB18FFFF03040304FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF9000",
                            "data": [
                            ]
                        },
                        {
                            "item": "00A40800041400100000",
                            "response": "6F358002002482030100008302100085010186090000FFFFFFFF11FFFFCB18FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF9000",
                            "data": [
                                {
                                    "item": "00B0000024",
                                    "response": "546F6B656E4D45202020202020202020202020202020202020202020202020200000040D9000"
                                }
                            ]
                        },
                        {
                            "item": "00A40800041400400000",
                            "response": "6F35800200F082030100008302400085010186090000000000000000FFCB18FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF9000",
                            "data": [
                                {
                                    "item": "00B0000064",
                                    "response": "00000000000000000000000000000000FAFE000000FAFE0000FF10040800FF2002052500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009000"
                                },
                                {
                                    "item": "00B0006464",
                                    "response": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009000"
                                },
                                {
                                    "item": "00B000C828",
                                    "response": "000000000000000000000000000000000000000000000000000000000000000000000000000000009000"
                                }
                            ]
                        },
                        {
                            "item": "00A40800041400500000",
                            "response": "6F35800200F082030100008302500085010186090010100000000000FFCB18FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF9000",
                            "data": [
                                {
                                    "item": "00B0000064",
                                    "response": "000000000000FAFE000000FAFE0000FF300E080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009000"
                                },
                                {
                                    "item": "00B0006464",
                                    "response": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009000"
                                },
                                {
                                    "item": "00B000C828",
                                    "response": "000000000000000000000000000000000000000000000000000000000000000000000000000000009000"
                                }
                            ]
                        },
                        {
                            "item": "00A408000614009001ABDE00",
                            "response": "6A82",
                            "data": [
                            ]
                        },
                        {
                            "item": "00A408000614009001FFF000",
                            "response": "6A82",
                            "data": [
                            ]
                        },
                        {
                            "item": "00A40000023F00",
                            "response": "9000",
                            "data": [
                                {
                                    "item": "80CADF6405",
                                    "response": "DF64024C5E9000"
                                },
                                {
                                    "item": "0020001000",  # this is PIN tries
                                    "response": {"pin":"9000", "default": "63C3"},
                                },
                                {
                                    "item": "0020001100",  # this is PUK tries
                                    "response": {"puk":"9000", "default": "63C8"}
                                }
                            ]
                        },
                        {
                            "item": "00A4080004140011CE00",
                            "response": "6A82",
                            "data": [
                            ]
                        },
                        {
                            "item": "00A40800061400900111CE00",
                            "response": "6F35800201008203010000830211CE8501018609000000FFFFFF0000FFCB18FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF9000",
                            "data": [
                                {
                                    "item": "00B0000064",
                                    "response": "0080997F06C0832C793E700A27BC95AFC9A53A1205E48451E6BC24EF6085888B0C25917D87812058B3A3246ECFD032B700FDCBAE4DDCDE7F88F744A07E40B0A833BC9C19B4C45D7577367C5F518D8D3FC236C0F78AE783866C998010E2664718CB6FF3389000"
                                },
                                {
                                    "item": "00B0006464",
                                    "response": "3A09B7E798FB2D758C36725DF53B72ED8539EE2FD991AF7BB188AF44B73E000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009000"
                                },
                                {
                                    "item": "00B000C838",
                                    "response": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009000"
                                }
                            ]
                        },
                        {
                            "item": "00A408000614009001210200",
                            "response": "6F358002005D8203010000830221028501018609001010FFFF10FFFFFFCB18FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF9000",
                            "data": [
                                {
                                    "item": "00B000005D",
                                    "response": "0001002774652D31303636393032362D653432652D346662382D386366642D393062303131303338323532002774652D31303636393032362D653432652D346662382D386366642D393062303131303338323532000000000003088E3C9000"
                                }
                            ]
                        },
                        {
                            "item": "00A408000614009001110400",
                            "response": "6F358002016D8203010000830211048501018609001010FFFF10FFFFFFCB18FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF9000",
                            "data": [
                                {
                                    "item": "00B0000064",
                                    "response": "004D002774652D31303636393032362D653432652D346662382D386366642D393062303131303338323532002774652D31303636393032362D653432652D346662382D386366642D393062303131303338323532000000000000000000000000000000009000"
                                },
                                {
                                    "item": "00B0006464",
                                    "response": "0000010093E23DFD912C0D230BBE7CA71A03703111FC42C25C0A092B0725FA093C1992CD0B876B0FAC6B654F2FA366FFF600E99560952F54692553E0549E920613351628D24EACB68B5E071669A145E574E04F872E10EFDC478EA22EBC3B73DCBB8C03979000"
                                },
                                {
                                    "item": "00B000C864",
                                    "response": "DBD69457637C5DE1A4F1DF4FCA2918A893598BABD920358BF1ECCA361AD3CE3326EA187FCE16125E64A53E28B7BEB0FC60DA40A0EE04F2814D415787C42A94A27ACB0826F515A26DBD41F3508463B53544850D9438FF2588ACDB8ACAA4F2AA94CC19BDED9000"
                                },
                                {
                                    "item": "00B0012C41",
                                    "response": "301DA56C8B87FE50CCC202EB4A16D812BCC12F30D6A471CE6EB110CB5334A197E171364242F7555732B6F891BE648B5A4640CF4599EA6A2EF31C8EEF00030100019000"
                                }
                            ]
                        },
                        {
                            "item": "00A408000614009002310E00",
                            "response": "6F358002016A82030100008302310E8501018609101010FFFF10FFFFFFCB18FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF9000",
                            "data": [
                                {
                                    "item": "00B0000064",
                                    "response": "0035002774652D31303636393032362D653432652D346662382D386366642D393062303131303338323532002774652D31303636393032362D653432652D346662382D386366642D393062303131303338323532000000000000000000000000000000009000"
                                },
                                {
                                    "item": "00B0006464",
                                    "response": "000093E23DFD912C0D230BBE7CA71A03703111FC42C25C0A092B0725FA093C1992CD0B876B0FAC6B654F2FA366FFF600E99560952F54692553E0549E920613351628D24EACB68B5E071669A145E574E04F872E10EFDC478EA22EBC3B73DCBB8C0397DBD69000"
                                },
                                {
                                    "item": "00B000C864",
                                    "response": "9457637C5DE1A4F1DF4FCA2918A893598BABD920358BF1ECCA361AD3CE3326EA187FCE16125E64A53E28B7BEB0FC60DA40A0EE04F2814D415787C42A94A27ACB0826F515A26DBD41F3508463B53544850D9438FF2588ACDB8ACAA4F2AA94CC19BDED301D9000"
                                },
                                {
                                    "item": "00B0012C3E",
                                    "response": "A56C8B87FE50CCC202EB4A16D812BCC12F30D6A471CE6EB110CB5334A197E171364242F7555732B6F891BE648B5A4640CF4599EA6A2EF31C8EEF030100019000"
                                },
                            ]
                        },
                        {
                            "item": "00A408000614009001200200",
                            "response": "6F35800205258203010000830220028501018609001010FFFF10FFFFFFCB18FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF9000",
                            "data": [
                                {
                                    "item": "00B0000004",
                                    "response": "308205219000"
                                },
                                {
                                    "item": "00B0000464",
                                    "response": "30820409A0030201020203088E3C300D06092A864886F70D01010B05003064310B300906035504061302435A312C302A060355040A0C23C48C65736BC3A120706FC5A174612C20732E702E205B49C48C2034373131343938335D312730250603550403139000"
                                },
                                {
                                    "item": "00B0006864",
                                    "response": "1E44454D4F20506F73745369676E756D205175616C69666965642043412032301E170D3138303131373139303430325A170D3138303231363139303430325A3081AC310B300906035504061302435A312D302B060355040A0C244D61736172796B6F76619000"
                                },
                                {
                                    "item": "00B000CC64",
                                    "response": "20756E697665727A697461205B49C48C2030303231363232345D310A3008060355040B0C01313127302506035504030C1E524E44722E204D69726F736C6176204BC599697061C48D2C2050682E442E312230200603550405131950313233343536202D209000"
                                },
                                {
                                    "item": "00B0013064",
                                    "response": "44454D4F20636572746966696B617431153013060355040C0C0C70726F6772616DC3A1746F7230820122300D06092A864886F70D01010105000382010F003082010A028201010093E23DFD912C0D230BBE7CA71A03703111FC42C25C0A092B0725FA093C9000"
                                },
                                {
                                    "item": "00B0019464",
                                    "response": "1992CD0B876B0FAC6B654F2FA366FFF600E99560952F54692553E0549E920613351628D24EACB68B5E071669A145E574E04F872E10EFDC478EA22EBC3B73DCBB8C0397DBD69457637C5DE1A4F1DF4FCA2918A893598BABD920358BF1ECCA361AD3CE33269000"
                                },
                                {
                                    "item": "00B001F864",
                                    "response": "EA187FCE16125E64A53E28B7BEB0FC60DA40A0EE04F2814D415787C42A94A27ACB0826F515A26DBD41F3508463B53544850D9438FF2588ACDB8ACAA4F2AA94CC19BDED301DA56C8B87FE50CCC202EB4A16D812BCC12F30D6A471CE6EB110CB5334A197E19000"
                                },
                                {
                                    "item": "00B0025C64",
                                    "response": "71364242F7555732B6F891BE648B5A4640CF4599EA6A2EF31C8EEF0203010001A38201913082018D30520603551D11044B304981116B72697061634066692E6D756E692E637AA01906092B06010401DC190201A00C0C0A31323334353637383930A019069000"
                                },
                                {
                                    "item": "00B002C064",
                                    "response": "0355040DA0120C104A616BC3BD6B6F6C697620706F70697330360603551D20042F302D302B06086781060104010173301F301D06082B0601050507020230110C0F44454D4F20636572746966696B6174301806082B06010505070103040C300A300806069000"
                                },
                                {
                                    "item": "00B0032464",
                                    "response": "04008E460101304F06082B0601050507010104433041303F06082B060105050730028633687474703A2F2F7777772E706F73747369676E756D2E637A2F6372742F64656D6F70737175616C69666965646361322E637274300E0603551D0F0101FF0404039000"
                                },
                                {
                                    "item": "00B0038864",
                                    "response": "0205E0301F0603551D2304183016801498FFF3F78B8B9BAD64E6D43EA609A48037CF6CB430440603551D1F043D303B3039A037A0358633687474703A2F2F7777772E706F73747369676E756D2E637A2F63726C2F64656D6F70737175616C6966696564639000"
                                },
                                {
                                    "item": "00B003EC64",
                                    "response": "61322E63726C301D0603551D0E0416041479376C0F7AA3B0CAE278A3739179DF89B5BC0660300D06092A864886F70D01010B05000382010100AAA630F7E83ECB4F3576370DBB545E1AA042C722E3F8904BF7DB4EA6776C40725008CA9FEB0A668B4BFDB29000"
                                },
                                {
                                    "item": "00B0045064",
                                    "response": "4554218A8CB664DA3440FF031864985780FB380C742EC5BDCCF5F888D7E6B4C508191B471A7A80B0017305CA8526542D87E0ABEE5CA00EF83407D438362027137EA7337FB432BA0BB957EA3AE1188A9D0F8DF69FAF605D69BCB63D1099AD620E569349AA9000"
                                },
                                {
                                    "item": "00B004B464",
                                    "response": "6F72E6CD07E3D17028C60CAC1B337C45233D86F9513CD08784017405185DF54AA72DEEF5CA6054DB097DA314DE7F6BA0329B54F1325F1C99D4222EC00EE0A90F6B9F5F04FE8F61073E203EDCC5EE06C5D31A3B7BA82B5F8CE18BD229B372A85EB1AE83099000"
                                },
                                {
                                    "item": "00B005180D",
                                    "response": "B99DAA53E91DAB2A57A0F2C49C9000"
                                },
                                {
                                    "item": "00200010083132333435363738",
                                    "response": "9000",
                                    "flagup": "pin"
                                },
                                {
                                    "item": "0020001000",
                                    "response": {"pin":"9000", "default": "63C3"}
                                },
                                {
                                    "item": "0020001100",
                                    "response": "63C8"
                                },

                            ]
                        },
                    ],
                }
            ]
        }
    ]

    def __init__(self, readername):
        self.mem_pointer = PythonPostsignum.memory
        self.sel_pointer = PythonPostsignum.memory
        self.selected = False
        self.dir = False
        self.ef = None
        self.reader = readername

    # noinspection PyMethodMayBeStatic
    def getupstreamconnection(self):
        """
        Creates a new upstream session for command requests
        :return:
        """
        return None

    def closeupstreamconnection(self, session):
        """
        As described in the abstract class
        :param session:
        :type session: requests.Session
        :return:
        """
        pass

    def reset(self):
        """
        As described in the abstract class
        :return:
        """
        self.mem_pointer = PythonPostsignum.memory
        self.sel_pointer = PythonPostsignum.memory
        # self.selected = False
        self.dir = False
        return "3BFF1800008131FE45006B11050700012101434E531031804A"

    def is_reset(self):
        """
        Check if the card has been reset now
        :return:
        """
        return not self.selected

    # noinspection PyMethodMayBeStatic
    def root(self, apdu):
        result = False
        for each in PythonPostsignum.memory:  # multiple applets, each just 1 entry point
            if apdu == each['data'][0]['item']:
                result = True
        return result

    def select_applet(self, apdu):
        for each in PythonPostsignum.memory:  # multiple applets, each just 1 entry point
            if apdu == each['data'][0]['item']:
                self.selected = True
                self.mem_pointer = each
                self.selected = True
                self.mem_pointer = each['data'][0]
                self.sel_pointer = each['data'][0]
                break
            elif apdu == each['item']:
                self.selected = True
                self.mem_pointer = each
                self.sel_pointer = each
                break

        # and shift to the correct structure
        if self.selected:
            return self.mem_pointer['response']
        else:
            return "6AX2"

    def command(self, apdu):
        """

        :param apdu:
        :return:
        """
        completed = False
        response = None
        if 'file' in self.sel_pointer:
            for each in self.sel_pointer['file']:  # multiple applets, each just 1 entry point
                if re.match(each['item'], apdu):
                # if apdu == each['item']:
                    response = each['response']
                    self.mem_pointer = each
                    self.sel_pointer = each
                    completed = True
                    break
        if not completed and 'data' in self.mem_pointer:
            for each in self.mem_pointer['data']:
                if re.match(each['item'], apdu):
                    # if apdu == each['item']:
                    response = each['response']
                    completed = True
                    break
        if not completed and 'mffile' in self.sel_pointer:
            for each in self.sel_pointer['mffile']:
                if re.match(each['item'], apdu):
                    response = each['response']
                    completed = True
                    self.mem_pointer = each
                    break

        if completed and response:
            return response
        else:
            return "6AX3"

    def execute(self, apdu):
        """

        :param apdu:
        :type apdu: str
        :return:
        """
        apdu = ''.join(apdu.split()).upper()
        if (not self.selected) and (not self.root(apdu)):
            return '6AXX'
        else:
            self.selected = True

            if self.root(apdu):
                self.dir = True
                return self.select_applet(apdu)
            else:
                return self.command(apdu)



