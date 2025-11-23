import os
import sys
from PIL import Image

def number2roman_numerals (integernumber:int):
    """
    Convert an integer to its Roman numeral representation.

    Args:
        integernumber (int): The integer to convert.

    Returns:
        str: Roman numeral string equivalent of the integer.
    """
    roman_numerals = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'),
        (1, 'I')]
    result = ""
    for value, symbol in roman_numerals:
        while integernumber >= value:
            result += symbol
            integernumber -= value
    return result

def number2alphabetic (integernumber:int):
	result = ""
	while integernumber > 0:
		integernumber -= 1
		result = chr((integernumber % 26) + 97) + result
		integernumber //= 26
	return result

def read_settings(settings_path):
	settings = {'Theme': 'dark_red', 'Font': 'First', 'Number_Format': 'Numbers'}
	if os.path.exists(settings_path):
		with open(settings_path, "r") as file:
			for line in file:
				key, value = line.strip().split(":")
				settings[key.strip()] = value.strip()
	else:
		with open(settings_path, "w") as file:
			for key, value in settings.items():
				file.write(f"{key}:{value}\n")

	return settings


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')  
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def change_image_color(input_image_path, output_image_path, target_hex_color, new_hex_color):
    
    target_color = hex_to_rgb(target_hex_color)
    new_color = hex_to_rgb(new_hex_color)

    image = Image.open(input_image_path).convert("RGBA")

    new_image = Image.new("RGBA", image.size)

    pixels = image.getdata()

    new_data = []
    for pixel in pixels:
        if pixel[:3] == target_color:
            new_data.append(new_color + (pixel[3],))
        else:
            new_data.append(pixel)

    new_image.putdata(new_data)
    
    new_image.save(output_image_path)


def load_activity_names(filename):
    """
    Load activity names from a text file. This function reads each line in the provided text file, strips any leading/trailing whitespace,
    and returns a list of activity names.

    Args:
        filename (str): The path to the text file containing activity names.

    Returns:
        list: A list of activity names read from the file. 
              Returns an empty list if the file is not found.

    Raises:
        FileNotFoundError: If the specified file cannot be found.

    
    """
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def create_day_times_list(max_hours):
    """
    Create a list of time slots for each hour of the day in 15-minute intervals.

    Args:
        max_hours (int): The maximum number of hours to include in the time list.

    Returns:
        list: A list of time strings formatted as 'hour:minute',  
              ranging from 00:00 to max_hours: 45 in 15-minute intervals.
    
    Example:
        If max_hours is 2, the list will contain:  
        ['0:00', '0:15', '0:30', '0:45', '1:00', '1:15', '1:30', '1:45', '2:00', '2:15', '2:30', '2:45']
    """
    timelist = []
    for hour in range(0, max_hours + 1):
        for minute in [0, 15, 30, 45]:
            timelist.append(f"{hour}:{minute:02}")
    return timelist

