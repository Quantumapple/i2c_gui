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

import logging
import i2c_gui
import i2c_gui.chips
from i2c_gui.usb_iss_helper import USB_ISS_Helper
from i2c_gui.fpga_eth_helper import FPGA_ETH_Helper

def test_etroc2_device_memory(
        helper: i2c_gui.ScriptHelper,
        conn: i2c_gui.Connection_Controller,
        chip: i2c_gui.chips.ETROC2_Chip,
        chip_address: int = 0x72,
        ws_address: int = None,
        error_mask: dict[str, bool] = {}
    ):
    if not (i2c_gui.__no_connect__ or conn.check_i2c_device(chip_address)):
        raise RuntimeError("Unable to reach ETROC2 device")

    chip.config_i2c_address(chip_address)
    chip.config_waveform_sampler_i2c_address(ws_address)

    # Read the full chip to get the current status:
    chip.read_all()

    mask_individual_read = False
    if 'individual_read' in error_mask:
        if error_mask['individual_read']:
            mask_individual_read = True
    mask_bit_flip = False
    if 'bit_flip' in error_mask:
        if error_mask['bit_flip']:
            mask_bit_flip = True
    mask_alternating_a = False
    if 'alternating_a' in error_mask:
        if error_mask['alternating_a']:
            mask_alternating_a = True
    mask_alternating_5 = False
    if 'alternating_5' in error_mask:
        if error_mask['alternating_5']:
            mask_alternating_5 = True
    mask_set = False
    if 'set' in error_mask:
        if error_mask['set']:
            mask_set = True
    mask_clear = False
    if 'clear' in error_mask:
        if error_mask['clear']:
            mask_clear = True

    address_space_errors = {}
    from i2c_gui.chips.etroc2_chip import register_model
    for address_space in register_model:
        block_errors = {}
        for block_name in register_model[address_space]['Register Blocks']:
            if 'Indexer' in register_model[address_space]['Register Blocks'][block_name]:
                blocks = helper.get_all_indexed_blocks(register_model[address_space]['Register Blocks'][block_name]['Indexer'], block_name)
            else:
                blocks = {
                    block_name: {
                        'indexers': {}  # There are no indexers for standard blocks
                    }
                }

            block_ref_errors = {}
            for block_ref in blocks:
                # Set the indexers for the current block position (if there are any indexers)
                for indexer in blocks[block_ref]['indexers']:
                    if indexer == 'block':
                        continue
                    chip._indexer_vars[indexer]['variable'].set(blocks[block_ref]['indexers'][indexer])

                #print(block_ref)
                #print(chip._gen_block_ref_from_indexers(address_space, block_name, full_array=False))
                #print()

                block_error_summary = {}
                if not mask_individual_read:
                    block_error_summary['repeated_read'] = {'full_block': False, 'errors': []}
                if not mask_bit_flip:
                    block_error_summary['bit_flip'] = {'full_block': False, 'errors': {}}
                if not mask_alternating_a:
                    block_error_summary['alternating_a'] = {'full_block': False, 'errors': {}}
                if not mask_alternating_5:
                    block_error_summary['alternating_5'] = {'full_block': False, 'errors': {}}
                if not mask_set:
                    block_error_summary['set'] = {'full_block': False, 'errors': {}}
                if not mask_clear:
                    block_error_summary['clear'] = {'full_block': False, 'errors': {}}

                # Loop through registers and do the individual tests, keep a record of found errors
                for register_name in register_model[address_space]['Register Blocks'][block_name]['Registers']:
                    register_info = register_model[address_space]['Register Blocks'][block_name]['Registers'][register_name]
                    read_only = False
                    if 'read_only' in register_info and register_info['read_only']:
                        read_only = True

                    var = chip.get_indexed_var(address_space, block_name, register_name)

                    original_value = int(var.get(), 0)

                    if not mask_individual_read:
                        chip.read_register(address_space, block_name, register_name)
                        individual_read_value = int(var.get(), 0)
                        if individual_read_value != original_value:
                            block_error_summary['repeated_read']['errors'] += [register_name]

                    if not read_only:
                        register_modified = False

                        if not mask_bit_flip:
                            register_modified = True
                            bit_flipped_setting = original_value ^ 0xff  # Flip the bits in the register
                            var.set(str(bit_flipped_setting))
                            chip.write_register(address_space, block_name, register_name, write_check=False)
                            chip.read_register(address_space, block_name, register_name)
                            bit_flip_value = int(var.get(), 0)
                            if bit_flip_value != bit_flipped_setting:
                                block_error_summary['bit_flip']['errors'][register_name] = (bit_flipped_setting, bit_flip_value)

                        if not mask_alternating_a:
                            register_modified = True
                            var.set(str(0xaa))
                            chip.write_register(address_space, block_name, register_name, write_check=False)
                            chip.read_register(address_space, block_name, register_name)
                            alternating_a_value = int(var.get(), 0)
                            if alternating_a_value != 0xaa:
                                block_error_summary['alternating_a']['errors'][register_name] = alternating_a_value

                        if not mask_alternating_5:
                            register_modified = True
                            var.set(str(0x55))
                            chip.write_register(address_space, block_name, register_name, write_check=False)
                            chip.read_register(address_space, block_name, register_name)
                            alternating_5_value = int(var.get(), 0)
                            if alternating_5_value != 0x55:
                                block_error_summary['alternating_5']['errors'][register_name] = alternating_5_value

                        if not mask_set:
                            register_modified = True
                            var.set(str(0xff))
                            chip.write_register(address_space, block_name, register_name, write_check=False)
                            chip.read_register(address_space, block_name, register_name)
                            set_value = int(var.get(), 0)
                            if set_value != 0xff:
                                block_error_summary['set']['errors'][register_name] = set_value

                        if not mask_clear:
                            register_modified = True
                            var.set(str(0x00))
                            chip.write_register(address_space, block_name, register_name, write_check=False)
                            chip.read_register(address_space, block_name, register_name)
                            clear_value = int(var.get(), 0)
                            if clear_value != 0x00:
                                block_error_summary['clear']['errors'][register_name] = clear_value

                        if register_modified:
                            var.set(str(original_value))  # Reset back to original state once finished
                            chip.write_register(address_space, block_name, register_name, write_check=False)

                for error_type in block_error_summary:
                    if len(block_error_summary[error_type]['errors']) == len(register_model[address_space]['Register Blocks'][block_name]['Registers']):
                        block_error_summary[error_type]['full_block'] = True
                    block_error_summary[error_type]['error_count'] = len(block_error_summary[error_type]['errors'])

                block_ref_errors[block_ref] = block_error_summary

            block_errors[block_name] = {}
            for block_ref in block_ref_errors:
                for error_type in block_ref_errors[block_ref]:
                    if error_type not in block_errors[block_name]:
                        block_errors[block_name][error_type] = {
                            'error_count': 0,
                            'full_block': True,  # Assume error in full block, then deassert if not
                            'errors': {},
                        }
                    if not block_ref_errors[block_ref][error_type]['full_block']:
                        block_errors[block_name][error_type]['full_block'] = False
                    block_errors[block_name][error_type]['errors'][block_ref] = block_ref_errors[block_ref][error_type]
                    block_errors[block_name][error_type]['error_count'] += block_ref_errors[block_ref][error_type]['error_count']

        address_space_errors[address_space] = {}
        for block_name in block_errors:
            for error_type in block_errors[block_name]:
                if error_type not in address_space_errors[address_space]:
                    address_space_errors[address_space][error_type] = {
                        'error_count': 0,
                        'full_address': True,  # Assume error in full block, then deassert if not
                        'errors': {},
                    }
                if not block_errors[block_name][error_type]['full_block']:
                    address_space_errors[address_space][error_type]['full_address'] = False
                address_space_errors[address_space][error_type]['error_count'] += block_errors[block_name][error_type]['error_count']
                address_space_errors[address_space][error_type]['errors'][block_name] = block_errors[block_name][error_type]
        if len(block_errors) != len(register_model[address_space]['Register Blocks']):
            full_address_space_error = False
            for block_name in block_errors:
                if block_errors[block_name]['full_block']:
                    print("There was an issue in reading/writing the full block {} of {}, all registers and block refs of the block failed read/write.".format(block_name, address_space))
        else:
            full_address_space_error = True

        if len(block_errors) > 0:
            address_space_errors[address_space] = {
                'full_address': full_address_space_error,
                'errors': block_errors,
            }

    print(address_space_errors)
    #if len(address_space_errors) > 0:
    #    chip_errors
    # TODO: what about testing the broadcast write?

