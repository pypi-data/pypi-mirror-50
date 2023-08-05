import os
import sys
import re

from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

class ImageLocalization(BasePlugin):

    config_scheme = (
        ('param', config_options.Type(mkdocs_utils.string_types, default='')),
    )

    def _init_(self):
        self.enabled = True
        self.total_time = 0

    def on_page_content(self, markdown, page, config, site_navigation=None, **kwargs):

        result = re.search('/(_assets\/img.[^\"\)]*)', markdown)

        while result:
          target = result.group(1)
          result = result.group(0)

          if (os.path.exists(config['docs_dir']+'/'+config['locale']+result)):
            markdown = markdown.replace(result, '/'+config['locale']+'/DeleteMarker'+target)
            print("NEW IMAGE: " + '/'+config['locale']+'/DeleteMarker'+target)

          else:
            markdown = markdown.replace(result, '/DeleteMarker'+target)
            print("Special image not found in:" + config['docs_dir']+'/'+config['locale']+result)

          result = re.search('/(_assets\/img.[^\"\)]*)', markdown)

        markdown = markdown.replace('DeleteMarker', '')

        return markdown