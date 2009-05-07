import ConfigParser
from builder.Tasks import TASKS


class Config(object):

    def __init__(self, configFilePath):
        self._configFilePath = configFilePath
        self.LoadSettings()


    def LoadSettings(self):
        """
        Load the ini file and set all options.
        """
        configParser = ConfigParser.ConfigParser()
        configParser.read(self._configFilePath)
        for task in TASKS:
            section = task.GetId()
            if not configParser.has_section(section):
                continue
            options = configParser.options(section)
            for option in options:
                if option == "enabled":
                    task.enabled = eval(configParser.get(section, "enabled"))
                else:
                    task.options[option] = configParser.get(section, option)


    def SaveSettings(self):
        """
        Save all options to the ini file.
        """
        config = ConfigParser.ConfigParser()
        # make ConfigParser case-sensitive
        config.optionxform = str
        config.read(self._configFilePath)
        for task in TASKS:
            section = task.GetId()
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, "enabled", task.enabled)
        configFile = open(self._configFilePath, "w")
        config.write(configFile)
        configFile.close()

