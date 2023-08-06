"""
Small configuration parser
written for small projects
ENJOY ;)
Author: Miasnenko Dmitry
"""
from typing import List, Tuple

class ConfigurationParser:

    def __init__(self, **params):
        import re
        self.settings = {
            "filename"           : "config.ini",                    # file to be read
            "splitter"           : "|",                             # splitter between var and value
            "bloc_sides"         : {"left" : "[", "right" : "]"},   # sides near bloc name
            "encoding"           : "utf-8",                         # file encoding
            "readed"             : False,						    # was file readed
            "bloc_pattern"       : None,						    # pattern of the bloc
            "comment_pattern"    : None,						    # comment pattern
            "comment_start"      : ">",							    # stert of the comment 
            "block_name_pattern" : re.compile("[a-zA-Z0-9_ -]{1,}") # bloc name pattern
        }
        # updating settings
        self.settings.update(**params)

        # creating re patterns
        sides = self.settings["bloc_sides"]
        temp_pattern = '[][a-zA-Z0-9_ ]{1,}{}'
        temp_pattern = temp_pattern.replace("[]", f"[{sides['left']}]", 1)
        temp_pattern = temp_pattern.replace("{}", f"[{sides['right']}]", 1)
        bloc_pattern = re.compile(temp_pattern)
        temp_pattern = '[a-zA-Z0-9_ ]{0,}'
        start = self.settings["comment_start"]
        comment_pattern = re.compile(f"[{start}]" + temp_pattern)
        self.settings["bloc_pattern"] = bloc_pattern
        self.settings["comment_pattern"] = comment_pattern
        
        # reading file and making cache for easy access later
        self.cache = self.__read_all()

    def __str__(self):
    	from pprint import pprint
    	pprint(self.cache)
    	return ""

    def __is_comment(self, line:str) -> bool:
    	"""
    	Checks if line is a comment
    	param : line: str: line to be checked
    	return: bool
    	"""
        pattern = self.settings["comment_pattern"]
        return bool(pattern.fullmatch(line))

    def __is_bloc(self, line:str) -> bool:
    	"""
    	Checks if line is a bloc
		param : line: str: line to be checked
		return: bool
    	"""
        pattern = self.settings["bloc_pattern"]
        return bool(pattern.fullmatch(line))

    def __get_bloc_name(self, line:str) -> str:
    	"""
    	Returning bloc name
		param : line: str: line from which to take name
		return: str
    	"""
        pattern = self.settings["block_name_pattern"]
        return pattern.search(line.strip())[0]

    def __get_bloc_names(self) -> List[str]:
    	"""
    	Taking bloc names
    	return: List[str] names
    	"""
        names = []
        filename = self.settings["filename"]
        encoding = self.settings["encoding"]
        with open(filename, "r", encoding=encoding) as file:
            for line in file:
                line = line.strip()
                if self.__is_bloc(line):
                    name = self.__get_bloc_name(line)
                    names.append(name)
            return names

    def __read_all(self) -> dict:
    	"""
    	Reading all blocks
		return: dict
    	"""
    	# Checking if the file
    	# has already been checked
        if self.settings["readed"]:
            return self.cache

        # setting reading bloc to True
        self.settings["readed"] = True
        
        # taking settings
        filename = self.settings["filename"]
        encoding = self.settings["encoding"]
        splitter = self.settings["splitter"]
        
        # taking all bloc names
        self.bloc_names = self.__get_bloc_names()
        
        All = {}
        
        # WOHOOO 
        # Start reading
        with open(filename, "r", encoding=encoding) as file:
            for name in self.bloc_names:
                All[name] = {}
                READING = False
                for line in file:
                    line = line.strip()
                    if READING:
                        if not self.__is_bloc(line) and not self.__is_comment(line) and line:
                            var_name, value = line.split(splitter)
                            All[name][var_name.strip()] = value.strip()
                        elif self.__is_bloc(line):
                            READING = False
                    else:
                        if self.__is_bloc(line):
                            current_name = self.__get_bloc_name(line)
                            READING = (current_name == name)
            return All

    def get_all(self) -> dict:
    	"""
    	returns readed file
    	"""
        return self.cache

    def take_from_bloc(self, block_name:str, var:str) -> str:
    	"""
		Taking variable from bloc
		param  : block_name: str: name of the bloc
		param  : var       : str: variable
		return : variable
    	"""
        return self.cache[block_name][var]

    def take(self, var:str) -> str:
    	"""
    	Taking from file 
    	first match to the
    	variable
		param: var: str: variable to be taken
    	"""
        for bloc in self.cache:
            for _var in self.cache[bloc]:
                if _var == var:
                    return self.cache[bloc][var]

    def read_blocs(self, *names:Tuple[str]) -> dict:
    	"""
    	Reading vars from taken blocs
    	param: names: Tuple[str]: names of the blocs
    	"""
        result = {}
        for bloc_name in self.cache:
            if bloc_name in names:
                result.update(self.cache[bloc_name])
        return result

    def get_all_blocs(self) -> List[str]:
    	"""
    	Taking names of all blocs
    	return: List[str]
    	"""
        return list(self.cache.keys())

    def get_all_variables(self) -> dict:
    	"""
    	Getting all variables in the file
    	warning: uncritical:
    		if variables have same names
    		the last one will be taken
    	return: dict
    	"""
        result = {}
        for bloc in self.cache:
            result.update(self.cache[bloc])
        return result
