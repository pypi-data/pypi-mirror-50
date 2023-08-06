# -*- coding: utf-8 -*-
"""
Adapted from Sharefile API Python example:

@author: Sam Rubanowitz

LICENSES FROM PREVIOUS VERSIONS:
            Copyright (c) 2015, Rob R, KHC
            Licensed under the Apache License, Version 2.0 (the "License");
            you may not use this file except in compliance with the License.
            You may obtain a copy of the License at

                http://www.apache.org/licenses/LICENSE-2.0

            Unless required by applicable law or agreed to in writing, software
            distributed under the License is distributed on an "AS IS" BASIS,
            WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
            See the License for the specific language governing permissions and
            limitations under the License.

            Original Python 2 version
            Copyright (c) 2014 Citrix Systems, Inc.
            MIT License
            Available July 07, 2016
            https://api.sharefile.com/rest/samples/python.aspx


LICENSE FOR THIS PROGRAM:
MIT License

Copyright (c) 2019 California Association of REALTORS, Inc.®


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:


The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.


THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


"""

import http.client as httplib
import json
import logging
import mimetypes
import os
import simplejson
import time
import urllib.parse as urlparse
import warnings

import requests
from . import ShareFile_errors as SF_errors

logging.getLogger('carsharefile').addHandler(logging.NullHandler())
# Disable all logging with this line:
# logging.getLogger('carsharefile').propagate = False


POST = 'POST'
GET = 'GET'
PATCH = 'PATCH'


class Token:
    """Creates a Token object that can be used to authorize calls to the
    ShareFile API. """

    def __init__(self, hostname, username, password, client_id, client_secret):
        self.hostname = hostname  # domain.sharefile.com
        self.username = username  # person@email.com
        self.password = password
        self.client_id = client_id  # - OAuth2 client_id key
        self.client_secret = client_secret  # - OAuth2 client_secret key
        self.info = self.authenticate()

        if self.info is None:
            msg = 'No token was found. Something is wrong with 1 or more of the following:\n hostname, username, ' \
                  'password, client_id, or client_secret.'

            raise SF_errors.InvalidCredentialsError(msg)

    def authenticate(self):
        """
        Authenticate via username/password. Returns json token object.
        """

        uri_path = '/oauth/token'

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # static
        params = {
            'grant_type': 'password', 'client_id': self.client_id, 'client_secret': self.client_secret,
            'username': self.username, 'password': self.password
        }

        url = 'https://' + self.hostname + uri_path

        response = requests.post(url, data=urlparse.urlencode(params), headers=headers)

        token = None
        if response.status_code == 200:
            token = response.json()
            logging.info(f'Received token: {token}')
        else:
            logging.info("Bad response, no token received.")

        return token

    def __repr__(self):
        return f'<ShareFile API Token object>. Authorized to {self.username}.'


def get_authorization_header(token):
    """Auth header used in all API calls."""
    return {'Authorization': f"Bearer {token.info['access_token']}"}


def get_hostname(token):
    """Gets the hostname using token info."""
    return f"{token.info['subdomain']}.sf-api.com"


def make_request(req_type, token, uri_path, add_header=None, **kwargs):
    """
    Make a request to the ShareFile API. Simplifies the process of making the request for code
    that would otherwise have to specify everything every time.
    :param req_type: the type of request -- POST or GET
    :param token: Token object used to authenticate API calls.
    :param uri_path: uri path to send to API
    :param add_header: add something to the header other than just the default
    :param kwargs: optional keyword arguments like 'json', 'data', 'params', etc.
    :return: response from API
    :rtype: dict (json)
    """

    url = "https://" + get_hostname(token) + uri_path
    header = get_authorization_header(token)
    if add_header:
        header.update(add_header)  # if passed in, add to header dict

    map_to_requests_func = {'POST': requests.post, 'GET': requests.get, 'PATCH': requests.patch}
    api_call = map_to_requests_func.get(req_type)  # set api_call to function of requests module using typ as key
    if api_call is None:  # if not POST, GET, or PATCH, .get() will return None
        msg = 'Bad parameter passed into make_request(). Can only pass in either GET, POST, or PATCH for request.'
        raise NotImplementedError(msg)

    return api_call(url, headers=header, **kwargs)


