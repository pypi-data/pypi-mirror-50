import os
import sys
from yaml import safe_load, YAMLError
from time import strftime, gmtime
from platform import system
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    def __init__(self,CONFIG_FILE=None):
        if system() == "Windows":
            self.DEFAULT_CONFIG_FILE = os.path.join(basedir, "default_config_windows.yaml")
        else:
            self.DEFAULT_CONFIG_FILE = os.path.join(basedir, "default_config.yaml")

        self.CONFIG_FILE = CONFIG_FILE or \
                os.environ.get('CWLAB_CONFIG') or \
                self.DEFAULT_CONFIG_FILE

        if not os.path.exists(self.CONFIG_FILE):
            sys.exit(
                "Error: the specified config file \"" +
                self.CONFIG_FILE +
                "\" does not exist."
            )

        print(">>> Using config file: " + self.CONFIG_FILE, file=sys.stderr)

        with open(self.CONFIG_FILE, 'r') as stream:
            try:
                self.CONFIG_FILE_content = safe_load(stream)
            except YAMLError as exc:
                sys.exit("Error while reading the config.yaml: " + exc)

        cwlab_fallback_dir = os.path.join(os.path.expanduser("~"), "cwlab")

        # parameters:
        self.SECRET_KEY = (
            os.environ.get('CWLAB_SECRET_KEY') or 
            self.CONFIG_FILE_content.get('SECRET_KEY') or  
            strftime("%Y%m%d%H%M%S", gmtime())
        )

        self.TEMP_DIR = (
            os.environ.get('CWLAB_TEMP_DIR') or
            self.CONFIG_FILE_content.get('TEMP_DIR') or  
            os.path.join( cwlab_fallback_dir, "temp")
        )
        self.CWL_DIR = (
            os.environ.get('CWLAB_CWL_DIR') or  
            self.CONFIG_FILE_content.get('CWL_DIR') or  
            os.path.join( cwlab_fallback_dir, "CWL")
        )
        self.EXEC_DIR = (
            os.environ.get('CWLAB_EXEC_DIR') or 
            self.CONFIG_FILE_content.get('EXEC_DIR') or   
            os.path.join( cwlab_fallback_dir, "exec")
        )
        self.INPUT_DIR = (
            os.environ.get('CWLAB_INPUT_DIR') or 
            self.CONFIG_FILE_content.get('INPUT_DIR') or   
            os.path.join( cwlab_fallback_dir, "input")
        )
        self.DB_DIR = (
            os.environ.get('CWLAB_DB_DIR') or 
            self.CONFIG_FILE_content.get('DB_DIR') or  
            os.path.join( cwlab_fallback_dir, "database")
        )
        
        self.DEBUG = (
            os.environ.get('CWLAB_DEBUG') == "True" or
            self.CONFIG_FILE_content.get('DEBUG')
        )

        if self.DEBUG:
            print("Debug mode turned on, don't use this on production machines.", file=sys.stderr)

        self.SQLALCHEMY_DATABASE_URI = (
            os.environ.get('CWLAB_DATABASE_URL') or
            self.CONFIG_FILE_content.get('DATABASE_URL') or  
            ('sqlite:///' + os.path.join(self.DB_DIR, 'cwlab.db'))
        )
        
        self.SQLALCHEMY_TRACK_MODIFICATIONS = (
            os.environ.get('DATABASE_TRACK_MODIFICATIONS') or
            self.CONFIG_FILE_content.get('CWLAB_DATABASE_TRACK_MODIFICATIONS') or  
            False
        )

        # execution profile:
        self.EXEC_PROFILES = self.CONFIG_FILE_content.get('EXEC_PROFILES') or {}
        
        # set defaults:
        timeout_defaults = {
            "pre_exec": 120,
            "exec": 86400,
            "eval": 120,
            "post_exec": 120
        }
        general_defaults = {
            "max_retries_default": 3,
            "max_parallel_runs_default": 3, # if exceeded, jobs will be queued
            "wait_when_queued": 10, # When beeing queued, wait this long before trying to start again
        }
        for exec_profile in self.EXEC_PROFILES.keys():
            timeout = timeout_defaults
            if "timeout" in self.EXEC_PROFILES[exec_profile].keys():
                timeout.update(self.EXEC_PROFILES[exec_profile]["timeout"])
            self.EXEC_PROFILES[exec_profile]["timeout"] = timeout
            general = general_defaults
            general.update(self.EXEC_PROFILES[exec_profile])
            self.EXEC_PROFILES[exec_profile] = general



        # Configure web server:
        self.WEB_SERVER_HOST = (
            os.environ.get('CWLAB_WEB_SERVER_HOST') or
            self.CONFIG_FILE_content.get('WEB_SERVER_HOST') or  
            "localhost"
        )
        self.WEB_SERVER_PORT = (
            os.environ.get('CWLAB_WEB_SERVER_PORT') or
            self.CONFIG_FILE_content.get('WEB_SERVER_PORT') or  
            "5000"
        )

        # not accessible by user:
        self.SEND_FILE_MAX_AGE_DEFAULT = 0 # disables caching
        