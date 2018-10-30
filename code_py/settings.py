import base64
import linecache

import configparser
import os
import stat
import socket
import subprocess

import sys

from code_py import sys_logging
import logging

logger = logging.getLogger(__name__)

class Settings():
    SECTION_SAP = 'Sap'
    SECTION_ORACLE = 'Oracle'
    SECTION_ORACLE_SAP = 'OracleSap'
    SECTION_LOGS = 'Logs'
    SECTION_EMAIL = 'Email'
    SECTION_WEB = 'Web'
    SECTION_QUERY_BUILDER = 'QueryBuilder'
    SECTION_GREENPLUM = 'Greenplum'
    SECTION_FOLDERS = 'Folders'
    SECTION_DEPLOYMENT = 'Deployment'
    SECTION_SAP_JAVA = 'SapJava'

    def __init__(self, config_path, instance_type, contour):
        config_parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config_files = [os.path.join(config_path, 'default.conf')] + [
            os.path.join(config_path, conf_name + '.conf') for conf_name in (contour, 'secret')]
        config_parser.read(config_files)
     #   if contour == 'prod_main':
     #       config_parser.set(self.SECTION_SAP, 'Host', get_curr_cms_addr('bicms.gtm.tcsbank.ru'))
     # when gtm will be work with sap return
        # ---------------------------------------SECTION_SAP---------------------------------------
        self.sap_host = config_parser.get(self.SECTION_SAP, 'Host').lower()
        self.sap_port = config_parser.getint(self.SECTION_SAP, 'Port')
        self.sap_username = config_parser.get(self.SECTION_SAP, 'UserName')
        self.sap_password = base64.b64decode(config_parser.get(self.SECTION_SAP, 'Password')).decode('utf-8')
        # ---------------------------------------SECTION_ORACLE--------------------------------------
        self.oracle_home = config_parser.get(self.SECTION_ORACLE, 'ORACLE_HOME')
        # ---------------------------------------SECTION_ORACLE_SAP--------------------------------------
        self.oracle_sap_tns = config_parser.get(self.SECTION_ORACLE_SAP, 'Tns')
        self.oracle_sap_user = config_parser.get(self.SECTION_ORACLE_SAP, 'User')
        self.oracle_sap_password = base64.b64decode(config_parser.get(self.SECTION_ORACLE_SAP, 'Password')).decode(
            'utf-8')
        self.oracle_aud_schema = config_parser.get(self.SECTION_ORACLE_SAP, 'SchemaAudit')
        self.oracle_cms_schema = config_parser.get(self.SECTION_ORACLE_SAP, 'SchemaCms')

        # ---------------------------------------SECTION_FOLDERS---------------------------------------
        self.base_directory = config_parser.get(self.SECTION_FOLDERS, 'BaseDir')
        self.data_folder = config_parser.get(self.SECTION_FOLDERS, 'BaseDataDir')
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
            os.chmod(self.data_folder, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        self.log_folder = config_parser.get(self.SECTION_FOLDERS, 'BaseLogDir')
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
            os.chmod(self.log_folder, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        self.temporary_data = config_parser.get(self.SECTION_FOLDERS, 'DataDir')
        if not os.path.exists(self.temporary_data):
            os.makedirs(self.temporary_data)
            os.chmod(self.temporary_data, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        self.full_log_dir = config_parser.get(self.SECTION_FOLDERS, 'ProgramFullLogDir')
        if not os.path.exists(self.full_log_dir):
            os.makedirs(self.full_log_dir)
            os.chmod(self.full_log_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        self.short_log_dir = config_parser.get(self.SECTION_FOLDERS, 'ProgramShortLogDir')
        if not os.path.exists(self.short_log_dir):
            os.makedirs(self.short_log_dir)
            os.chmod(self.short_log_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        # ---------------------------------------SECTION_LOGS---------------------------------------
        self.logging_program_log_full = config_parser.get(self.SECTION_LOGS, 'ProgramLogsFull')
        self.logging_program_log_short = config_parser.get(self.SECTION_LOGS, 'ProgramLogsShort')
        self.logging_file_config = config_parser.get(self.SECTION_LOGS, 'LoggingConf')
        # ---------------------------------------SECTION_EMAIL--------------------------------------
        self.email_smtp_server_name = config_parser.get(self.SECTION_EMAIL, 'SmtpServerName')
        self.email_from_addr = config_parser.get(self.SECTION_EMAIL, 'FromAddr')
        self.email_to_addr_users = config_parser.get(self.SECTION_EMAIL, 'UserEmails').replace(' ', '').split(',')
        self.email_to_addr_admins = config_parser.get(self.SECTION_EMAIL, 'AdminEmails').replace(' ', '').split(',')
        self.email_subject = config_parser.get(self.SECTION_EMAIL, 'EmailSubject')
        self.email_subject_admin_notification = config_parser.get(self.SECTION_EMAIL, 'EmailSubjectAdminNotification')
        # ---------------------------------------SECTION_WEB---------------------------------------
        self.auth = config_parser.get(self.SECTION_WEB, 'Auth')
        self.sap_web_username = config_parser.get(self.SECTION_WEB, 'UserName')
        self.sap_web_password = base64.b64decode(config_parser.get(self.SECTION_WEB, 'Password')).decode('utf-8')
        self.url_logon = config_parser.get(self.SECTION_WEB, 'UrlLogon')
        self.url_logoff = config_parser.get(self.SECTION_WEB, 'UrlLogoff')
        self.url_documents = config_parser.get(self.SECTION_WEB, 'UrlDocuments')
        self.url_document = config_parser.get(self.SECTION_WEB, 'UrlDocument')
        self.url_dataproviders = config_parser.get(self.SECTION_WEB, 'UrlDataproviders')
        self.url_infostore = config_parser.get(self.SECTION_WEB, 'UrlInfostore')
        self.url_publication_launch = config_parser.get(self.SECTION_WEB, 'UrlPublicationLaunch')
        self.url_publication_schedule = config_parser.get(self.SECTION_WEB, 'UrlPublicationSchedule')
        self.url_dataprovider_specification = config_parser.get(self.SECTION_WEB, 'UrlDataproviderSpecification')
        # ---------------------------------------QueryBuilder---------------------------------------
        self.java_libs = config_parser.get(self.SECTION_QUERY_BUILDER, 'JavaLibs')
        self.query_builder_libs = config_parser.get(self.SECTION_QUERY_BUILDER, 'QueryBuilderLibs')
        self.query_builder_jar = os.path.join(self.query_builder_libs,
                                              config_parser.get(self.SECTION_QUERY_BUILDER, 'MainJar'))
        self.query_builder_class = config_parser.get(self.SECTION_QUERY_BUILDER,
                                                     'MainClass')
        self.query_builder_user = config_parser.get(self.SECTION_QUERY_BUILDER, 'User')
        self.query_builder_password = base64.b64decode(
            config_parser.get(self.SECTION_QUERY_BUILDER, 'Password')).decode('utf-8')
        self.query_builder_auth = config_parser.get(self.SECTION_QUERY_BUILDER, 'Auth')
        self.query_builder_server = config_parser.get(self.SECTION_QUERY_BUILDER, 'Server')
        # ---------------------------------------Greenplum---------------------------------------
        self.gp_login = config_parser.get(self.SECTION_GREENPLUM, 'Login')
        self.gp_path = config_parser.get(self.SECTION_GREENPLUM, 'Path')
        self.gp_port = config_parser.get(self.SECTION_GREENPLUM, 'Port')
        self.gp_db = config_parser.get(self.SECTION_GREENPLUM, 'Database')
        self.gp_schema = config_parser.get(self.SECTION_GREENPLUM, 'Schema')
        self.gp_password = base64.b64decode(config_parser.get(self.SECTION_GREENPLUM, 'Password')).decode('utf-8')
        self.select_grants_to = config_parser.get(self.SECTION_GREENPLUM, 'SelectGrantsTo')
        # ----------------------------------------Instance------------------------------------------
        self.instance_type = instance_type
        self.deployment_id = config_parser.get(self.SECTION_DEPLOYMENT, 'Deployment_id')
        # ----------------------------------------SapJava------------------------------------------
        self.sap_java_path = config_parser.get(self.SECTION_SAP_JAVA, 'SapJavaPath')
        self.sap_java_connect_dir = config_parser.get(self.SECTION_SAP_JAVA, 'ConnectivityDir')
        self.sap_java_libs = config_parser.get(self.SECTION_SAP_JAVA, 'SapJavaLibs')
        self.sap_sngl_unv_jar = config_parser.get(self.SECTION_SAP_JAVA, 'SingleUniverseJar')
        self.sap_sngl_unv_class = config_parser.get(self.SECTION_SAP_JAVA, 'SingleUniverseMainClass')
        self.sap_mltp_unv_jar = config_parser.get(self.SECTION_SAP_JAVA, 'MultipleUniverseJar')
        self.sap_mltp_unv_class = config_parser.get(self.SECTION_SAP_JAVA, 'MultipleUniverseMainClass')

    def error_handling(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        return "Error in {file}, line {n_line} {line}.\nError {type}: {message}".format(file=filename, n_line=lineno,
                                                                            line=line.strip(),
                                                                            message = exc_obj, type=exc_type.__name__)



def get_curr_cms_addr(balancer_addr):
    command = 'nslookup ' + balancer_addr + '''| awk "NR==6" | awk -F':' '{print $2}' | xargs nslookup | awk "NR==4" | awk -F'=' '{print $2}' | awk -F'.' '{print $1}' '''
    result = subprocess.check_output(command, shell=True).strip().decode('utf-8')

    return result


def initialize_settings(config_name, instance_type, config_folder_name='config'):
    logger.debug("Initialize settings for {x} is working".format(x=config_name))
    base_path = os.path.dirname(__file__) + '/..'
    config_path = "{base_path}/{config_folder_name}".format(base_path=base_path, config_folder_name=config_folder_name)
    global settings
    settings = Settings(config_path, instance_type, config_name)
    os.environ['ORACLE_HOME'] = settings.oracle_home
    os.environ["NLS_LANG"] = "AMERICAN_AMERICA.AL32UTF8"

    sys_logging.set_logging_configuration(config_path, settings)
    logger.info("SAP is on {x}.".format(x=settings.sap_host))
    return settings


global settings