def get_toplevel_folder(token, folder_name):
    """
    Gets a toplevel folder that lives right underneath all shared folders for an account.
    :param token: Token object used to authenticate API calls.
    :param folder_name: Name of folder.
    :return: json dict containing info about toplevel folder.
    :rtype: dict
    """

    uri_path = '/sf/v3/Items(allshared)?$expand=Children'  # 'allshared' is the folder Id for Shared Folders in
    # ShareFile

    response = make_request(GET, token, uri_path)  # GET request to API

    toplevel_subfolders = response.json()['Children']

    for child in toplevel_subfolders:
        if child['Name'] == folder_name:
            toplevel_folder = child
            break

    else:  # if there was no break, meaning folder was not found
        msg = f"{folder_name} was not found in all shared. Try inputting a different folder name for param folder_name."
        raise FileNotFoundError(msg)

    return toplevel_folder


def filter_children(children, desired):
    """
    Filters children from a passed in list of children.
    :param children: List of all children
    :param desired: List of names of desired children
    :return: List of only desired children
    """
    certain_children = children
    if desired is not None:  # if they specified to filter
        if type(desired) is not list:
            msg = 'Desired children must be passed in as a list.'
            raise TypeError(msg)

        certain_children = [child for child in certain_children if child['Name'] in desired]  # filter

    return certain_children


def get_children_by_path(token, master_id, full_path, desired_children: list = None):
    """
    Get children of a master folder by path. Uses query parameters expand=Children and path=full_path.
    :param token: Token object used to authenticate API calls.
    :param master_id: Id of folder that lives just above the first sub-folder in the full_path passed in.
    :param full_path: path that leads to desired children. First sub-folder in path must be underneath the
    master folder, which the param master_id refers to.
    :param desired_children: Optional. Must be a list. Passed in to filter out only desired children once all
    # children are found.
    :return: List of dictionaries. Each dict is one of the children and contains child info.
    :rtype: list
    """

    encoded_path = urlparse.quote(full_path)  # encodes special characters to URL-readable format:
    # quote('abc def') -> 'abc%20def'
    uri_path = f'/sf/v3/Items({master_id})/ByPath?$expand=Children&path=' + encoded_path
    response = make_request(GET, token, uri_path)  # make a GET request using uri_path

    all_children = response.json()

    if response.status_code == 404:
        raise SF_errors.ItemNotFoundError(f"Item at path: {full_path} does not exist.")

    certain_children = all_children['Children']

    return filter_children(certain_children, desired_children)


def get_child_by_path(token, master_id, full_path, desired_child):
    """
    Get children of a master folder by path. Uses query parameters expand=Children and path=full_path.
    :param token: Token object used to authenticate API calls.
    :param master_id: Id of folder that lives just above the first sub-folder in the full_path passed in.
    :param full_path: path that leads to desired children. First sub-folder in path must be underneath the
    master folder, which the param master_id refers to.
    :param desired_child: Desired child from parent folder.
    :return: List of dictionaries. Each dict is one of the children and contains child info.
    :rtype: list
    """

    child = get_children_by_path(token, master_id, full_path, desired_children=[desired_child])
    if not child:
        raise SF_errors.ItemNotFoundError(f"{desired_child} not found in"
                                          f"{get_item_by_id(token, master_id)['Name']}")
    return child[0]


def get_children_by_id(token, item_id, desired_children: list = None):
    """
    Get children of folder using folder's id. Uses query parameters 'expand' and 'select':
    expand = Children to get any Children of the folder
    select = Id,Name,Children/Id,Children/Name,Children to get the Id, Name of the folder,
    and the Id and Name of any Children of that folder.
    :param token: Token object used to authenticate API calls.
    :param item_id: Id of folder from which to get children.
    :param desired_children: Optional. Must be a list. Passed in to filter out only desired children once all
    # children are found.
    :return: List of dictionaries. Each dict is one of the children and contains child info.
    :rtype: list
    """

    select_this = 'Id,Name,Children/Id,Children/Name'
    uri_path = f'/sf/v3/Items({item_id})?$expand=Children&$select=' + select_this

    response = make_request(GET, token, uri_path)  # GET request to API
    items = response.json()

    if 'Children' not in items:
        msg = f'{items["Name"]} has no children. Try inputting a different id.'
        raise SF_errors.NoChildrenError(msg)
    else:
        children = items['Children']  # get children of returned json dict of folder using key 'Children'

    return filter_children(children, desired_children)