def slow(
    error_mask: dict[str, bool],
    port: str = "COM3"
    ):
    logger = logging.getLogger("Script_Logger")

    Script_Helper = i2c_gui.ScriptHelper(logger)

    conn = i2c_gui.Connection_Controller(Script_Helper)

    ## For USB ISS connection
    conn.connection_type = "USB-ISS"
    conn.handle: USB_ISS_Helper
    conn.handle.port = port
    conn.handle.clk = 100

    ## For FPGA connection (not yet fully implemented)
    #conn.connection_type = "FPGA-Eth"
    #conn.handle: FPGA_ETH_Helper
    #conn.handle.hostname = "192.168.2.3"
    #conn.handle.port = "1024"

    conn.connect()

    try:
        chip = i2c_gui.chips.ETROC2_Chip(parent=Script_Helper, i2c_controller=conn)
        test_etroc2_device_memory(Script_Helper, conn, chip,
            error_mask=error_mask,
        )
    except Exception:  # as e:
        # print("An Exception occurred:")
        # print(repr(e))
        import traceback
        traceback.print_exc()
    except:
        print("An Unknown Exception occurred")
    finally:
        conn.disconnect()

def fast(
    error_mask: dict[str, bool],
    port: str = "COM3"
    ):
    logger = logging.getLogger("Script_Logger")

    Script_Helper = i2c_gui.ScriptHelper(logger)

    conn = i2c_gui.Connection_Controller(Script_Helper)

    ## For USB ISS connection
    conn.connection_type = "USB-ISS"
    conn.handle: USB_ISS_Helper
    conn.handle.port = port
    conn.handle.clk = 100

    ## For FPGA connection (not yet fully implemented)
    #conn.connection_type = "FPGA-Eth"
    #conn.handle: FPGA_ETH_Helper
    #conn.handle.hostname = "192.168.2.3"
    #conn.handle.port = "1024"

    conn.connect()

    try:
        chip = i2c_gui.chips.ETROC2_Chip(parent=Script_Helper, i2c_controller=conn)
        #fast_test_etroc2_device_memory(Script_Helper, conn, chip,
        #    error_mask=error_mask,
        #)
    except Exception:  # as e:
        # print("An Exception occurred:")
        # print(repr(e))
        import traceback
        traceback.print_exc()
    except:
        print("An Unknown Exception occurred")
    finally:
        conn.disconnect()



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run a full test of the ETROC2 registers')
    parser.add_argument(
        '-l',
        '--log-level',
        help = 'Set the logging level. Default: WARNING',
        choices = ["CRITICAL","ERROR","WARNING","INFO","DEBUG","TRACE","DETAILED_TRACE","NOTSET"],
        default = "WARNING",
        dest = 'log_level',
    )
    parser.add_argument(
        '--log-file',
        help = 'If set, the full log will be saved to a file (i.e. the log level is ignored)',
        action = 'store_true',
        dest = 'log_file',
    )
    parser.add_argument(
        '-p',
        '--port',
        metavar = 'device',
        help = 'The port name the USB-ISS module is connected to. Default: COM3',
        default = "COM3",
        dest = 'port',
        type = str,
    )
    parser.add_argument(
        '-s'
        '--slow',
        help='Run the slow algorithm which checks the registers one by one (this can take a very long time)',
        action = 'store_true',
        dest = 'slow',
    )
    parser.add_argument(
        '--repeated-read',
        help='Enable the error check for repeated read',
        action = 'store_true',
        dest = 'individual_read',
    )
    parser.add_argument(
        '--bit-flip',
        help='Enable the error check for bit flipping',
        action = 'store_true',
        dest = 'bit_flip',
    )
    parser.add_argument(
        '--alternating-a',
        help='Enable the error check for writing the alternating bit pattern 0xAA to the registers',
        action = 'store_true',
        dest = 'alternating_a',
    )
    parser.add_argument(
        '--alternating-5',
        help='Enable the error check for writing the alternating bit pattern 0x55 to the registers',
        action = 'store_true',
        dest = 'alternating_5',
    )
    parser.add_argument(
        '--set',
        help='Enable the error check for writing the bit pattern 0xFF to the registers',
        action = 'store_true',
        dest = 'set',
    )
    parser.add_argument(
        '--clear',
        help='Enable the error check for writing the bit pattern 0x00 to the registers',
        action = 'store_true',
        dest = 'clear',
    )
    parser.add_argument(
        '--chip_address',
        help='Set the address of the ETROC chip. You can use any number that python would recognise. Default: 0x72',
        default = "0x72",
        dest = 'chip_address',
        type = str,
    )
    parser.add_argument(
        '--ws_address',
        help='Set the address of the Waveform Sampler of the ETROC chip. You can use any number that python would recognise. Default: None',
        default = None,
        dest = 'ws_address',
        type = str,
    )

    args = parser.parse_args()

    if args.log_file:
        logging.basicConfig(filename='logging.log', filemode='w', encoding='utf-8', level=logging.NOTSET)
    else:
        log_level = 90
        if args.log_level == "CRITICAL":
            log_level=50
        elif args.log_level == "ERROR":
            log_level=40
        elif args.log_level == "WARNING":
            log_level=30
        elif args.log_level == "INFO":
            log_level=20
        elif args.log_level == "DEBUG":
            log_level=10
        elif args.log_level == "TRACE":
            log_level=8
        elif args.log_level == "DETAILED_TRACE":
            log_level=5
        elif args.log_level == "NOTSET":
            log_level=0
        logging.basicConfig(format='%(asctime)s - %(levelname)s:%(name)s:%(message)s', level=log_level)
    ### Old way, do not use anymore
    #logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s:%(name)s:%(message)s')  # For very detailed output, it is probably overkill
    #logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s:%(name)s:%(message)s')

    # By default mask everything, then use command line options to enable specific ones
    error_mask = {
        'individual_read': True,
        'bit_flip': True,
        'alternating_a': True,
        'alternating_5': True,
        'set': True,
        'clear': True,
    }
    for key in error_mask:
        if hasattr(args, key):
            error_mask[key] = not getattr(args, key)

    i2c_gui.__no_connect__ = True  # Set to fake connecting to an ETROC2 device
    #i2c_gui.__no_connect_type__ = "echo"  # for actually testing readback
    #i2c_gui.__no_connect_type__ = "check"  # default behaviour

    if args.slow:
        slow(
            error_mask=error_mask,
            port=args.port,
        )
    else:
        fast(
            error_mask=error_mask,
            port=args.port,
        )