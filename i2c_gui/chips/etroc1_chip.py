#############################################################################
# zlib License
#
# (C) 2023 Cristóvão Beirão da Cruz e Silva <cbeiraod@cern.ch>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#############################################################################

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..connection_controller import Connection_Controller

from .base_chip import Base_Chip
from ..gui_helper import GUI_Helper

import tkinter as tk
import tkinter.ttk as ttk  # For themed widgets (gives a more native visual to the elements)
import logging

etroc1_version = "0.0.1"

register_model = {
    "Array_Reg_A": {  # Address Space (i.e. separate I2C memory spaces)
        "Memory Size": 48,
        "Register Blocks": {
            "Registers": {  # Register Block (i.e. group of registers to be handled as one unit)
                "Base Address": 0x0000,
                "Registers": {
                    "Reg_A_00": {
                        "offset": 0x0000,
                        "default": 0xF8,
                    },
                    "Reg_A_01": {
                        "offset": 0x0001,
                        "default": 0x37,
                    },
                    "Reg_A_02": {
                        "offset": 0x0002,
                        "default": 0xFF,
                    },
                    "Reg_A_03": {
                        "offset": 0x0003,
                        "default": 0xFF,
                    },
                    "Reg_A_04": {
                        "offset": 0x0004,
                        "default": 0x11,
                    },
                    "Reg_A_05": {
                        "offset": 0x0005,
                        "default": 0x01,
                    },
                    "Reg_A_06": {
                        "offset": 0x0006,
                        "default": 0x00,
                    },
                    "Reg_A_07": {
                        "offset": 0x0007,
                        "default": 0x01,
                    },
                    "Reg_A_08": {
                        "offset": 0x0008,
                        "default": 0x00,
                    },
                    "Reg_A_09": {
                        "offset": 0x0009,
                        "default": 0x00,
                    },
                    "Reg_A_0A": {
                        "offset": 0x000A,
                        "default": 0x00,
                    },
                    "Reg_A_0B": {
                        "offset": 0x000B,
                        "default": 0x02,
                    },
                    "Reg_A_0C": {
                        "offset": 0x000C,
                        "default": 0x08,
                    },
                    "Reg_A_0D": {
                        "offset": 0x000D,
                        "default": 0x20,
                    },
                    "Reg_A_0E": {
                        "offset": 0x000E,
                        "default": 0x80,
                    },
                    "Reg_A_0F": {
                        "offset": 0x000F,
                        "default": 0x00,
                    },
                    "Reg_A_10": {
                        "offset": 0x0010,
                        "default": 0x02,
                    },
                    "Reg_A_11": {
                        "offset": 0x0011,
                        "default": 0x08,
                    },
                    "Reg_A_12": {
                        "offset": 0x0012,
                        "default": 0x20,
                    },
                    "Reg_A_13": {
                        "offset": 0x0013,
                        "default": 0x80,
                    },
                    "Reg_A_14": {
                        "offset": 0x0014,
                        "default": 0x00,
                    },
                    "Reg_A_15": {
                        "offset": 0x0015,
                        "default": 0x02,
                    },
                    "Reg_A_16": {
                        "offset": 0x0016,
                        "default": 0x08,
                    },
                    "Reg_A_17": {
                        "offset": 0x0017,
                        "default": 0x20,
                    },
                    "Reg_A_18": {
                        "offset": 0x0018,
                        "default": 0x80,
                    },
                    "Reg_A_19": {
                        "offset": 0x0019,
                        "default": 0x00,
                    },
                    "Reg_A_1A": {
                        "offset": 0x001A,
                        "default": 0x02,
                    },
                    "Reg_A_1B": {
                        "offset": 0x001B,
                        "default": 0x08,
                    },
                    "Reg_A_1C": {
                        "offset": 0x001C,
                        "default": 0x20,
                    },
                    "Reg_A_1D": {
                        "offset": 0x001D,
                        "default": 0x80,
                    },
                    "Reg_A_1E": {
                        "offset": 0x001E,
                        "default": 0xFF,
                    },
                    "Reg_A_1F": {
                        "offset": 0x001F,
                        "default": 0xFF,
                    },
                    "Reg_A_20": {
                        "offset": 0x001F,
                        "default": 0x00,
                        "read_only": True,
                    },
                }
            },
        }
    },
    "Array_Reg_B": {
        "Memory Size": 32,
        "Register Blocks": {
            "Registers": {
                "Base Address": 0x0000,
                "Registers": {
                    "Reg_B_00": {
                        "offset": 0x0000,
                        "default": 0x1C,
                    },
                    "Reg_B_01": {
                        "offset": 0x0001,
                        "default": 0x01,
                    },
                    "Reg_B_02": {
                        "offset": 0x0002,
                        "default": 0x00,
                    },
                    "Reg_B_03": {
                        "offset": 0x0003,
                        "default": 0x09,
                    },
                    "Reg_B_04": {
                        "offset": 0x0004,
                        "default": 0x00,
                    },
                    "Reg_B_05": {
                        "offset": 0x0005,
                        "default": 0x03,
                    },
                    "Reg_B_06": {
                        "offset": 0x0006,
                        "default": 0x41,
                    },
                    "Reg_B_07": {
                        "offset": 0x0007,
                        "default": 0x38,
                    },
                    "Reg_B_08": {
                        "offset": 0x0008,
                        "default": 0x18,
                    },
                    "Reg_B_09": {
                        "offset": 0x0009,
                        "default": 0x18,
                    },
                    "Reg_B_0A": {
                        "offset": 0x000A,
                        "default": 0x38,
                    },
                    "Reg_B_0B": {
                        "offset": 0x000B,
                        "default": 0x77,
                    },
                }
            },
        }
    },
    "Full_Pixel": {
        "Memory Size": 48,
        "Register Blocks": {
            "Registers": {
                "Base Address": 0x0000,
                "Registers": {
                    "Reg_00": {
                        "offset": 0x0000,
                        "default": 0x2C,
                    },
                    "Reg_01": {
                        "offset": 0x0001,
                        "default": 0x2C,
                    },
                    "Reg_02": {
                        "offset": 0x0002,
                        "default": 0x2C,
                    },
                    "Reg_03": {
                        "offset": 0x0003,
                        "default": 0x2C,
                    },
                    "Reg_04": {
                        "offset": 0x0004,
                        "default": 0x2C,
                    },
                    "Reg_05": {
                        "offset": 0x0005,
                        "default": 0x2C,
                    },
                    "Reg_06": {
                        "offset": 0x0006,
                        "default": 0x2C,
                    },
                    "Reg_07": {
                        "offset": 0x0007,
                        "default": 0x2C,
                    },
                    "Reg_08": {
                        "offset": 0x0008,
                        "default": 0x2C,
                    },
                    "Reg_09": {
                        "offset": 0x0009,
                        "default": 0x2C,
                    },
                    "Reg_0A": {
                        "offset": 0x000A,
                        "default": 0x2C,
                    },
                    "Reg_0B": {
                        "offset": 0x000B,
                        "default": 0x2C,
                    },
                    "Reg_0C": {
                        "offset": 0x000C,
                        "default": 0x2C,
                    },
                    "Reg_0D": {
                        "offset": 0x000D,
                        "default": 0x2C,
                    },
                    "Reg_0E": {
                        "offset": 0x000E,
                        "default": 0x2C,
                    },
                    "Reg_0F": {
                        "offset": 0x000F,
                        "default": 0x2C,
                    },
                    "Reg_10": {
                        "offset": 0x0010,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_11": {
                        "offset": 0x0011,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_12": {
                        "offset": 0x0012,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_13": {
                        "offset": 0x0013,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_14": {
                        "offset": 0x0014,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_15": {
                        "offset": 0x0015,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_16": {
                        "offset": 0x0016,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_17": {
                        "offset": 0x0017,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_18": {
                        "offset": 0x0018,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_19": {
                        "offset": 0x0019,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1A": {
                        "offset": 0x001A,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1B": {
                        "offset": 0x001B,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1C": {
                        "offset": 0x001C,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1D": {
                        "offset": 0x001D,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1E": {
                        "offset": 0x001E,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1F": {
                        "offset": 0x001F,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_20": {
                        "offset": 0x0020,
                        "default": 0x2C,
                        "read_only": True,
                    },
                }
            },
        }
    },
    "TDC_Test_Block": {
        "Memory Size": 48,
        "Register Blocks": {
            "Registers": {
                "Base Address": 0x0000,
                "Registers": {
                    "Reg_00": {
                        "offset": 0x0000,
                        "default": 0x2C,
                    },
                    "Reg_01": {
                        "offset": 0x0001,
                        "default": 0x2C,
                    },
                    "Reg_02": {
                        "offset": 0x0002,
                        "default": 0x2C,
                    },
                    "Reg_03": {
                        "offset": 0x0003,
                        "default": 0x2C,
                    },
                    "Reg_04": {
                        "offset": 0x0004,
                        "default": 0x2C,
                    },
                    "Reg_05": {
                        "offset": 0x0005,
                        "default": 0x2C,
                    },
                    "Reg_06": {
                        "offset": 0x0006,
                        "default": 0x2C,
                    },
                    "Reg_07": {
                        "offset": 0x0007,
                        "default": 0x2C,
                    },
                    "Reg_08": {
                        "offset": 0x0008,
                        "default": 0x2C,
                    },
                    "Reg_09": {
                        "offset": 0x0009,
                        "default": 0x2C,
                    },
                    "Reg_0A": {
                        "offset": 0x000A,
                        "default": 0x2C,
                    },
                    "Reg_0B": {
                        "offset": 0x000B,
                        "default": 0x2C,
                    },
                    "Reg_0C": {
                        "offset": 0x000C,
                        "default": 0x2C,
                    },
                    "Reg_0D": {
                        "offset": 0x000D,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_0E": {
                        "offset": 0x000E,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_0F": {
                        "offset": 0x000F,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_10": {
                        "offset": 0x0010,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_11": {
                        "offset": 0x0011,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_12": {
                        "offset": 0x0012,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_13": {
                        "offset": 0x0013,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_14": {
                        "offset": 0x0014,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_15": {
                        "offset": 0x0015,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_16": {
                        "offset": 0x0016,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_17": {
                        "offset": 0x0017,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_18": {
                        "offset": 0x0018,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_19": {
                        "offset": 0x0019,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1A": {
                        "offset": 0x001A,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1B": {
                        "offset": 0x001B,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1C": {
                        "offset": 0x001C,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1D": {
                        "offset": 0x001D,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1E": {
                        "offset": 0x001E,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1F": {
                        "offset": 0x001F,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_20": {
                        "offset": 0x0020,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_21": {
                        "offset": 0x0021,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_22": {
                        "offset": 0x0022,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_23": {
                        "offset": 0x0023,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_24": {
                        "offset": 0x0024,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_25": {
                        "offset": 0x0025,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_26": {
                        "offset": 0x0026,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_27": {
                        "offset": 0x0027,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_28": {
                        "offset": 0x0028,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_29": {
                        "offset": 0x0029,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_2A": {
                        "offset": 0x002A,
                        "default": 0x2C,
                        "read_only": True,
                    },
                    "Reg_2B": {
                        "offset": 0x002B,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_2C": {
                        "offset": 0x002C,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_2D": {
                        "offset": 0x002D,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_2E": {
                        "offset": 0x002E,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_2F": {
                        "offset": 0x002F,
                        "default": 0x2C,
                        "read_only": True,
                        "display": False,
                    },
                }
            },
        }
    },
}