def get_child_by_id(token, parent_id, desired_child):
    """
    Get children of folder using folder's id. Uses query parameters 'expand' and 'select':
    expand = Children to get any Children of the folder
    select = Id,Name,Children/Id,Children/Name,Children to get the Id, Name of the folder,
    and the Id and Name of any Children of that folder.
    :param token: Token object used to authenticate API calls.
    :param parent_id: Id of folder from which to get children.
    :param desired_child: Desired child from folder.
    :param
    :return: child item, json
    """

    child = get_children_by_id(token, parent_id, desired_children=[desired_child])
    if not child:
        raise SF_errors.ItemNotFoundError(f"{desired_child} not found in "
                                          f"{get_item_by_id(token, parent_id)['Name']}")
    return child[0]


def choose_item(folder, desired_item):
    """
    Chooses an item from a given folder.
    :param folder: Folder from which to get the item
    :param desired_item: Name of desired item
    :return: Found item
    """
    chosen_item = None
    for item in folder:
        if item['Name'] == desired_item:
            chosen_item = item

    if chosen_item is None:
        msg = f"{desired_item} was not found in passed in folder, called {folder['Name']}."
        raise FileNotFoundError(msg)

    return chosen_item


def create_share_link(token, item_id, filename):
    """
    Gets shareable link for an item to be put in excel sheet.
    :param token: Token object used to authenticate API calls.
    :param item_id: Id of item which the link will point to.
    :param filename: Used in params, required by API.
    :return: Shareable link to item.
    :rtype: str
    """

    uri_path = '/sf/v3/Shares?notify=false '

    params = {
        "ShareType": "Send",
        "Title": filename,
        "Items": [{"Id": item_id}],
        "Recipients": [],
        "ExpirationDate": "9999-12-31",  # static "date", disables share expiration
        "RequireLogin": 'false',
        "RequireUserInfo": 'false',
        "MaxDownloads": -1,  # no max, unlimited downloads
        "UsesStreamIDs": 'false'
    }

    response = make_request(POST, token, uri_path, json=params)  # POST request to API using params
    link = response.json().get('Uri')  # get link from response dict returned from POST request using 'Uri' key.
    if link is None:  # if no 'Uri' key exists for whatever reason...
        raise SF_errors.LinkNotAcquiredError(f'Link for {filename} with id of {item_id} not found.')

    return link


def create_folder_tree(token, parent_id, tree_dict):
    """
    Recursively creates a folder in a given parent folder with a name and (optional) description.
    Uses schema to validate the inputted tree structure dict.
    :param token: Token object used to authenticate API calls.
    :param parent_id: the parent folder in which to create the folder
    :param tree_dict: dictionary containing subfolder information
    Tree must have this structure:
        {'Name': FOLDERNAME, 'Items': []}
    Each item in the list (value of key 'Items') must have the same format as above. Simple recusion.

    :type tree_dict: dict
    """
    from schema import Schema, And, Optional
    schema = Schema({
        'Name': And(str),
        Optional('Items'): list
    })
    schema.validate(tree_dict)

    master_folder = create_folder(token, parent_id, tree_dict['Name'])

    branches = tree_dict['Items']
    for child in branches:
        schema.validate(tree_dict)
        if 'Items' not in child:
            create_folder(token, master_folder['Id'], child['Name'])
        else:
            create_folder_tree(token, master_folder['Id'], child)

    return master_folder


