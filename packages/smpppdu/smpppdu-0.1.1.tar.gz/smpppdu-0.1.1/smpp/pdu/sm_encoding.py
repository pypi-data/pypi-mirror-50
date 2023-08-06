"""
Copyright 2009-2010 Mozes, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import io
import struct
from typing import Tuple, Optional

from smpp.pdu.gsm_encoding import UserDataHeaderEncoder
from smpp.pdu.gsm_types import InformationElementIdentifier
from smpp.pdu.pdu_types import *

ShortMessageString = namedtuple('ShortMessageString', 'bytes, str, udh')


class SMStringEncoder(object):
    userDataHeaderEncoder = UserDataHeaderEncoder()

    def decode_SM(self, pdu):
        data_coding = pdu.params['data_coding']
        # TODO - when to look for message_payload instead of short_message??
        (smBytes, udhBytes, smStrBytes) = self.split_SM(pdu)
        udh = self.decodeUDH(udhBytes)

        if data_coding.scheme == DataCodingScheme.DEFAULT:
            unicode_str = None
            if data_coding.schemeData == DataCodingDefault.SMSC_DEFAULT_ALPHABET:
                unicode_str = str(smStrBytes, 'ascii')
            elif data_coding.schemeData == DataCodingDefault.IA5_ASCII:
                unicode_str = str(smStrBytes, 'ascii')
            elif data_coding.schemeData == DataCodingDefault.UCS2:
                unicode_str = str(smStrBytes, 'UTF-16BE')
            elif data_coding.schemeData == DataCodingDefault.LATIN_1:
                unicode_str = str(smStrBytes, 'latin_1')
            if unicode_str is not None:
                return ShortMessageString(smBytes, unicode_str, udh)

        raise NotImplementedError(f"I don't know what to do!!! Data coding {data_coding}")

    def contains_UDH(self, pdu):
        if EsmClassGsmFeatures.UDHI_INDICATOR_SET in pdu.params['esm_class'].gsmFeatures:
            return True
        return False

    def is_concatenated_SM(self, pdu):
        return self.get_concatenated_SM_info_element(pdu) is not None

    def get_concatenated_SM_info_element(self, pdu):
        (smBytes, udhBytes, smStrBytes) = self.split_SM(pdu)
        udh = self.decodeUDH(udhBytes)
        if udh is None:
            return None
        return self.find_concatenated_SM_info_element(udh)

    def find_concatenated_SM_info_element(self, udh):
        iElems = [iElem for iElem in udh if iElem.identifier in (
            InformationElementIdentifier.CONCATENATED_SM_8BIT_REF_NUM,
            InformationElementIdentifier.CONCATENATED_SM_16BIT_REF_NUM
        )]
        assert len(iElems) <= 1
        if len(iElems) == 1:
            return iElems[0]
        return None

    def decodeUDH(self, udhBytes: bytes):
        if udhBytes is not None:
            return self.userDataHeaderEncoder.decode(io.BytesIO(udhBytes))
        return None

    def split_SM(self, pdu) -> Tuple[bytes, Optional[bytes], bytes]:
        short_message: bytes = pdu.params['short_message']
        if self.contains_UDH(pdu):
            if len(short_message) == 0:
                raise ValueError("Empty short message")
            header_len = struct.unpack('!B', short_message[0:1])[0]
            if header_len + 1 > len(short_message):
                raise ValueError(
                    f'Invalid header len ({header_len}). Longer than short_message len ({len(short_message)}) + 1')
            return (
                short_message,
                short_message[:header_len + 1],
                short_message[header_len + 1:]
            )
        return short_message, None, short_message
