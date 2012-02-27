""" 
.. module:: views.account
   :synopsis: Account-related Indivo view implementations.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from base import *
import urllib
import logging
from indivo.lib import utils
from django.http import HttpResponseBadRequest
from django.db import IntegrityError

ACTIVE_STATE, UNINITIALIZED_STATE = 'active', 'uninitialized'

def account_password_change(request, account):
    """ Change a account's password.

    request.POST must contain:
    
    * *old*: The existing account password.
    * *new*: The desired new password.

    Will return :http:statuscode:`200` on success,
    :http:statuscode:`403` if the old password didn't
    validate, :http:statuscode:`400` if the POST data
    didn't contain both an old password and a new one.
    
    """

    OLD = 'old'
    NEW = 'new'
    if request.POST.has_key(OLD) and request.POST.has_key(NEW):
        if account and account.password_check(request.POST[OLD]):
            account.password = request.POST[NEW]
            account.save()
            return DONE
        else:
            raise PermissionDenied()
    return HttpResponseBadRequest()


def account_reset(request, account):
    """ Reset an account to an ``uninitialized`` state.

    Just calls into :py:meth:`~indivo.models.accounts.Account.reset`.

    Will return :http:statuscode:`200` on success.

    """

    account.reset()
    return DONE


def account_set_state(request, account):
    """ Set the state of an account. 
    
    request.POST must contain:
    
    * *state*: The desired new state of the account.
    
    Options are: 
    
    * ``active``: The account is ready for use.
    
    * ``disabled``: The account has been disabled,
      and cannot be logged into.
      
    * ``retired``: The account has been permanently
      disabled, and will never allow login again.
      Retired accounts cannot be set to any other 
      state.
    
    Will return :http:statuscode:`200` on success,
    :http:statuscode:`403` if the account has been
    retired and :http:statuscode:`400` if POST data
    did not contain a "status" parameter
    
    """
    
    if not request.POST.get('state'):
        return HttpResponseBadRequest('No state')
    
    try:
        account.set_state(request.POST['state'])
    except Exception, e:
        raise PermissionDenied(e)
    account.save()
    return DONE


def account_password_set(request, account):
    """ Force the password of an account to a given value.

    This differs from 
    :py:meth:`~indivo.views.account.account_password_change`
    in that it does not require validation of the old password. This
    function is therefore admin-facing, whereas 
    :py:meth:`~indivo.views.account.account_password_change` 
    is user-facing.

    request.POST must contain:
    
    * *password*: The new password to set.

    Will return :http:statuscode:`200` on success, :http:statuscode:`400`
    if the passed POST data didn't contain a new password.

    """

    if account and request.POST.has_key('password'):
        account.password = request.POST['password']
        account.save()
        return DONE
    return HttpResponseBadRequest()


def account_username_set(request, account):
    """ Force the username of an account to a given value.

    request.POST must contain:

    * *username*: The new username to set.

    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`400` if the POST data doesn't conatain
    a new username.

    """

    if account and request.POST.has_key('username'):
        account.set_username(request.POST['username'])
        return DONE
    return HttpResponseBadRequest()


def account_info_set(request, account):
    """ Set basic information about an account.
    
    request.POST can contain any of:
    
    * *contact_email*: A new contact email for the account.
    
    * *full_name*: A new full name for the account.
    
    Each passed parameter will be updated for the account.
    
    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`400` if the POST data contains none of
    the settable parameters.
    
    """
    
    contact_email = request.POST.get('contact_email')
    full_name = request.POST.get('full_name')
    if not contact_email and not full_name:
        return HttpResponseBadRequest('No parameter given')
    
    if contact_email:
        account.contact_email = contact_email
    if full_name:
        account.full_name = full_name
    
    account.save()
    return DONE


@transaction.commit_on_success
def account_initialize(request, account, primary_secret):
    """ Initialize an account, activating it.

    After validating primary and secondary secrets, changes the 
    account's state from ``uninitialized`` to ``active`` and sends
    a welcome email to the user.

    If the account has an associated secondary secret, request.POST 
    must contain:

    * *secondary_secret*: The secondary_secret generated for the account.

    Will return :http:statuscode:`200` on success, :http:statuscode:`403`
    if the account has already been initialized or if either of the account
    secrets didn't validate, and :http:statuscode:`400` if a secondary secret
    was required, but didn't appear in the POST data.
    
    """
    
    SECONDARY_SECRET = 'secondary_secret'
    
    # check primary secret
    if account.primary_secret != primary_secret:
        account.on_failed_login()
        raise PermissionDenied()
    
    if account.state != UNINITIALIZED_STATE:
        raise PermissionDenied()
    
    # if there is a secondary secret in the account, check it in the form
    if not account.secondary_secret or request.POST.has_key(SECONDARY_SECRET):
        secondary_secret = request.POST.get(SECONDARY_SECRET)
        if account.secondary_secret and secondary_secret != account.secondary_secret:
            account.on_failed_login()
            raise PermissionDenied()
        
        account.state = ACTIVE_STATE
        try:
            account.send_welcome_email()
        except Exception, e:
            logging.exception(e)
        account.save()
        
        return DONE
    return HttpResponseBadRequest()


def account_primary_secret(request, account):
    """ Display an account's primary secret.

    This is an admin-facing call, and should be used sparingly,
    as we would like to avoid sending primary-secrets over the
    wire. If possible, use 
    :py:meth:`~indivo.views.account.account_check_secrets`
    instead.

    Will return :http:statuscode:`200` with the primary secret on success.
    
    """

    return render_template('secret', {'secret': account.primary_secret})


def account_info(request, account):
    """ Display information about an account.

    Return information includes the account's secondary-secret,
    full name, contact email, login counts, state, and auth 
    systems.

    Will return :http:statuscode:`200` on success, with account info
    XML.

    """
    # get the account auth systems
    auth_systems = account.auth_systems.all()
    return render_template('account', {'account': account,
                                'auth_systems': auth_systems})


def account_check_secrets(request, account, primary_secret):
    """ Validate an account's primary and secondary secrets.

    If the secondary secret is to be validated, request.GET must
    contain:

    * *secondary_secret*: The account's secondary secret.

    This call will validate the prmary secret, and the secondary
    secret if passed.

    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`403` if either validation fails.

    """

    SECONDARY_SECRET = 'secondary_secret'
    
    # check primary secret
    if account.primary_secret != primary_secret:
        account.on_failed_login()
        raise PermissionDenied()
    
    # if there is a secondary secret in the account, check it in the form
    if request.GET.has_key(SECONDARY_SECRET):
        secondary_secret = request.GET[SECONDARY_SECRET]
        if account.secondary_secret and secondary_secret != account.secondary_secret:
            raise PermissionDenied()
    return DONE

def account_search(request):
    """ Search for accounts by name or email.
    
    request.GET must contain the query parameters, any of:
    
    * *fullname*: The full name of the account
    
    * *contact_email*: The contact email for the account.
    
    This call returns only accounts matching all passed 
    query parameters exactly: there is no partial matching
    or text-search.
    
    Will return :http:statuscode:`200` with XML describing
    matching accounts on success, :http:statuscode:`400` if
    no query parameters are passed.
    
    """
    
    fullname      = request.GET.get('fullname', None)
    contact_email = request.GET.get('contact_email', None)
    
    if not (fullname or contact_email):
        return HttpResponseBadRequest('No search criteria given')
    
    query = Account.objects
    if fullname:
        query = query.filter(full_name = fullname)
    if contact_email:
        query = query.filter(contact_email = contact_email)
    
    return render_template('accounts_search', {'accounts': query}, type='xml')


@transaction.commit_manually
def account_authsystem_add(request, account):
    """ Add a new method of authentication to an account.

    Accounts cannot be logged into unless there exists a
    mechanism for authenticating them. Indivo supports one
    built-in mechanism, password auth, but is extensible with
    other mechanisms (i.e., LDAP, etc.). If an external mechanism 
    is used, a UI app is responsible for user authentication, and 
    this call merely registers with indivo server the fact that 
    the UI can handle auth. If password auth is used, this call 
    additionally registers the password with indivo server.
    Thus, this call can be used to add internal or external auth 
    systems.

    request.POST must contain:

    * *system*: The identifier (a short slug) associated with the
      desired auth system. ``password`` identifies the internal
      password system, and external auth systems will define their
      own identifiers.

    * *username*: The username that this account will use to 
      authenticate against the new authsystem
      
    * *password*: The password to pair with the username.
      **ONLY REQUIRED IF THE AUTH SYSTEM IS THE INTERNAL
      PASSWORD SYSTEM**.

    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`403` if the indicated auth system doesn't exist,
    and :http:statuscode:`400` if the POST data didn't contain a system
    and a username (and a password if system was ``password``), or if
    the account is already registered for the given authsystem, or a 
    different account is already registered for the given authsystem with
    the same username.

    """
    
    # check for username
    USERNAME, PASSWORD = 'username', 'password'
    
    if request.POST.has_key(USERNAME):
        username = request.POST[USERNAME]
    else:
        transaction.rollback()
        return HttpResponseBadRequest('No username')
    
    # did we get a system?
    desired_system = request.POST.get('system')
    if not desired_system:
        transaction.rollback()
        return HttpResponseBadRequest('No system')
    
    # if we got "password" as system, did we get a password?
    new_password = None
    if 'password' == desired_system:
        new_password = request.POST.get(PASSWORD)
        if not new_password:
            transaction.rollback()
            return HttpResponseBadRequest('No password')
    
    # set the auth system
    try:
        system = AuthSystem.objects.get(short_name = desired_system)
        account.auth_systems.create(username = username, 
                                 auth_system = system)
    except AuthSystem.DoesNotExist:
        transaction.rollback()
        raise PermissionDenied()
    except IntegrityError:
        transaction.rollback()
        return HttpResponseBadRequest('Duplicate attempt to add authsystem to account')
    else:
        if system == AuthSystem.PASSWORD() and new_password:
            account.password_set(new_password)
            account.set_state(ACTIVE_STATE)
            account.save()
        
        transaction.commit()
        # return the account info instead
        return DONE


def account_forgot_password(request, account):
    """ Resets an account if the user has forgotten its password.

    This is a convenience call which encapsulates
    :py:meth:`~indivo.views.account.account_reset`, 
    :py:meth:`~indivo.views.account.account_resend_secret`, and
    :py:meth:`~indivo.views.account.account_secret`. In summary,
    it resets the account to an uninitialized state, emails
    the user with a new primary-secret, and returns the
    secondary secret for display.

    Will return :http:statuscode:`200` with the secondary secret
    on success, :http:statuscode:`400` if the account hasn't yet
    been initialized and couldn't possibly need a reset. If the
    account has no associated secondary secret, the return XML
    will be empty.
    
    """

    if account.state != UNINITIALIZED_STATE:
        account.reset()
    else:
        return HttpResponseBadRequest("Account has not been initialized")
    
    try:
        account.send_forgot_password_email()
    except Exception, e:
        logging.exception(e)
    return HttpResponse("<secret>%s</secret>" % account.secondary_secret)


def account_resend_secret(request, account):
    """ Sends an account user their primary secret in case they lost it.

    Will return :http:statuscode:`200` on success.

    """

    # FIXME: eventually check the status of the account
    try:
        account.send_secret()
    except Exception, e:
        logging.exception(e)
    
    # probably ok to return DONE, but it should just be empty, like Flickr
    return DONE


def account_secret(request, account):
    """ Return the secondary secret of an account.

    Will always return :http:statuscode:`200`. If the account 
    has no associated secondary secret, the return XML will
    be empty.

    """

    return HttpResponse("<secret>%s</secret>" % account.secondary_secret)

@transaction.commit_on_success
def account_create(request):
    """ Create a new account, and send out initialization emails.
    
    request.POST holds the creation arguments. 
    
    Required Parameters:
    
    * *account_id*: an identifier for the new address. Must be formatted
      as an email address.
    
    Optional Parameters:
    
    * *full_name*: The full name to associate with the account. Defaults
      to the empty string.
    
    * *contact_email*: A valid email at which the account holder can 
      be reached. Defaults to the *account_id* parameter.
    
    * *primary_secret_p*: ``0`` or ``1``. Whether or not to associate 
      a primary secret with the account. Defaults to ``1``.
    
    * *secondary_secret_p*: ``0`` or ``1``. Whether or not to associate
      a secondary secret with the account. Defaults to ``0``.
    
    After creating the new account, this call generates secrets for it,
    and then emails the user (at *contact_email*) with their activation
    link, which contains the primary secret.
    
    This call will return :http:statuscode:`200` with info about the new
    account on success, :http:statuscode:`400` if *account_id* isn't 
    provided or isn't a valid email address, or if an account already
    exists with an id matching *account_id*.
      
    """
    
    account_id = request.POST.get('account_id', None)
    if not account_id or not utils.is_valid_email(account_id):
        return HttpResponseBadRequest("Account ID not valid")
    
    new_account, create_p = Account.objects.get_or_create(email=urllib.unquote(account_id).lower().strip())
    if create_p:
        
        # generate a secondary secret or not? Requestor can say no.
        # trust model makes sense: the admin app requestor only decides whether or not 
        # they control the additional interaction or if it's not necessary. They never
        # see the primary secret.
        
        new_account.full_name = request.POST.get('full_name', '')
        new_account.contact_email = request.POST.get('contact_email', account_id)
        
        new_account.creator = request.principal
        
        password            = request.POST.get('password', None)
        primary_secret_p    = (request.POST.get('primary_secret_p', "1") == "1")
        secondary_secret_p  = (request.POST.get('secondary_secret_p', "0") == "1")
        
        # we don't allow setting the password here anymore
        new_account.save()
        
        if primary_secret_p:
            new_account.generate_secrets(secondary_secret_p = secondary_secret_p)
            try:
                new_account.send_secret()
            except Exception, e:
                logging.exception(e)
    
    # account already existed
    else:
        return HttpResponseBadRequest("An account with email address %s already exists." % account_id)
    
    return render_template('account', {'account': new_account}, type='xml')
