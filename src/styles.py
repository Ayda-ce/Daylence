from PyQt5.QtGui import QFont

def color_palette(theme: str = "dark_red"):
    """
    Returns a color palette dictionary for the specified theme.
    
    Args:
        theme (str): Name of the color theme. Default is "dark_red".
        
    Returns:
        dict: Color values for various UI elements in the specified theme.
              Returns dark_red theme if specified theme not found.
    """
    themes = {
        'dark_red': {
            'Text': '#FAF6F3',
            'Table': '#363636',
            'Hover': '#AD0E0E',
            'Header': '#B53534',
            'Splash': '#640408',
            'Button': '#B53534',
            'Background': '#2A2A2A',
            'HeaderText': '#FFFFFF'
        },
        'dark_green': {  
            'Text': '#FAF6F3',  
            'Table': '#363636',  
            'Hover': '#0EAD0E',  
            'Header': '#2CAD2C',  
            'Splash': '#046404',  
            'Button': '#2CAD2C',  
            'Background': '#1F1F1F',  
            'HeaderText': '#FFFFFF'  
        },
        'dark_blue': {  
            'Text': '#FFFFFF',  
            'Table': '#1C1C2A',  
            'Hover': '#0E4DAE',  
            'Header': '#003366',  
            'Splash': '#001F4D',  
            'Button': '#003366',  
            'ButtonText': '#FFFFFF',  
            'Background': '#1A1A2E',  
            'HeaderText': '#FFFFFF'  
        },
        'light': {
            "Text": "#4B5563",
            "Table": "#F1F0E8",
            "Hover": "#89A8B2",
            "Header": "#B3C8CF",
            "Splash": "#E5E1DA",
            "Button": "#B3C8CF",
            "ButtonText": "#FFFFFF",
            "Background": "#F1F0E8",
            "HeaderText": "#4B5563",
            "HoverText": "#FFFFFF"
        },
        'dark_mode': {
            "Text": "#EEEEEE",
            "Table": "#31363F",
            "Hover": "#76ABAE",
            "Header": "#76ABAE",
            "Splash": "#31363F",
            "Button": "#76ABAE",
            "ButtonText": "#EEEEEE",
            "Background": "#222831",
            "HeaderText": "#EEEEEE",
            "HoverText": "#EEEEEE",
            "Border": "#EEEEEE"
        },
        'dark_pink': {
            'Text': '#FAF6F3',
            'Table': '#3D2A30',
            'Hover': '#D5006D',
            'Header': '#C2185B',
            'Splash': '#880E4F',
            'Button': '#C2185B',
            'Background': '#2A2A2A',
            'HeaderText': '#FFFFFF'
        },
        'the_best_theme': {
            'Text': '#FFFFFF',
            'Table': '#444444',
            'Hover': '#FF5722',
            'Header': '#FF9800',
            'Splash': '#FF9800',
            'Button': '#FF9800',
            'Background': '#212121',
            'HeaderText': '#FFFFFF'
        },
        'optimal_theme': {
            "Text": "#504B38",
            "Table": "#F8F3D9", 
            "Hover": "#B9B28A",
            "Header": "#EBE5C2",
            "Splash": "#F8F3D9",
            "Button": "#EBE5C2",
            "ButtonText": "#504B38",
            "Background": "#F8F3D9",
            "HeaderText": "#504B38",
            "HoverText": "#504B38",
        },
        'dark_optimal_theme': {
            "Text": "#ECDFCC",       
            "Table": "#3C3D37",      
            "Hover": "#697565",       
            "Header": "#697565",      
            "Splash": "#3C3D37",       
            "Button": "#697565",      
            "Background": "#181C14",  
            "HeaderText": "#ECDFCC"
        }
    }
    return themes.get(theme, "dark_red")

def font_families(font_set_name: str = "First"):
    """
    Returns a dictionary of QFont objects for different UI elements.
    
    Args:
        font_set_name (str): Name of the font set ("First", "Second", or "Third").
                            Default is "First".
                            
    Returns:
        dict: Dictionary containing QFont objects for various UI elements.
              Returns "First" font set if specified set not found.
    """
    fonts = {
        "First": {
            "Main_Font": QFont('Consolas', 22, QFont.Bold),
            "Table": QFont('Consolas', 12),
            "Button": QFont('Consolas', 16, QFont.Bold),
            "Text": QFont('Consolas', 14),
            "Table_Header": QFont('Consolas', 14, QFont.Bold),
            "Group_Box": QFont('Consolas', 12, QFont.Bold),
            "Table_View_Header": QFont('Consolas', 10, QFont.Bold)
        },
        "Second": {
            "Main_Font": QFont('Arial', 22, QFont.Bold),
            "Table": QFont('Arial', 12),
            "Button": QFont('Arial', 16, QFont.Bold),
            "Text": QFont('Arial', 14),
            "Table_Header": QFont('Arial', 14, QFont.Bold),
            "Group_Box": QFont('Arial', 12, QFont.Bold),
            "Table_View_Header": QFont('Arial', 10, QFont.Bold)
        },
        "Third": {
            "Main_Font": QFont('Roboto', 22, QFont.Bold),
            "Table": QFont('Roboto', 12),
            "Button": QFont('Roboto', 16, QFont.Bold),
            "Text": QFont('Roboto', 14),
            "Table_Header": QFont('Roboto', 14, QFont.Bold),
            "Group_Box": QFont('Roboto', 12, QFont.Bold),
            "Table_View_Header": QFont('Roboto', 10, QFont.Bold)
        }
    }

    return fonts.get(font_set_name, fonts["First"])