def create_folder(token, parent_id, name, description=None, overwrite=False):
    """
    Creates a folder in a given parent folder with a name and (optional) description.
    :param token: Token object used to authenticate API calls.
    :param parent_id: the parent folder in which to create the folder
    :param name: name of new folder
    :param description: description of folder -- RARELY needed
    :param overwrite: bool, optional. Overwrite if folder currently exists.
    :return:
    """

    uri_path = f'/sf/v3/Items({parent_id})/Folder?overwrite={overwrite}'
    folder = {'Name': name, 'Description': description}
    header = {'Content-Type': 'application/json'}

    response = make_request(POST, token, uri_path, json=folder, add_header=header)

    if response.status_code == 409 and overwrite is False:
        msg = f'Folder "{name}" already exists.'
        raise SF_errors.FolderExistsError(msg)
    else:
        new_folder = response.json()

    return new_folder


def update_item(token, item_id, name, description=None):
    """
    Update the name and description of an item -- folder or file.
    :param token: Token object used to authenticate API calls.
    :param item_id: id of item to update
    :param name: new name to give to item
    :param description: new description to give to item
    :return: Nothing, no need to.
    """

    uri_path = f'/sf/v3/Items({item_id})'
    folder_params = {'Name': name, 'Description': description}
    response = make_request(PATCH, token, uri_path, json=folder_params)


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def multipart_form_post_upload(url, file_to_upload, filename):
    """
    Does a multipart form post upload of a file to a url.
    Treating this function as a "blackbox" as I don't fully understand the http requests it is sending -- got it from
    ShareFile API.
    :param url: url to upload file to, returned from previous API download call
    :param file_to_upload: file object to upload
    :param filename: name to name the file in ShareFile upon upload
    :return: http response
    """

    headers = {}

    boundary = f'----------{int(time.time())}'
    headers['content-type'] = f'multipart/form-data; boundary={boundary}'

    to_append = [f'--{boundary}',
                 f'Content-Disposition: form-data; name="{"File1"}"; filename="{filename}"',
                 f'Content-Type: {get_content_type(filename)}',
                 '',
                 file_to_upload,
                 f'--{boundary}--',
                 '']

    data = [thing.encode('utf-8')
            if thing is not file_to_upload else thing
            for thing in to_append]  # if thing is the file in to_append, can't utf-8 encode a file bytes object so just
    # add thing to it instead of thing.encode('utf-8')

    newline = b'\r\n'
    data_str = newline.join(data)
    headers['content-length'] = len(data_str)

    uri = urlparse.urlparse(url)  # Parse url into 6 components <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    http = httplib.HTTPSConnection(uri.netloc)  # open connection

    # Do upload
    http.putrequest(POST, f'{uri.path}?{uri.query}')
    for hdr_name, hdr_value in headers.items():
        http.putheader(hdr_name, hdr_value)
    http.endheaders()
    http.send(data_str)

    return http.getresponse()


def upload_file(token, folder_id, local_path, filename=None):
    """
    Uploads a file to a given folder with multipart/form mime encoded POST.
    :param token: Token object used to authenticate API calls.
    :param folder_id: Id of folder to upload file to
    :param local_path: complete file path to local file that will be uploaded, e.g. /Users/Sam/Documents/file.txt
    :param filename: optional, the filename will be set to this if passed in. If not, filename will be the actual name
    of file in folder (using os.path.basename, which returns the "final component" of a pathname)
    :return: the file that was just uploaded
    """

    uri_path = f'/sf/v3/Items({folder_id})/Upload'
    upload_config = make_request(GET, token, uri_path).json()

    file_to_upload = open(local_path, 'rb').read()
    filename = filename or os.path.basename(local_path)

    if 'ChunkUri' in upload_config:
        upload_response = multipart_form_post_upload(upload_config['ChunkUri'], file_to_upload, filename)
        if upload_response.status != 200:
            msg = f"{filename} failed to upload. Response: {upload_response.status, upload_response.reason}"
            raise SF_errors.UploadFailedError(msg)
    else:
        raise SF_errors.UploadFailedError('No upload URL received from ShareFile API.')

    return upload_response


