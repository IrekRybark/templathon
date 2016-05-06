"""
Package: templathon
Unit: case_generator

Unit implements merging template files with values
"""

class CaseValues:
    """
    The class encapsulates all the test case values in dictionary
    """

    def __init__(self, row, cols):
        """ Map test case fields into a dictionary
        :param row: test case row
        :param cols: list of columns in the dictionary
        :return: dictionary with test case values
        """
        self.field_dict = {}
        for c in range(len(cols)):
            self.field_dict[cols[c]] = row[c]


class CaseGenerator:
    """
    The class encapsulate a single test case generation functionality
    """

    def __init__(self, cfg, test_case_vals, seq):
        self.cfg = cfg

    def get_fld_suffix(self, fld):
        """ Get field suffix by checking against list of suffixes
        :param fld: field name
        """
        suffix = ""
        for s in self.cfg.suffixes:
            s_index = fld.find(s)
            if s_index >= 0:  # suffix found
                suffix = s
                break
        return suffix

    def merge_line_values(self, line, values, suffix=''):
        """ Merge field values into the line
        If suffix provided, try to match suffixed fields.
        :param line: template line with placeholders to be substituted
        :param values: dictionary of field values
        :param suffix: current suffix to be considered (can be empty)
        :return: line with substituted placeholders
        """
        for fld in values:
            fs = self.get_fld_suffix(fld)

            placeholder = ""
            if suffix == "":
                # consider only non-suffixed fields
                if fs == "":
                    placeholder = fld
            else:
                # consider non-suffixed and matching suffix fields
                if fs == "":
                    placeholder = fld
                elif fs == suffix:
                    placeholder = fld.replace(fs, "", 1)  # remove suffix to locate placeholder
            if placeholder != "":
                line = line.replace("".join(['##', placeholder, '##']), str(values[fld]))
        return line

    def merge_template_values(self, template_input, template_suffix, vals):
        """ Merge values into a single template
        :param template_input: template part (header, line, etc.) file
        :param template_suffix: suffix corresponding to template part
        :param vals:
        :return:
        """
        # merge all templates
        part_lines = []
        if template_input == template_input:
            template_path = '/'.join([self.cfg.template_dir, template_input])
            with open(template_path, "rt") as fin:
                for line in fin:
                    line = self.merge_line_values(line, vals, template_suffix)
                    part_lines.append(line)
        return part_lines

