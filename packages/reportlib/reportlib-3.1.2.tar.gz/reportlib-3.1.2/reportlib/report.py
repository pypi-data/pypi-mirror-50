import sys
import os
from os.path import dirname, exists, join, abspath
from uuid import uuid4

import htmlmin
import yaml
from css_html_js_minify import css_minify

from reportlib.utils.pandas.styler import Styler
from reportlib.utils.templating import template_loader, get_template_dirs
from tkmail import Email


class Report:
    def __init__(self, 
                 template_name='base/base.html',
                 styles=None,
                 title=None, extra=None, context=None, 
                 html_output=None, email_config=None, email_credentials=None):
        self.template_name = template_name
        
        styles = styles or []
        if isinstance(styles, str):
            styles = [styles]
        self.styles = list({'base/styles.css'} | set(styles))
        
        self.title = title
        self.extra = extra
        self.tables = []
        
        self.context = {
            'title': self.title,
            'uuid4': str(uuid4()),
        }
        if context:
            for key, value in context.items():
                if isinstance(key, str):
                    self.context[key] = value
        
        self.html_output = html_output
        self.email_config = email_config
        self.email_credentials = email_credentials
        
        self.attachments = []
        
    def add_attachment(self, src, name=None):
        self.attachments.append({
            'src': src,
            'name': name,
        })
        return self
        
    def _get_context(self):
        return {
            'title': self.title,
            'extra': self.extra,
            **self.context,
            'tables': self.tables,
            'styles': self._load_styles(),
        }

    def add_table(self, styler):
        if isinstance(styler, Styler):
            styler.set_context(**self.context)
            self.tables.append(styler)
        elif isinstance(styler, (list, tuple)):
            for s in styler:
                self.add_table(s)
        else:
            raise ValueError('`styler` must be an instance of `reportlib.utils.pandas.styler.Styler` or a list of them')
        
    def add_grouped_table(self, stylers):
        if len(stylers) > 1:
            for i, styler in enumerate(stylers):
                if i > 0:
                    styler.set_context(skip_table_open_tag=True)
                if i < len(stylers) - 1:
                    styler.set_context(skip_table_close_tag=True)
        self.add_table(stylers)
        
    def _load_styles(self):
        styles = []
        for path in self.styles:
            for folder in get_template_dirs():
                _path = join(folder, path)
                if exists(_path):
                    with open(_path, 'r') as f:
                        css = f.read()
                        css = css_minify(css)
                        styles.append(css)
                    break
        return styles
      
    def run(self):
        """Render, write to file and send email"""
        html_string = self.render_html()
        
        if 'IPython.display' in sys.modules:
            from IPython.display import display, HTML
            display(HTML(html_string))

        self.write_to_file(html_string)
        self.send_email(html_string)

    def write_to_file(self, html_string):
        if self.html_output:
            html_output = abspath(self.html_output)
            os.makedirs(dirname(html_output), exist_ok=True)
            with open(html_output, 'w', encoding='utf-8') as f:
                f.write(html_string)
                
    def send_email(self, html_string):
        if self.email_config and self.email_credentials:
            if isinstance(self.email_config, dict):
                config = self.email_config.copy()
            elif isinstance(self.email_config, str) and exists(self.email_config):
                with open(self.email_config, 'r') as f:
                    config = yaml.load(f, Loader=yaml.FullLoader)
            else:
                config = None

            if config:
                print('Email config: %s' % str(config))
                if 'subject' in config:
                    config['subject'] = config['subject'].format(**self.context)
                config.update(self.email_credentials)
                email = Email(**config).html(html_string)
                for attachment in self.attachments:
                    email.attachment(**attachment)
                email.send().retry(5)
            else:
                print('Invalid email config')

    def render_html(self):
        template = template_loader.get_template(self.template_name)
        html_string = template.render(self._get_context())
        html_string = htmlmin.minify(
            html_string,
            remove_comments=True,
            remove_empty_space=True,
            reduce_boolean_attributes=True,
            reduce_empty_attributes=True,
            remove_optional_attribute_quotes=True,
            convert_charrefs=True,
        )
        return html_string
