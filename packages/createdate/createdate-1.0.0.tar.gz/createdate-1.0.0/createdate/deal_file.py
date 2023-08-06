# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import xlrd
import logging
import datetime
import ConfigParser
from jinja2 import Environment, FileSystemLoader, BaseLoader

BaseDir = os.path.dirname(__file__)
reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger('Excel to xml Data')
year = datetime.datetime.now().strftime("%Y")
logging.basicConfig(level=logging.INFO)

class value():
    def __init__(self):
        self.RunTest = "RunTest"
        self.format_date = "%Y-%m-%d %H:%M:%S"
        self.log_path = os.path.join(BaseDir, "log.txt")
        self.url = "http://docs.jinkan.org/docs/jinja2/templates.html#autoescape-overrides"

class Config():
    def __init__(self):
        self.years = "2020"
        self.cases_counts = "50"
        self.conf_dict = {}
        self.file_path = os.path.join(BaseDir, "config.ini")
        self.is_dswitch_server_name = "DSwitchServer"
        self.format_type = {"x": ["x", "xml"], "j": ["j", "json"]}
        self.file_format = "xml"
        self.project_name = ""
        self.is_dswitch_server = ""
        self.file_name = ""
        self.sheet_name = ""
        self.excel_path = ""

    def clean(self):
        self.is_dswitch_server_name = ""
        self.is_dswitch_server = ""
        self.file_name = ""
        self.sheet_name = ""
        self.file_format = "xml"

    def connection(self):
        config = ConfigParser.ConfigParser()
        config.read(self.file_path)
        return config

    def get_options(self):
        sections = self.connection().sections()
        for section in sections:
            self.conf_dict[section] = self.connection().options(section)


class Excel():
    def __init__(self, config):
        self.config = config
        self.V = value()

    def _get_sheet(self, config):
        return xlrd.open_workbook(os.path.join(BaseDir, config.excel_path)).sheet_by_name(config.sheet_name)

    def get_sheet_data(self, config):
        sheet_datas = []
        nrows = int(self._get_sheet(config).nrows)
        for row in range(nrows):
            rows_value = self._get_sheet(config).row_values(row)
            sheet_datas.append(rows_value)
        return sheet_datas

    def deal_code(self, value):
        if type(value) is unicode:
            return value.encode("utf-8").strip()
        elif type(value) is float:
            return value
        else:
            return value

    @staticmethod
    def clean_rows(sheet_values):
        data_lists = []
        for values in sheet_values:
            lists = []
            for value in values:
                if value:
                    lists.append(value)
            if len(lists) > 0:
                data_lists.append(values)
        return data_lists

    def deal_sheet_data(self, config):
        datas_list = []
        sheet_datas = self.get_sheet_data(config)
        keys = sheet_datas[0]
        if str(keys[0]) != self.V.RunTest:
            keys[0] = self.V.RunTest
        sheet_values = sheet_datas[1:]
        for values in Excel.clean_rows(sheet_values):
            data_dict = {}
            for key, value in zip(keys, values):
                if str(key) == "":
                    output = "第 %s 列为空" % str([index + 1 for index, key in enumerate(keys) if str(key) == ""][0])
                    raise Exception(output)
                key = self.deal_code(key)
                value = self.deal_code(value)
                if isinstance(value, str):
                    if value.startswith("{") and value.endswith("}"):
                        data_dict[key] = eval(value)
                    elif value.startswith("[") and value.endswith("]"):
                        data_dict[key] = eval(value)
                    else:
                        data_dict[key] = value
                elif isinstance(value, float):
                    data_dict[key] = value
            datas_list.append(data_dict)
        return datas_list

class TestTemplate(object):
    def __init__(self, config):
        self.config = config

    def Render_Template_To_File(self, template_path, context, outputfile):
        if type(context) is unicode:
            context = eval(context)
        if os.path.isfile(template_path):
            fstring = self._FileSystemLoader(template_path, context)
        else:
            fstring = self._StringLoader(template_path, context)
        if self.config.file_format in self.config.format_type["x"]:
            self.write_file(outputfile, fstring)
        elif self.config.file_format in self.config.format_type["j"]:
            try:
                json_outputfile = os.path.splitext(outputfile)[0] + ".json"
                root_text = self.get_root_text(fstring)
                string = str(root_text).replace("<bodys>", "").replace("</bodys>", "")
                s = eval(string)
                json.dump(set(s), open(json_outputfile, 'wb'), ensure_ascii=False, sort_keys=True, indent=4)
            except Exception, e:
                pass
        else:
            self.write_file(outputfile, fstring)

    def write_file(self, file_path, fstring):
        with open(file_path, "w") as f:
            f.write(fstring)
            f.close()

    def get_root_text(self, string):
        from lxml import etree
        tree = etree.XML(string)
        root = tree.find(".")
        return root.text

    def _StringLoader(self, myString, context):
        try:
            template = Environment(loader=BaseLoader, trim_blocks=True, lstrip_blocks=True).from_string(myString)
            result = template.render(context).encode('utf-8')
            return result
        except Exception, e:
            return e

    def _FileSystemLoader(self, temp, context):
        try:
            temp_dir = os.path.dirname(temp)
            temp_file = os.path.basename(temp)
            env = Environment(loader=FileSystemLoader(temp_dir), trim_blocks=True, lstrip_blocks=True)
            template = env.get_template(temp_file)
            result = template.render(context).encode('utf-8')
            return result
        except Exception, e:
            return e

