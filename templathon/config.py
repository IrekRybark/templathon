"""
Package: templathon
Unit: config

Unit parses configuration and stores values in the object.
Also, provides general access to the configuration, like incrementing counters
"""

import configparser

class Config:

    def __init__(self, config_file_name):
        self.config_file_name = "".join([config_file_name, ".config"])

        self.input_file_name = ""
        self.input_field_types = {}

        self.out_seq_num = 0
        self.output_file_name_format = ""

        self.input_dir = ""
        self.output_dir = ""
        self.template_dir = ""

        self.test_setup_file = ""
        self.test_teardown_file = ""
        self.suffixes = ""
        self.template_parts = ""
        self.tag_delimiter = ""

        self.global_tags = {}

    def get_config(self):
        """ Retrieve configuration """
        config = configparser.ConfigParser()
        config.read(self.config_file_name)

        self.input_file_name = config['Input']['datafile']
        self.input_field_types = {}
        for field in config['InputFieldTypes']:
            self.input_field_types[field] = config['InputFieldTypes'][field]

        self.out_seq_num = int(config['Output']['SeqNum'])
        self.output_file_name_format = config['Output']['OutputFileNameFormat']

        self.input_dir = config['Directories']['input']
        self.output_dir = config['Directories']['output']
        self.template_dir = config['Directories']['templates']

        self.test_setup_file = config['Templates']['test_setup_template']
        self.test_teardown_file = config['Templates']['test_teardown_template']
        self.suffixes = config['Templates']['template_suffixes'].split(",") # [_1,_2,_3]
        # the order of template parts reflects sequence of merging them
        self.template_parts = config['Templates']['template_parts'].split(",") # template_header,template_detail,template_finalization
        self.tag_delimiter = config['Templates'].get('tag_delimiter', '##')

        self.global_tags = {}
        for tag in config['GlobalTags']:
            self.global_tags[tag] = config['GlobalTags'][tag]


    def set_config_seq(self, seq):
        """
        Save value of sequential number in the configuration
        :param seq: new value for sequential number
        :return: nothing
        """
        config = configparser.ConfigParser()
        config.read(self.config_file_name)
        config['Output']['SeqNum'] = "{0}".format(seq)
        with open(self.config_file_name, 'w') as configfile:
            config.write(configfile)
