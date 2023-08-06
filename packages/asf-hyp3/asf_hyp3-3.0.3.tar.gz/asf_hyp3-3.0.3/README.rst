==================
asf_hyp3 API CLASS
==================
>>> from asf_hyp3 import API
>>> api = API('username')
>>> api.login()

This module is a Python interface to the hyp3-api which handles making web requests
and parsing the output back to python objects. It takes care of adding the
username and API key to each request by letting you set them once in the constructor.
Pass them in through the username and api_key parameters:

>>> api = API('username', api_key="SAMPLE_API_KEY")


:Formats:
    - json by default which will be converted into appropriate data type,
    - csv or any other format returns string of data received

:Functions:
   | login_
   | reset_api_key_
   | get_jobs_
   | get_job_
   | get_products_
   | get_product_
   | get_products_public_
   | get_process_
   | get_processes_
   | get_groups_
   | one_time_process_
   | one_time_process_batch_
   | get_subscriptions_
   | get_subscription_
   | get_subscriptions_public_
   | create_subscription_
   | enable_subscription_
   | disable_subscription_
   | modify_subscription_
   | create_group_
   | modify_group_

.. login_

login
-----

Logs the user in and gets a valid api key

:Parameters:
    Required - None

    Optional - password, doesPrint, reset_key

:Returns:
    None

.. reset_api_key_

reset_api_key
-------------

Sets the user's api_key to a new random key

:Parameters:
    Required - None

    Optional - doesPrint

:Returns:
    A dictionary containing the username and new api_key

.. get_jobs_

get_jobs
--------
:Parameters:
    Required - None

    Optional - id(can be a list of ids), status, sub_id, granule, format

:Returns:
    A list of dictionaries containing job information with the specified
    attributes.

    Job info:
        - id, sub_id, user_id, process_id, status, granule,
          granule_url, other_granules, other_granule_urls,
          request_time, processed_time, priority, message

.. get_job_

get_job
-------
:Parameters:
    Required - id

    Optional - None

:Returns:
    A dictionary just like the one referenced in get_jobs

.. get_products_

get_products
------------
:Parameters:
    Required - None

    Optional - id, sub_id, sub_ids, sub_name, creation_date, start_date, end_date, name, group_id, group_ids, process_id, page, page_size, format

:Returns:
    A list of dictionaries containing product information for products with
    the specified attributes. The list is limited to 100 items, but more items
    can be retrieved with the page parameter (first page is 0). The default page
    size can also be changed with the page_size parameter.

    Product info contains fields:
        - id, sub_id, name, url, browse_url, browse_thumbnail, browse_geo_immage,
          browse_geo_xml, size, creation_date

    Attributes `browse_thumbnail`, `browse_geo_immage`, `browse_geo_xml` are dictionaries with the following fields:
        - url, epsg, lat_min, lat_max, lon_min, lon_max

.. get_product_

get_product
-----------
:Parameters:
    Required - id

    Optional - None

:Returns:
    A dictionary just like the one referenced in get_product

.. get_products_public_

get_products_public
------------------------
:Parameters:
    Required - group_id
    Optional - page, format

:Returns:
    A JSON or CSV array with information about all products in the public
    group with given group_id.

.. get_process_

get_process
-----------
:Parameters:
    Required - id

    Optional - format

:Returns:
    A dictionary or a string depending on format containing information about
    the process.

    Return fields are:
        - id, name, description, requires_pair,
          supports_time_series_processing, requires_dual_pol

.. get_processes_

get_processes
-------------
:Parameters:
    Required - None

    Optional - format

:Returns:
    A list of dictionaries for all available processes. Each entry is as described
    by get_process.

.. get_groups_

get_groups
-------------
:Parameters:
    Required - None

    Optional - id, name, format

:Returns:
    A list of dictionaries containing information about each group.

    Return fields are:
        - id, name, description, subscriptions

.. one_time_process_

one_time_process
----------------

Schedules a new processing request and returns a dictionary indicating whether
or not the request succeeded, and an error message. If the process_id specifies
a process that requires a granule pair, then other_granules must also be
supplied.

:Parameters:
    Required - granule, process_id

    Optional - other_granules, priority, message

:granule:
    can be passed a single granule, a list of granule strings, a file name
    or an open file with granules in it.
    All granule operations are done with the given process_id.

:Returns:
    {"status": "SUCCESS", "message": null} or

    {"status": "SUCCESS", "id": 1234} or

    {"status": "ERROR", "message": *A Contextual Message*}

.. one_time_process_batch_

one_time_process_batch
----------------------