class deal():
    def __init__(self, config):
        self.config = config
        self.template = TestTemplate(config)
        self.excel = Excel(config)
        self.V = value()

    def is_channel_dir(self, outputTestDir, source_file, content):
        if os.path.isdir(os.path.join(outputTestDir, self.config.is_dswitch_server_name)):
            self.template.Render_Template_To_File(os.path.join(BaseDir, source_file), content,
                                                  os.path.join(os.path.join(outputTestDir, self.config.is_dswitch_server_name),
                                                               source_file))
        else:
            os.makedirs(os.path.join(outputTestDir, self.config.is_dswitch_server_name))
            self.template.Render_Template_To_File(os.path.join(BaseDir, source_file), content,
                                                  os.path.join(os.path.join(outputTestDir, self.config.is_dswitch_server_name),
                                                               source_file))

    def is_provider_dir(self, outputTestDir, source_file, content):
        if os.path.isdir(outputTestDir):
            self.template.Render_Template_To_File(os.path.join(BaseDir, source_file), content,
                                                  os.path.join(outputTestDir, source_file))
        else:
            os.makedirs(outputTestDir)
            self.template.Render_Template_To_File(os.path.join(BaseDir, source_file), content,
                                                  os.path.join(outputTestDir, source_file))

    def channel_or_provider(self, config, content):
        outputDir = os.path.join(BaseDir, config.project_name)
        outputTestDir = os.path.join(outputDir, content[self.V.RunTest])
        if config.is_dswitch_server.strip() == "true":
            self.is_channel_dir(outputTestDir, config.file_name, content)
        else:
            self.is_provider_dir(outputTestDir, config.file_name, content)

    def deal_data(self, config, content, key):
        run_cases = str(content[self.V.RunTest]).split("=") or str(content[self.V.RunTest]).split(":")
        if len(run_cases) == 1:
            self.channel_or_provider(config, content)
            dealfile().write_log(self.V.log_path, "{}: {}--->{}".format(key, content[self.V.RunTest], content))
        elif len(run_cases) == 2:
            for eq_content in self.excel.deal_sheet_data(config)[:int(config.cases_counts)]:
                if run_cases[1] == eq_content[self.V.RunTest]:
                    eq_content[self.V.RunTest] = run_cases[0]
                    self.channel_or_provider(config, eq_content)
                    dealfile().write_log(self.V.log_path, "{}: {}--->{}".format(key, eq_content[self.V.RunTest], eq_content))
        elif len(run_cases) > 2:
            raise Exception("length > 2, check the {}".format(self.V.RunTest))


    def write_data_to_file(self, config, key):
        logging.info("{}".format(key))
        for content in self.excel.deal_sheet_data(config)[:int(self.config.cases_counts)]:
            match = re.match("TC.*", content[self.V.RunTest])
            if match:
                self.deal_data(config, content, key)


class dealfile(value):
    @staticmethod
    def write_log(path, string):
        with open(path, "a+") as f:
            f.write(string)
            f.close()

    @staticmethod
    def truncate_log(path):
        with open(path, "w") as f:
            f.truncate()
            f.close()

    @staticmethod
    def compare():
        now = datetime.datetime.now().strftime(value().format_date)
        d1 = datetime.datetime.strptime(now, value().format_date)
        d2 = datetime.datetime.strptime('{}-12-12 11:59:59'.format(Config().years), value().format_date)
        delta = d1 - d2
        if int(delta.days) < 0:
            return True
        else:
            return False

def main():
    config = Config()
    config.get_options()
    for key, values in config.conf_dict.items():
        if str(key).lower() == "config":
            config.excel_path = config.connection().get(key, "excel_path")
            config.project_name = config.connection().get(key, "project_name")
    for key, values in config.conf_dict.items():
        if str(key).lower() != "config":
            for v in values:
                if hasattr(config, v):
                    setattr(config, v, config.connection().get(key, v))
            deal(config).write_data_to_file(config, key)
            config.clean()

if __name__ == "__main__":
    try:
        logging.info("begin")
        dealfile().truncate_log(value().log_path)
        main()
    except Exception, e:
        logging.info(e)
    logging.info(value().url)
    logging.info("done")
