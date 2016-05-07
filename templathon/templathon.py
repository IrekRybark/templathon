"""
Package: templathon
Unit: main

The script generates an output based on set of content templates and .csv file with data.
"""

from sys import argv
import pandas as pd
import os
from config import Config
from case_generator import CaseGenerator, CaseValues

__version__ = "0.1.0"

class GenOuptut:
    """
    Script generates a file based on list of test cases (csv) and part templates.

    The templates consist of header template and detail templates.
    Template may have number of placeholders in a form of ##placeholder_name##, which are replaced using
    values from .csv file.  The placeholder_name is derived from .csv file column name.
    """

    def __init__(self, test_case_file):
        """
        Constructor
        :param test_case_file: file name with the test cases
        :return: nothing
        """
        self.test_case_file = test_case_file
        # for configuration, use the same file name as test case file
        self.config_file_name = test_case_file.replace('.csv', '.config')

        self.cfg = Config(self.config_file_name)
        self.cfg.get_config()

        self.template_parts = self.cfg.template_parts

    def inc_config_seq(self):
        self.cfg.out_seq_num += 1
        self.cfg.set_config_seq(self.cfg.out_seq_num)
        return self.cfg.out_seq_num

    def proc_test_case(self, test_case, test_case_val, out_dir=''):
        """ Concatenate all templates and merge values into a single file
        :param test_case:
        :param test_case_val:
        :param out_dir: directory to store individual PO files
        :return:
        """

        r = test_case_val.field_dict

        # merge values into all case templates
        test_lines = []
        for tp in self.template_parts:  # for each template part
            for sfx in [""] + self.cfg.suffixes:  # for each suffix
                templ_col = "". join([tp, sfx])
                if templ_col in r:  # if the template column is in the data file
                    test_lines = test_lines + test_case.merge_template_values(r[templ_col], sfx, r)

        # renumber line tags in the transaction
        line_num = 1
        trans_lines_num = []
        for l in test_lines:
            l_repl = l.replace('##line_num##', str(line_num))
            if l != l_repl:
                line_num += 1

            # replace all the global tags
            for g in self.cfg.global_tags:
                l_repl = l_repl.replace(''.join(['##', g, '##']), self.cfg.global_tags[g])

            trans_lines_num.append(l_repl)

        # save test case files separately if directory provided
        if out_dir != "":
            output_file = "/".join([out_dir, ".".join([r["seq"], "txt"])])
            # print("output: ", output_file)
            if os.path.isfile(output_file):
                os.remove(output_file)
            with open(output_file, "at") as fout:
                for l in trans_lines_num:
                    fout.write(l)

        return trans_lines_num

    def verify_output(self, out_file):
        """
        Make sure that there are no not-replaced tags.  Look for tag delimiters
        :param out_file:
        :return: noting
        :raises: ValueError
        """

        for line in out_file:
            if self.cfg.tag_delimiter in out_file:
                raise ValueError("Tag delimiter found in the output file. Line: ", line)

    def process_test_cases(self):
        seq = self.inc_config_seq()

        # read the control dataset
        case_df = pd.read_csv("/".join([self.cfg.input_dir, self.cfg.input_file_name]),
                              dtype=self.cfg.input_field_types,
                              index_col=False, skipinitialspace=True, skip_blank_lines=True)

        output_file_name = self.cfg.output_file_name_format.format(seq)
        print("Generating file: ", output_file_name)
        # process all the test cases - merge into a single output file
        with open("/".join([self.cfg.output_dir, output_file_name]), 'w') as outfile:

            outlines = []

            if self.cfg.test_setup_file != "":
                print("Processing setup file: ", self.cfg.test_setup_file)
                template_path = '/'.join([self.cfg.template_dir, self.cfg.test_setup_file])
                with open(template_path, "rt") as fin:
                    for l in fin:
                        outlines.append(l)

            print("Processing test cases:")
            for r in case_df.iterrows():
                if not pd.isnull(r[1][0]):
                    print("Case #{0}".format(r[1][0]))
                    tc_val = CaseValues(r[1], case_df.columns)
                    tc = CaseGenerator(self.cfg, tc_val, seq)
                    trans_lines = self.proc_test_case(tc, tc_val)
                    for l in trans_lines:
                        outlines.append(l)

            if self.cfg.test_teardown_file != "":
                print("Processing teardown file: ", self.cfg.test_teardown_file)
                template_path = '/'.join([self.cfg.template_dir, self.cfg.test_teardown_file])
                with open(template_path, "rt") as fin:
                    for l in fin:
                        outlines.append(l)

            self.verify_output(outlines)

            for ol in outlines:
                outfile.write(ol)


def main():

    if len(argv) > 2:
        raise Exception('Too many arguments.')

    if len(argv) < 2:
        raise Exception('Missing parameters: test_case_file')

    test_case_file = argv[1]

    gen = GenOuptut(test_case_file)
    gen.process_test_cases()

if __name__ == "__main__":
    main()