register_decoding = {
    "Array_Reg_A": {  # Address Space (i.e. separate I2C memory spaces)
        "Register Blocks":{
            "Registers": {  # Register Block (i.e. group of registers to be handled as one unit)
                "PLL_ClkGen_disCLK": {
                    "bits": 1,
                    "position": [("Reg_A_00", "0", "0")]  # The tuple should be 1st position is the register, 2nd position the bits in the register, 3rd position the bits in the value
                },
            },
        }
    },
    "Array_Reg_B": {  # Address Space (i.e. separate I2C memory spaces)
        "Register Blocks":{
            "Registers": {  # Register Block (i.e. group of registers to be handled as one unit)
                "PLL_ClkGen_disCLK": {
                    "bits": 1,
                    "position": [("Reg_B_00", "0", "0")]  # The tuple should be 1st position is the register, 2nd position the bits in the register, 3rd position the bits in the value
                },
            },
        }
    },
    "Full_Pixel": {  # Address Space (i.e. separate I2C memory spaces)
        "Register Blocks":{
            "Registers": {  # Register Block (i.e. group of registers to be handled as one unit)
                "PLL_ClkGen_disCLK": {
                    "bits": 1,
                    "position": [("Reg_00", "0", "0")]  # The tuple should be 1st position is the register, 2nd position the bits in the register, 3rd position the bits in the value
                },
            },
        }
    },
    "TDC_Test_Block": {  # Address Space (i.e. separate I2C memory spaces)
        "Register Blocks":{
            "Registers": {  # Register Block (i.e. group of registers to be handled as one unit)
                "PLL_ClkGen_disCLK": {
                    "bits": 1,
                    "position": [("Reg_00", "0", "0")]  # The tuple should be 1st position is the register, 2nd position the bits in the register, 3rd position the bits in the value
                },
            },
        }
    },
}

