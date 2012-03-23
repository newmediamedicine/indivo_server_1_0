from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',

    # forgotten password: Combines a reset and a secret-resend into one call
    (r'^forgot-password$', MethodDispatcher({'POST': account_forgot_password})),

    # FBY: send an account a message
    (r'^send/$', MethodDispatcher({'POST' : send_account_message})),

    # FBY: get messages account sent
    (r'^sent/$', MethodDispatcher({'GET' : account_sent})),

    # FBY: read a sent message
    (r'^sent/(?P<message_id>[^/]+)$',
      MethodDispatcher({'GET': account_sent_message})),

    # FBY: archive a sent message
    (r'^sent/(?P<message_id>[^/]+)/archive$',
      MethodDispatcher({'POST': account_sent_message_archive})),

    # reset
    (r'^reset$', MethodDispatcher({'POST': account_reset})),

    # set state
    (r'^set-state$', MethodDispatcher({'POST': account_set_state})),

    # update info
    (r'^info-set$', MethodDispatcher({'POST': account_info_set})),

    # auth systems
    (r'^authsystems/$', MethodDispatcher({'POST': account_authsystem_add})),

    # change the password
    (r'^authsystems/password/change$', MethodDispatcher({
                'POST' : account_password_change})),

    # set the password
    (r'^authsystems/password/set$', MethodDispatcher({
                'POST' : account_password_set})),

    # set the username
    (r'^authsystems/password/set-username$', MethodDispatcher({'POST': account_username_set})),

    # URL to initialize account
    (r'^initialize/(?P<primary_secret>[^/]+)$', MethodDispatcher({'POST': account_initialize})),
    (r'^check-secrets/(?P<primary_secret>[^/]+)$', MethodDispatcher({'GET': account_check_secrets})),

    # URL to resend the login URL
    (r'^secret-resend$', MethodDispatcher({'POST':account_resend_secret})),

    # secret
    (r'^secret$', MethodDispatcher({'GET':account_secret})),

    # primary secret (very limited call)
    (r'^primary-secret$', MethodDispatcher({'GET':account_primary_secret})),

    # record list
    (r'^records/$', MethodDispatcher({'GET':record_list})),

    # send a message or read the inbox
    (r'^inbox/$', MethodDispatcher({
                'GET' : account_inbox,
                'POST': account_send_message})),

    # read a message
    (r'^inbox/(?P<message_id>[^/]+)$',
      MethodDispatcher({'GET': account_inbox_message})),

    # archive a message
    (r'^inbox/(?P<message_id>[^/]+)/archive$',
      MethodDispatcher({'POST': account_message_archive})),

    # accept an attachment
    (r'^inbox/(?P<message_id>[^/]+)/attachments/(?P<attachment_num>[^/]+)/accept$', MethodDispatcher({
                'POST': account_inbox_message_attachment_accept})),

    # healthfeed
    (r'^notifications/$', MethodDispatcher({'GET':account_notifications})),

    (r'^permissions/$', MethodDispatcher({'GET': account_permissions})), 
)    
