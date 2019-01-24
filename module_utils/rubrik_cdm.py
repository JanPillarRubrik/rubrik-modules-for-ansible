
# This code is part of Ansible, but is an independent component.
#
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2018 Rubrik, Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


from ansible.module_utils.six import iteritems

import urllib3
urllib3.disable_warnings()

import os


def credentials(module):
    """Helper function to establish inital connectivity to the Rubrik cluster. The function will first attempt
    to read the relevant credentials from environment variables and then if those are not found try to manually provie
    the values through supplied parameters.

    Arguments:
        module {class} -- Ansible module helper class.

    Returns:
        [str] -- Any potential error that may occur during the initial connection.
        [class] -- On success, return rubrik_cdm.Connect
    """

    ansible = module.params

    try:
        node_ip = ansible["node_ip"]
        username = ansible["username"]
        password = ansible["password"]
    except KeyError:
        node_ip = os.environ.get('rubrik_cdm_node_ip')
        username = os.environ.get('rubrik_cdm_username')
        password = os.environ.get('rubrik_cdm_password')

    return node_ip, username, password


login_credentials_spec = {
    'node_ip': dict(),
    'username': dict(),
    'password': dict(no_log=True),
}

rubrik_argument_spec = {
    'provider': dict(type='dict', options=login_credentials_spec),
}


def load_provider_variables(module):
    """Pull the node_ip, username, and password arguments from the provider
    variable
    """

    provider = module.params.get('provider') or dict()
    for key, value in iteritems(provider):
        if key in login_credentials_spec:
            if module.params.get(key) is None and value is not None:
                module.params[key] = value
