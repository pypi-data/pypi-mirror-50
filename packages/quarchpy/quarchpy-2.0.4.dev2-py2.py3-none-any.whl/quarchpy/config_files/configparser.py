import logging
import os, os.path, sys
import inspect
import quarchpy.config_files
from enum import Enum

'''
Describes a unit for time measurement
'''
class TimeUnit(Enum):
    "UNSPECIFIED",
    "nS",
    "uS",
    "mS",
    "S",

'''
Described a precise time duration for settings
'''
class TimeValue:
    time_value = None
    time_unit = None

    def __init__ (self):
        time_value = 0
        time_unit = TimeUnit.UNSPECIFIED

'''
Describes a single range element if a module range parameter
'''
class ModuleRangeItem:
    min_value = 0
    max_value = 0
    step_value = 0
    unit = None

    def __init__ (self):
        min_value = 0
        max_value = 0
        step_value = 0
        unit = None

'''
Describes a range of values which can be applied to the settings on a module
This is generally a time value, but can be anything
'''
class ModuleRangeParam:
    ranges = None
    range_unit = None

    def __init__ (self):
        ranges = list()
        range_unit = None

    '''
    Adds a new range item, which is verified to match any existing items
    '''
    def add_range (self, new_range_item):
        value = true        

        if (self.range_unit is None):
            self.range_unit = new_range_item.range_unit
        # For additional ranges, verify the unit is the same
        else:
            if (new_range_item.range_unit != self.range_unit):
                value = False

        # Add the new range if all is OK
        if (valid):
            ranges.append (new_range_item)
            return True
        else:
            return False

    '''
    Internal method to find the closest value within a given range
    '''
    def _get_closest_value (self, range_item, value):

        # Check for out of rang values
        if (value < range_item.min_value):
            result = range_item.min_value
        elif (value > range_item.max_value):
            result = range_item.max_value
        # Else value is in range
        else:
            low_steps = int((float(value) / float(range_item.step_value)) + 0.5)
            low_value = int(low_steps * range_item.step_value)
            high_value = int(low_value + range_item.step_value)

        # Get the closest step
        if (abs(low_value - value) < abs(high_value - value)):
            result - low_value
        else:
            result - high_value

        return result

    '''
    Returns the closest allowable value to the given number
    '''
    def get_closest_value (self, value):
        valid_value = -sys.maxsize -1
        in_range = list()
        running_error = sys.maxsize
        curr_error = 0
        possible_value = 0

        if (self.ranges is None or len(self.ranges) == 0):
            raise ValueError ("No ranges available to check against")
        else:
            # Loop through the ranges
            for i in self.ranges:
                # Find the closest value in this range
                possible_value = self._get_closest_value (i, value)
                curr_error = abs(possible_value - value)

                # Store if it is closer than the previous tests
                if (curr_error < running_error):
                    running_error = curr_error
                    valid_value = possible_value

        return possible_value

    '''
    Returns the largest allowable value
    '''
    def get_max_value (self):
        valid_value = -sys.maxsize -1

        for i in self.ranges:
            if (i.max_value > valid_value):
                valid_value = i.max_value

        return valid_value

    '''
    Returns the smallest allowable value
    '''
    def get_max_value (self):
        valid_value = sys.maxsize

        for i in self.ranges:
            if (i.min_value < valid_value):
                valid_value = i.min_value

        return valid_value

'''
Describes a switched signal on a breaaker module
'''
class BreakerModuleSignal:
    name = None
    parameters = None

    def __init__ (self):
        self.name = None
        self.parameters = dict ()

'''
Describes a signal group on a breaker module
'''
class BreakerSignalGroup:
    name = None
    signals = None

    def __init__ (self):
        self.name = None
        self.signals = list ()

'''
Describes control sources on a breaker module
'''
class BreakerSource:
    number = None
    type = None
    default_initial_delay = None
    initial_delay_limits = None


    def __init__ (self):
        self.name = None
        self.signals = list ()
        self.default_initial_delay = TimeValue()
        self.initial_delay_limits = ModuleRangeParam()

'''
Describes a Torridon hot-swap/breaker module and all its capabilities
'''
class TorridonBreakerModule:
    signals = None
    groups = None
    sources = None

    def __init__ (self):
        self.signals = list ()
        self.groups = list ()
        self.sources = list ()

