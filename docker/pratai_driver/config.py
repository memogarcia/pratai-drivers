import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("/etc/pratai/pratai-driver.conf")


def parse_config(section):
    """Parse a config file into a dict
    :param section:
    :return:
    """
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: {0}".format(option))
        except Exception:
            print("exception on {0}!".format(option))
            dict1[option] = None
    return dict1
