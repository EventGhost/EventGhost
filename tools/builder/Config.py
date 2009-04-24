import ConfigParser
import builder


class Option(object):
    """
    Represents a single option of the Config class
    """
    def __init__(self, name, label, value):
        self.name = name
        self.label = label
        self.value = value
            
    

class Config(object):

    def __init__(self, configFilePath):
        self._configFilePath = configFilePath
        self._options = []
        self._optionsDict = {}
        for task in builder.TASKS:
            if task.option is None:
                continue
            self.AddOption(task.option, task.description, task.default)
        self.LoadSettings()
        
        
    def __getattr__(self, name):
        return self._optionsDict[name].value
    
    
    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            self._optionsDict[name].value = value
    
    
    def __iter__(self):
        return self._options.__iter__()
    
    
    def AddOption(self, name, label, value):
        """ Adds an option to the configuration. """
        option = Option(name, label, value)
        self._options.append(option)
        self._optionsDict[name] = option
    
    
    def LoadSettings(self):
        """
        Load the ini file and set all options.
        """ 
        configParser = ConfigParser.ConfigParser()
        configParser.read(self._configFilePath)
        for option in self._options:
            if configParser.has_option("Settings", option.name):
                value = configParser.get("Settings", option.name)
                if value == "True":
                    value = True
                elif value == "False":
                    value = False
                option.value = value
            
            
    def SaveSettings(self):
        """
        Save all options to the ini file.
        """
        config = ConfigParser.ConfigParser()
        # make ConfigParser case-sensitive
        config.optionxform = str
        config.read(self._configFilePath)
        if not config.has_section("Settings"):
            config.add_section("Settings")
        for option in self._options:
            config.set("Settings", option.name, option.value)
        configFile = open(self._configFilePath, "w")
        config.write(configFile)
        configFile.close()
        