'''
Returns the path to the most recent config file that is compatible with the given module.  Module information can be passed in as
an existing IDN string from the "*IDN?" command or via an open connection to the module
'''
def get_config_path_for_module (idn_string = None, module_connection = None):
    device_number = None
    device_fw = None
    device_fpga = None
    result = True

    # Check for invalid parameters
    if (idn_string is None and module_connection is None):
        logging.error("Invalid parameters, no module information given")
        result = False
    else:
        # Prefer IDN string, otherwise use the module connection to get it now
        if (idn_string is None):
            idn_string = module_connection.sendCommand ("*IDN?")

        # Split the string into lines and run through them to locate the parts we need
        idn_lines = idn_string.upper().split("\n")
        for i in idn_lines:
            # Part number of the module
            if "PART#:" in i:
                device_number = i[6:].strip()
            # Firmware version
            if "PROCESSOR:" in i:
                device_fw = i[10:].strip()
                pos = device_fw.find (",")
                if (pos == -1):
                    device_fw = None
                else:
                    device_fw = device_fw[pos+1:].strip()
            # FPGA version
            if "FPGA 1:" in i:
                device_fpga = i[7:].strip()
                pos = device_fpga.find (",")
                if (pos == -1):
                    device_fpga = None
                else:
                    device_fpga = device_fpga[pos+1:].strip()

        # Log the failure if we did not get all the info needed
        if (device_number is None):
            result = False
            logging.error("Unable to indentify module - no module number")
        if (device_fw is None):
            logging.error("Unable to indentify module - no firmware version")
            result = False
        if (device_fpga is None):
            logging.error("Unable to indentify module - no FPGA version")
            result = False

        # If we got all the data, use it to find the config file
        config_matches = list()
        if (result == False):
            return None
        else:
            # Get all config files as a dictionary of their basic header information
            config_file_header = get_config_file_headers ()

            # Loop through each config file header
            for i in config_file_header:
                # If the part number can be used with this config file
                if (check_part_number_matches(i, device_number)):
                    # Check if the part number is not seperately excluded
                    if (check_part_exclude_matches(i, device_number) == False):
                        # Check Firmware can be used with this config file
                        if (check_fw_version_matches(i, device_fw)):
                            # Check if FPGA version matches
                            if (check_fpga_version_matches(i, device_fpga)):
                                # Store this as a matching config file for the device
                                logging.debug("Located matching config file: " + i["Config_Path"])
                                config_matches.append (i)

            # Sort the config files into preferred order
            if (len(config_matches) > 0):
                config_matches = sort_config_headers (config_matches)
                return config_matches[0]["Config_Path"]
            else:
                logging.error("No matching config files were found for this module")
                return None


'''                
Processes all config files to get a list of dictionaries of basic header information
'''
def get_config_file_headers ():

    # Get the path to the config files folder
    folder_path = os.path.dirname (os.path.abspath(quarchpy.config_files.__file__))
    files_found = list()
    config_headers = list()

    # Iterate through all files, including and recursive folders
    for search_path, search_subdirs, search_files in os.walk(folder_path):
        for name in search_files:
            if (".qfg" in name.lower()):
                files_found.append (os.path.join(search_path, name))

    # Now parse the header section of each file into the list of dictionaries
    for i in files_found:
        read_file = open (i, "r")
        next_line, read_point = read_config_line (read_file)
        if ("@CONFIG" in next_line):
            # Read until we find the @HEADER section
            while ("@HEADER" not in next_line):
                next_line, read_point = read_config_line (read_file)
            # Parse the header section data
            new_config = parse_section_to_dictionary (read_file)
            # Store the file path as an item
            new_config["Config_Path"] = i
            config_headers.append (new_config)
        else:
            logging.error("Config file parse failed, @CONFIG section not found")

    return config_headers

'''
Reads the next line of the file which contains usable data, skips blank lines and comments
'''
def read_config_line (read_file):
    while(True):
        start_pos = read_file.tell()
        line = read_file.readline ()

        if (line == None):
            return None
        else:
            line = line.strip()
            if (len(line) > 0):
                if (line[0] != '#'):
                    return line, start_pos

'''
Reads the next section of the file (up to the next @ line) into a dictionary
'''
def parse_section_to_dictionary (read_file):
    elements = dict()

    # Read until we find the end
    while(True):
        # Read a line and the read point in the file
        line, start_pos = read_config_line (read_file)
        # If this is the start of a new section, set the file back one line and stop
        if (line.find ('@') == 0):
            read_file.seek (start_pos)
            break
        # Else we parse the line into a new dictionary item
        else:
            pos = line.find ('=')
            if (pos == -1):
                logging.error("Config line does not meet required format of x=y: " + line)
                return None
            else:
                elements[line[:pos]] = line[pos+1:]

    return elements


