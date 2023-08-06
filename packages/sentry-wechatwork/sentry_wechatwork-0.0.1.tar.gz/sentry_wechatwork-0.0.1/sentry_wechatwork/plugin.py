# coding: utf-8
import logging
from collections import defaultdict

from django import forms
from django.utils.translation import ugettext_lazy as _

from sentry.plugins.bases import notify
from sentry.http import safe_urlopen
from sentry.utils.safe import safe_execute

from . import __version__, __doc__ as package_doc


class WechatWorkNotificationsOptionsForm(notify.NotificationConfigurationForm):
    webhook = forms.CharField(
        label=_('Webhook'),
        widget=forms.TextInput(attrs={'placeholder': 'http://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx'}),
        help_text=_('Read more: https://work.weixin.qq.com/api/doc#90000/90136/91770'),
    )
    message_template = forms.CharField(
        label=_('Message template'),
        widget=forms.Textarea(attrs={'class': 'span4'}),
        help_text=_('Set in standard python\'s {}-format convention, available names are: '
                    '{project_name}, {url}, {title}, {message}, {tag[%your_tag%]}'),
        initial='# {project_name} {tag[level]}: {title}\n\n{message}\n\n[{url}]({url})'
    )


class WechatWorkNotificationsPlugin(notify.NotificationPlugin):
    title = 'WechatWork Notifications'
    slug = 'sentry_wechatwork'
    description = package_doc
    version = __version__
    author = 'Allen'
    author_url = 'https://github.com/kuainiu/sentry-wechatwork'
    resource_links = [
        ('Bug Tracker', 'https://github.com/kuainiu/sentry-wechatwork/issues'),
        ('Source', 'https://github.com/kuainiu/sentry-wechatwork'),
    ]

    conf_key = 'sentry_wechatwork'
    conf_title = title

    project_conf_form = WechatWorkNotificationsOptionsForm

    logger = logging.getLogger('sentry.plugins.sentry_wechatwork')

    def is_configured(self, project, **kwargs):
        return bool(self.get_option('webhook', project) and self.get_option('message_template', project))

    def get_config(self, project, **kwargs):
        return [
            {
                'name': 'webhook',
                'label': 'Webhook',
                'type': 'text',
                'help': 'Read more: https://work.weixin.qq.com/api/doc#90000/90136/91770',
                'placeholder': 'http://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=',
                'validators': [],
                'required': True,
            },
            {
                'name': 'message_template',
                'label': 'Message Template',
                'type': 'textarea',
                'help': 'Set in standard python\'s {}-format convention, available names are: '
                    '{project_name}, {url}, {title}, {message}, {tag[%your_tag%]}. Undefined tags will be shown as [NA]',
                'validators': [],
                'required': True,
                'default': '# {project_name} {tag[level]}: {title}\n\n{message}\n\n[{url}]({url})'
            },
        ]

    def build_message(self, group, event):
        the_tags = defaultdict(lambda: '[NA]')
        the_tags.update({k:v for k, v in event.tags})
        names = {
            'title': event.title,
            'tag': the_tags,
            'message': event.message,
            'project_name': group.project.name,
            'url': group.get_absolute_url(),
        }

        template = self.get_message_template(group.project)

        text = template.format(**names)

        return {
            'msgtype': 'markdown',
            'markdown': {
                'content': text    
            }
        }

    def get_message_template(self, project):
        return self.get_option('message_template', project)

    def send_message(self, url, payload):
        self.logger.debug('Sending message to %s ' % url)
        response = safe_urlopen(
            method='POST',
            url=url,
            json=payload,
        )
        self.logger.debug('Response code: %s, content: %s' % (response.status_code, response.content))

    def notify_users(self, group, event, fail_silently=False, **kwargs):
        self.logger.debug('Received notification for event: %s' % event)
        payload = self.build_message(group, event)
        self.logger.debug('Built payload: %s' % payload)
        url = self.get_option('webhook', group.project)
        self.logger.debug('Webhook url: %s' % url)
        safe_execute(self.send_message, url, payload, _with_transaction=False)
