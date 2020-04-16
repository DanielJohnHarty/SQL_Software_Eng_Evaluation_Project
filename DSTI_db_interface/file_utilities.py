import re



def is_permitted_filename(filename:str)->bool:
    """
    Returns True if passed filename is compatible 
    with permitted_filename_regex_pattern (defined below):
    """
    # Any patterns of characters a-z, _ or 0-9
    permitted_filename_regex_pattern = \
        r'^[A-Za-z0-9_.]+$'

    file_extention_ok = \
        filename.lower().endswith('.csv')

    filename_characterset_ok = \
        re.match(permitted_filename_regex_pattern, filename)
    
    if file_extention_ok and filename_characterset_ok:
        result = True
    else:
        result = False
    
    return result