'''
Returns true of the config header is allowed for use on a module with the given part number
'''
def check_part_number_matches(config_header, device_number):

    # Strip down to the main part number, removing the version
    pos = device_number.find ("-")
    if (pos != -1):
        pos = len(device_number) - pos
        short_device_number = device_number[:-pos]
    # Fail on part number not including the version section
    else:
        logging.debug("Part number did not contain the version :" + device_number)
        return False

    # Loop through the allowed part numbers
    allowed_device_numbers = config_header["DeviceNumbers"].split(",")
    for dev in allowed_device_numbers:
        pos = dev.find('-');
        if (pos != -1):
            pos = len(dev) - pos
            short_config_number = dev[:-pos]
            if ("xx" in dev):
                any_version = True;
            else:
                any_version = False;               
        # Fail if config number is invalid
        else:
            logging.debug("Part number in config file is not in the right format: " + dev)
            return False;

        # Return true if we find a number that matches in full, or one which matches in part and the any_version flag was present in the config file
        if (device_number == dev or (short_device_number == short_config_number and any_version)):
            return True

    # False as the fallback if no matching part numbers were found
    return False

'''
Returns true of the config header does not contain an exclusion for the given device number
'''
def check_part_exclude_matches(config_header, device_number):

    # Strip down to the main part number, removing the version
    pos = device_number.find ("-")
    if (pos != -1):
        pos = len(device_number) - pos
        short_device_number = device_number[:-pos]
    # Fail on part number not including the version section
    else:
        logging.debug("Part number did not contain the version :" + device_number)
        return False

    # Check that the part number is fully qualified (will not be the case if the serial number is not set)
    if ("?" in device_number):
        logging.debug("Part number is not fully qualified :" + device_number)
        return False

    # Loop through the excluded part numbers
    allowed_device_numbers = config_header["DeviceNumbersExclude"].split(",")
    for dev in allowed_device_numbers:
        # Skip blanks (normally due to no part numbers specified)
        if (len(dev) == 0):
            continue

        pos = dev.find('-');
        if (pos != -1):
            pos = len(dev) - pos
            short_config_number = dev[:-pos]
            if ("xx" in dev):
                any_version = True;
            else:
                any_version = False;               
        # Fail if config number is invalid
        else:
            logging.debug("Exclude part number in config file is not in the right format: " + dev)
            return False;

        # Return true if we find a number that matches in full, or one which matches in part and the any_version flag was present in the config file
        if (device_number == dev or (short_device_number == short_config_number and any_version)):
            return True

    # False as the fallback if no matching part numbers were found
    return False

'''
Checks that the firmware version on the config header allows the version on the device
'''
def check_fw_version_matches(config_header, device_fw):
    if float(device_fw) >= float(config_header["MinFirmwareRequired"]):
        return True
    else:
        return False

'''
Checks that the FPGA version on the config header allows the version on the device
'''
def check_fpga_version_matches(config_header, device_fpga):
    if (float(device_fpga) >= float(config_header["MinFpgaRequired"])):
        return True
    else:
        return False

'''
Sorts a list of config headers into order, where the highest firmware version file is at the top of the list
This is the one which would normally be chosen
'''
def sort_config_headers (config_matches):
    return sorted (config_matches, key=lambda i: i["MinFirmwareRequired"], reverse=True)

def parse_config_file (file):

    config_dict = dict ()
    section_dict = dict ()
    section_name = None
    read_file = open (file, "r")
    
    # Start with the first line, as this is not useful info anyway
    line, read_pos = read_config_line (read_file)
    # Loop through the file, reading all lines
    while (line is not None):
        line, read_pos = read_config_line (read_file)

        # If this is the start of the first section, store its name
        if ("@" in line and section_name is None):
            section_name = line[1:]
        # If a new section, store the old one first
        elif ("@" in line):
            config_dict[section_name] = section_dict
            section_name = line[1:]
            section_dict = dict ()
        # Else this must be a standard data line
        else:
            # Special case for module signals, create as a BreakerSignal class type
            if ("SIGNALS" in section_name):
                signal = BreakerModuleSignal ()
                line_value = line.split(',')                
                # Loop to add the optional parameters
                for i in line_value:
                    pos = i.find('=')
                    line_name = i[pos+1:]
                    line_param = i[:pos]
                    if ("Name" in line_name):
                        signal.name = line_name
                    else:
                        signal.parameters[line_name] = line_param

            else:
                pos = line.find('=')
                line_value = line[pos+1:]
                line_name = line[:pos]
                section_dict[line_name] = line_value


    