def download_item(token, item_id, local_path):
    """
    Downloads a single Item. If downloading a folder the local_path name should end in .zip.
    :param token: Token object used to authenticate API calls.
    :param item_id: the id of the item to download
    :param local_path: complete file path where to download the item to, like "c:\path\to\the.file"
    """

    uri_path = f'/sf/v3/Items({item_id})/Download'

    http = httplib.HTTPSConnection(get_hostname(token))
    http.request('GET', uri_path, headers=get_authorization_header(token))
    response = http.getresponse()
    location = response.getheader('location')
    redirect = None
    if location:
        redirect_uri = urlparse.urlparse(location)
        redirect = httplib.HTTPSConnection(redirect_uri.netloc)
        redirect.request('GET', '%s?%s'%(redirect_uri.path, redirect_uri.query))
        response = redirect.getresponse()

    with open(local_path, 'wb') as target:
        b = response.read(1024*8)
        while b:
            target.write(b)
            b = response.read(1024*8)

    print(response.status, response.reason)
    http.close()
    if redirect:
        redirect.close()


def get_item_by_id(token, item_id):
    """
    Gets an item by its id.
    :param token: Token object used to authenticate API calls.
    :param item_id: string, id of the item
    :return: Item itself.
    :rtype: dict (json)
    """

    uri_path = f'/sf/v3/Items({item_id})'
    response = make_request(GET, token, uri_path)

    item = response.json()
    return item


def get_item_by_path(token, path):
    """
    Gets an item using the path to it. The API returns the last specified item in the path.
    :param token: Token object used to authenticate API calls.
    :param path: the path to the item. Always must start with '/allshared'. Final path would look something like this:
    '/allshared/MemInfo (2)/R&E (Dec 2017)/Products/'
    :return:
    """

    slash_warning = "Doing it for you, but paths should {} with '/' (forward slash)."
    if not path.startswith('/'):
        path = '/' + path
        warnings.warn(slash_warning.format('start'))
    if not path.endswith('/'):
        path = path + '/'
        warnings.warn(slash_warning.format('end'))
    if not path.startswith('/allshared/'):
        warnings.warn("Doing it for you, but paths must begin with '/allshared/'")
        path = '/allshared' + path

    uri_path = f'/sf/v3/Items/ByPath?path={urlparse.quote(path)}'
    response = make_request(GET, token, uri_path)
    try:
        return response.json()
    except (json.decoder.JSONDecodeError, simplejson.scanner.JSONDecodeError):
        raise SF_errors.ItemNotFoundError(response.text)


def paste_item(token, source, target, overwrite=False):
    """
    Copies an item (file or folder) from one place into another (essentially copy and paste) using the source's id and
    the target folder's id.
    :param token: Token object used to authenticate API calls.
    :param source: The id or path of the original, or source, item.
    :param target: The id or path of the folder in which you want to paste the item
    :param overwrite: bool, optional. Overwrite if item in target currently exists.
    :return: None, no reason to return anything because not getting anything from the API.
    """

    no_id_msg = "Did not receive an id as {}, so finding id by calling get_item_by_path. Will be faster to pass in id " \
                "directly."
    if '/allshared/' in source:  # if a path is passed in rather than the id itself,
        source = get_item_by_path(token, source)['Id']  # turn the path into an id
        warnings.warn(no_id_msg.format('source'))
    if '/allshared/' in target:
        target = get_item_by_path(token, target)['Id']
        warnings.warn(no_id_msg.format('target'))

    uri_path = f'/sf/v3/Items({source})/Copy?'
    params = {'targetid': target, 'overwrite': overwrite}

    while True:
        try:
            response = make_request(POST, token, uri_path, params=params)

            if response.status_code == 409:
                msg = f"Folder {get_item_by_id(token, source)['Name']} already exists."
                raise SF_errors.FolderExistsError(msg)

            elif response.status_code >= 400:  # if not 409 but greater than or == 400
                msg = f"Error when trying to paste item: {response.status_code, response.reason}"
                raise ConnectionError(msg)

        except ConnectionError as e:  # if it's a FolderExistsError I want it to stop the program, but if other error
            # it should just try to paste again.
            time.sleep(5)
        else:
            break

    return response.json()