class ETROC1_Chip(Base_Chip):
    def __init__(self, parent: GUI_Helper, i2c_controller: Connection_Controller):
        super().__init__(
            parent=parent,
            chip_name="ETROC1",
            version=etroc1_version,
            i2c_controller=i2c_controller,
            register_model=register_model,
            register_decoding=register_decoding
        )

        self._i2c_address_a = None
        self._i2c_address_b = None
        self._i2c_address_full_pixel = None
        self._i2c_address_tdc_test_block = None

        self.clear_tab("Empty")
        self.register_tab(
            "Graphical View",
            {
                "canvas": False,
                "builder": self.graphical_interface_builder
            }
        )
        self.register_tab(
            "Array Registers",
            {
                "canvas": True,
                "builder": self.array_register_builder
            }
        )
        self.register_tab(
            "Array Decoded",
            {
                "canvas": False,
            }
        )
        self.register_tab(
            "Full Pixel Registers",
            {
                "canvas": True,
            }
        )
        self.register_tab(
            "Full Pixel Decoded",
            {
                "canvas": False,
            }
        )
        self.register_tab(
            "TDC Test Block Registers",
            {
                "canvas": False,
            }
        )
        self.register_tab(
            "TDC Test Block Decoded",
            {
                "canvas": False,
            }
        )

    def update_whether_modified(self):
        if self._i2c_address_a is not None:
            state_a = self._address_space["Array_Reg_A"].is_modified
        else:
            state_a = None

        if self._i2c_address_b is not None:
            state_b = self._address_space["Array_Reg_B"].is_modified
        else:
            state_b = None

        if self._i2c_address_full_pixel is not None:
            state_full = self._address_space["Full_Pixel"].is_modified
        else:
            state_full = None

        if self._i2c_address_tdc_test_block is not None:
            state_tdc = self._address_space["TDC_Test_Block"].is_modified
        else:
            state_tdc = None

        state_summary = []
        if state_a is not None:
            state_summary += [state_a]
        if state_b is not None:
            state_summary += [state_b]
        if state_full is not None:
            state_summary += [state_full]
        if state_tdc is not None:
            state_summary += [state_tdc]

        if len(state_summary) == 0:
            final_state = "Unknown"
        elif len(state_summary) == 0:
            final_state = state_summary[0]
        else:
            if len(set(state_summary)) == 1: # If all elements are equal
                final_state = state_summary[0]
            elif "Unknown" in state_summary: # If at least one has unknown status, the full chip has unknown status
                final_state = "Unknown"
            elif True in state_summary: # If at least one is modified, the full chip is modified
                final_state = True
            else:
                final_state = False

        if final_state == True:
            final_state = "Modified"
        elif final_state == False:
            final_state = "Unmodified"

        self._parent._local_status_update(final_state)

    def config_i2c_address_a(self, address):
        self._i2c_address_a = address

        from .address_space_controller import Address_Space_Controller
        if "Array_Reg_A" in self._address_space:
            address_space: Address_Space_Controller = self._address_space["Array_Reg_A"]
            address_space.update_i2c_address(address)
        self.update_whether_modified()

    def config_i2c_address_b(self, address):
        self._i2c_address_b = address

        from .address_space_controller import Address_Space_Controller
        if "Array_Reg_B" in self._address_space:
            address_space: Address_Space_Controller = self._address_space["Array_Reg_B"]
            address_space.update_i2c_address(address)
        self.update_whether_modified()

    def config_i2c_address_full_pixel(self, address):
        self._i2c_address_full_pixel = address

        from .address_space_controller import Address_Space_Controller
        if "Full_Pixel" in self._address_space:
            address_space: Address_Space_Controller = self._address_space["Full_Pixel"]
            address_space.update_i2c_address(address)
        self.update_whether_modified()

    def config_i2c_address_full_pixel(self, address):
        self._i2c_address_tdc_test_block = address

        from .address_space_controller import Address_Space_Controller
        if "TDC_Test_Block" in self._address_space:
            address_space: Address_Space_Controller = self._address_space["TDC_Test_Block"]
            address_space.update_i2c_address(address)
        self.update_whether_modified()

    def graphical_interface_builder(self, frame: ttk.Frame):
        pass

    def array_register_builder(self, frame: ttk.Frame):
        frame.columnconfigure(100, weight=1)
        columns = 4

        self._ETROC2_peripheral_config_frame = self.build_block_interface(
            element=frame,
            title="Register Block A",
            internal_title="Register Block A",
            button_title="REG A",
            address_space="Array_Reg_A",
            block="Registers",
            col=100,
            row=100,
            register_columns=columns
        )

        self._ETROC2_peripheral_config_frame = self.build_block_interface(
            element=frame,
            title="Register Block B",
            internal_title="Register Block B",
            button_title="REG B",
            address_space="Array_Reg_B",
            block="Registers",
            col=100,
            row=200,
            register_columns=columns
        )