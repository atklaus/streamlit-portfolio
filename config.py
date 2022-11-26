import sys
import os
from dotenv import load_dotenv
from pathlib import Path
import sys
import git
from git import Repo
sys.path.insert(1, os.path.join(sys.path[0], '..'))

dotenv_path = Path('/Users/adamklaus/.env')
load_dotenv(dotenv_path=dotenv_path)

CREDS = os.environ
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  