Schedules any number of new processing requests through an input file containing
descriptions of the jobs.

:Parameters:
    Required - filename

:File (CSV):
    granule,process_id,other_granules,priority,message

    S1_GRANULE,2,,10,sample message

    S1_GRANULE,10,S1_GRANULE,,,

.. create_subscription_

create_subscription
-------------------


Schedules a new subscription and returns a dictionary indicating
whether or not the request succeeded, as well as an error message in
the event of failure. If you pass a file path to shapefilepath this will
override your entry for location. The shapefilepath must point to one of
the files necessary to create your geometry object, not simply their parent
directory.


:Parameters:
    Required - polarization, crop_to_selection, name, process_id, platform

    Optional - location, start_date, end_date, description, extra_arguments, enable, project_id, group_id

:Returns:
    {"status": "SUCCESS", "id": 1234} or

    {"status": "ERROR", "message": *A Contextual Message*}

.. get_subscriptions_

get_subscriptions
-----------------
:Parameters:
    Required - None

    Optional - id, process_id, name, location, start_date, end_date, enable,
    project_id, group_id, format

:Returns:
    A array of subscription information with the specified
    attributes or a string depending on format.

    Subscription info contains fields:
        - id, process_id, user_id, name, location, start_date, end_date, enabled

.. get_subscription_

get_subscription
----------------
:Parameters:
    Required - id
    Optional - None

:Returns:
    A JSON or CSV array with information belonging to the subscription holding
    the subscription id passed.

    Subscriptions info contains fields:
        - id, process_id, user_id, name, location, start_date, end_date, enabled

.. get_subscriptions_public_

get_subscriptions_public
------------------------
:Parameters:
    Required - group_id
    Optional - format

:Returns:
    A JSON or CSV array with information about all subscriptions in the public
    group with given group_id.

.. disable_subscription_

disable_subscription
--------------------
Sets the property 'enabled' of a subscription to False. No further
actions will be taken based on this subscription until it is enabled
again. Returns a dictionary indicating whether or not the request
succeeded, and an error message in the event it did not.

:Parameters:
    None

:Returns:
    A dictionary just like the one referenced in get_subscriptions

.. enable_subscription_

enable_subscription
-------------------
Sets the property 'enabled' of a subscription to True. Further
actions will be taken based on this subscription until it is disabled
again. Returns a dictionary indicating whether or not the request
succeeded, and an error message in the event it did not.

:Parameters:
    None

:Returns:
    A dictionary just like the one referenced in get_subscriptions

.. modify_subscription_

modify_subscription
-------------------
Sets the property 'name' and property 'description' of a subscription to
the passed values, if those values are not None. Returns a dictionary indicating
what has changed and if the request was a success.

:Parameters:
    Required: username, id
    Optional: project_id, name, description, end_date

:Returns:
    A dictionary indicating the updated values. If the request has failed, the
    dictionary will indicate that instead.

.. create_group_

create_group
-------------
Create a new subscription group. You can add subscriptions to it by calling
modify_group

:Parameters:
    Required - name

    Optional - description

:Returns:
    A status and an id. Or on failure, a status and a message.

    Return fields are:
        - status, (id | message)

.. modify_group_

modify_group
-------------
Modify the attributes of a group with given id. Arguments add_subs and rem_subs
must be an iterable of sub_id's. Similarly, arguments add_users and rem_users
must be an iterable of username's. If a value appears in both an add_* and rem_*
argument, it is ignored.

:Parameters:
    Required - id

    Optional - name, description, add_subs, rem_subs, add_users, rem_users, icon

:Returns:
    A status and a message.

    Return fields are:
        - status, message


============
HYP3 SCRIPTS
============
>>> from asf_hyp3 import scripts

:Functions:
    | download_products_
    | load_granules_

.. download_products_

download_products
-----------------
Calls api.get_products and downloads everything that has not been downloaded yet
to the given directory. Filter arguments will be passed to the api.get_products
call

:Parameters:
    Required::

        api            The api object to use

    Optional::

        directory      The destination folder
        id             The product id to match
        sub_id         The subscription id to match
        sub_name       The subscription name to match
        creation_date  The creation date to match
        verbose        Print verbose output (progress bar and download status)
        threads        The number of products to download at a time

.. load_granules_

load_granules
-------------
Searches through a file and finds all strings that look like S1 granules.

Granule Format::
    S1A_IW_GRDH_1SDV_YYYYMMDDTHHMMSS_YYYYMMDDTHHMMSS_123456_789ABC_89AB

:Parameters:
    Required::

        filename      The name of the file to search through
:Returns:
    A list of all granules found in the file
