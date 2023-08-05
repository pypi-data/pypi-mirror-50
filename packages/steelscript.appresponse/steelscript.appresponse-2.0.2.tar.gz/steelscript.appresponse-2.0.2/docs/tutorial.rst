.. py:currentmodule:: steelscript.appresponse.core

SteelScript AppResponse Report Tutorial
=======================================

This tutorial will show you how to run a report against
an AppResponse appliance using SteelScript for Python.
This tutorial assumes a basic understanding of Python.

The tutorial has been organized so you can follow it sequentially.
Throughout the example, you will be expected to fill in details
specific to your environment.  These will be called out using a dollar
sign ``$<name>`` -- for example ``$host`` indicates you should fill
in the host name or IP address of an AppResponse appliance.

Whenever you see ``>>>``, this indicates an interactive session using
the Python shell.  The command that you are expected to type follows
the ``>>>``.  The result of the command follows.  Any lines with a
``#`` are just comments to describe what is happening.  In many cases
the exact output will depend on your environment, so it may not match
precisely what you see in this tutorial.

AppResponse Object
------------------

Interacting with an AppResponse Applicance leverages two key classes:

* :py:class:`AppResponse <appresponse.AppResponse>` - provides the primary interface to the appliance, handling initialization, setup,
and communication via REST API calls.

* :py:class:`Report <reports.Report>` - talks through the AppResponse object to create new report and pull data when the report is completed.

To start, start Python from the shell or command line:

.. code-block:: bash

   $ python
   Python 2.7.13 (default, Apr  4 2017, 08:47:57)
   [GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.38)] on darwin
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

Once in the python shell, let's create an AppReponse object:

.. code-block:: python

   >>> from steelscript.appresponse.core.appresponse import AppResponse
   >>> from steelscript.common import UserAuth

   >>> ar = AppResponse('$host', auth=UserAuth('$username', '$password'))

In the above code snippet, we have created an AppResponse object, which
represents a connection to an AppResponse appliance.
The first argument is the hostname or IP address of the AppResponse
appliance.  The second argument is a named parameter and identifies
the authentication method to use -- in this case, simple
username/password is used.

As soon as the AppResponse object is created, a connection is established
to the AppResponse appliance, and the authentication credentials are
validated.  If the username and password are not correct, you will
immediately see an exception.

The ``ar`` object is the basis for all communication with the AppResponse
appliance, whether that is running a report, updating host groups or
downloading a pcap file. Now lets take a look at the basic information
of the AppResponse appliance that we just connected to:

.. code-block:: python

   >>> info = ar.get_info()

   >>> info['model']
   u'VSCAN-2000'

   >>> info['sw_version']
   u'11.2.0 #13859'

   # Let's see the entire info structure
   >>> info
   {u'device_name': u'680-valloy1',
    u'hw_version': u'',
    u'mgmt_addresses': [u'10.33.158.77'],
    u'model': u'VSCAN-2000',
    u'serial': u'',
    u'sw_version': u'11.2.0 #13859'}


Creating a Report Script
------------------------

Let's create our first script. We're going to write a simple script that
runs a report against a packets capture job on our AppResponse
appliance.

This script will get packets from a running packets capture job. To start,
make sure the targeted AppResponse appliance has a running packets
capture job.

Now create a file called ``report.py`` and insert the following code:

.. code-block:: python

   import pprint

   from steelscript.appresponse.core.appresponse import AppResponse
   from steelscript.common import UserAuth
   from steelscript.appresponse.core.reports import DataDef, Report
   from steelscript.appresponse.core.types import Key, Value, TrafficFilter
   from steelscript.appresponse.core.reports import SourceProxy

   # Fill these in with appropriate values
   host = '$host'
   username = '$username'
   password = '$password'

   # Open a connection to the appliance and authenticate
   ar = AppResponse(host, auth=UserAuth(username, password))

   packets_source = ar.get_capture_job_by_name('default_job')

   source = SourceProxy(packets_source)

   columns = [Key('start_time'), Value('sum_tcp.total_bytes'), Value('avg_frame.total_bytes')]

   granularity = '10'

   resolution = '20'

   time_range = 'last 1 minute'

   data_def = DataDef(source=source, columns=columns, granularity=granularity,
                      resolution=resolution, time_range=time_range)

   data_def.add_filter(TrafficFilter('tcp.port==80'))

   report = Report(ar)
   report.add(data_def)
   report.run()
   pprint.pprint(report.get_data())

Be sure to fill in appropriate values for ``$host``, ``$username`` and
``$password``. Run this script as follows and you should see something
like the following:

.. code-block:: bash

   $ python report.py
    [(1510685000, 3602855, 772.979),
     (1510685020, 4109306, 754.001),
     (1510685040, 657524, 779.057)]

Let's take a closer look at what this script is doing.

Importing Classes
^^^^^^^^^^^^^^^^^

The first few lines are simply importing a few classes that we will be using:

.. code-block:: python

   import pprint

   from steelscript.appresponse.core.appresponse import AppResponse
   from steelscript.common import UserAuth
   from steelscript.appresponse.core.reports import DataDef, Report
   from steelscript.appresponse.core.types import Key, Value, TrafficFilter
   from steelscript.appresponse.core.reports import SourceProxy

Creating an AppResponse object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, we create an AppResponse object that establishes our connection to
the target appliance:

.. code-block:: python

   # Open a connection to the appliance and authenticate
   ar = AppResponse(host, auth=UserAuth(username, password))

Creating a Data Definition Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This section describes how to create a data definition object.

Creating a SourceProxy object
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Now we need to create a SourceProxy object which carries the information
of source where data will be fetched.

.. code-block:: python

   packets_source = ar.get_capture_job_by_name('default_job')

   source = SourceProxy(packets_source)

We first obtain a packet capture job object by using the name of the capture job.

.. code-block:: python

   packets_source = ar.get_capture_job_by_name('default_job')

To run a report against a Pcap file source, the file object can be derived as below:

.. code-block:: python

   packets_source = ar.get_file_by_id('$file_id')

Then we need to initialize a SourceProxy object as below:

.. code-block:: python

   source_proxy = SourceProxy(packets_source)

To run a report against a non-packets source, the SourceProxy object is initialized by
just using the name of the source as below:

.. code-block:: python

   source_proxy = SourceProxy(name='$source_name')

To know the available source names, just execute the following command in shell:

.. code-block:: bash

   $ steel appresponse sources $host -u $username -p $password

   Name                 Groups                                       Filters Supported on Metric Columns  Granularities in Seconds
   ------------------------------------------------------------------------------------------------------------------------------------------------------
   packets              Packets                                      False                                0.1, 0.01, 0.001, 1, 10, 60, 600, 3600, 86400
   aggregates           Application Stream Analysis, Web             True                                 60, 300, 3600, 21600, 86400
                        Transaction Analysis, UC Analysis
   dbsession_summaries  DB Analysis                                  False                                60, 300, 3600, 21600, 86400
   sql_summaries        DB Analysis                                  False                                60, 300, 3600, 21600, 86400

It shows that there are totally 4 supported sources. Note the following:

- Source ``aggregates`` belongs to the 3 groups: Application Stream Analysis, Web Transaction Analysis and UC Analysis.

- Filters can be applied on the metric columns for the source ``aggregates``.

- Filters are not supported on metric columns for source ``packets``, ``dbsession_summaries`` and ``sql_summaries``.

We will support native methods for accessing source information via Python
in an upcoming release.

Choosing Columns
>>>>>>>>>>>>>>>>

Then we select the set of columns that we are interested in collecting. Note
that AppResponse supports multiple sources. Each source supports a different set
of columns.  Each column can be either a key column or a value column.
Each row of data will be aggregated according to the set of key columns selected.
The value columns define the set of additional data to collect per row. In this
example, we are asking to collect total bytes for tcp packets and average total
packet length for each resolution bucket.

To help identify which columns are available, just execute the helper command
as below in your shell prompt.

.. code-block:: bash

   $ steel appresponse columns $host -u $usernmae -p $password --source $source_name

For instance, to know the available columns within source ``packets``, we execute the
command in shell as:

.. code-block:: bash

   $ steel appresponse columns $host -u $username -p $password --source packets

     ID                                                Description                                        Type       Metric   Key/Value
     ----------------------------------------------------------------------------------------------------------------------------------
     ...
     avg_frame.total_bytes                             Total packet length                                number     True     Value
     ...
     start_time                                        Used for time series data. Indicates the           timestamp  ----     Key
                                                       beginning of a resolution bucket.
     ...
     sum_tcp.total_bytes                               Number of total bytes for TCP traffic              integer    True     Value

Note that it would be better to pipe the output using ``| more`` as there can be more
than 1000 rows.

Construct a list of columns, including both key columns and value columns in
your script as shown below.

.. code-block:: python

   columns = [Key('start_time'), Value('sum_tcp.total_bytes'), Value('avg_frame.total_bytes')]

We will support native methods for accessing column information via Python in an upcoming release.

Setting Time Fields
>>>>>>>>>>>>>>>>>>>

Now it is time to set the time related criteria fields. We firstly need to see the possible
granularity values that the interested source supports. Running the below command in shell.

.. code-block:: bash

   $ steel appresponse sources $host -u $username -p $password

   Name                 Groups                                       Filters Supported on Metric Columns  Granularities in Seconds
   ------------------------------------------------------------------------------------------------------------------------------------------------------
   packets              Packets                                      False                                0.1, 0.01, 0.001, 1, 10, 60, 600, 3600, 86400
   aggregates           Application Stream Analysis, Web             True                                 60, 300, 3600, 21600, 86400
                        Transaction Analysis, UC Analysis
   dbsession_summaries  DB Analysis                                  False                                60, 300, 3600, 21600, 86400
   sql_summaries        DB Analysis                                  False                                60, 300, 3600, 21600, 86400

As can be seen, source ``packets`` supports graunularity values of ``0.1``,
``0.01``, ``0.001``, ``1``, ``10``, ``60``, ``600``, ``3600`` and ``86400`` (as in seconds).

.. code-block:: python

   granularity = '10'

   resolution = '20'

   time_range = 'last 1 minute'

Setting granularity to ``10`` means the data source computes a
summary of the metrics it received based on intervals of ``10`` seconds.

Resolution is a setting in addition to granularity that tells the
data source to aggregate the data further. Its numeric value must be
multiple of the requested granularity value. In the script, the data
will be aggregated on 20-second intervals. Setting resolution is optional.

If resolution is taken out from the script, the output would consist of
10-second summaries instead of 20-second aggregated records, similar as below.

.. code-block:: bash

   $ python report.py
    [(1510687770, 911456, 784.386),
     (1510687780, 1672581, 780.85),
     (1510687790, 1709843, 776.143),
     (1510687800, 1338178, 797.484),
     (1510687810, 1368713, 771.541),
     (1510687820, 545244, 791.356)]

The parameter ``time_range`` specifies the time range for which the data source computes
the metrics. Other valid formats include "``this minute``", "``previous hour``" and
"``06/05/17 17:09:00 to 06/05/17 18:09:00``".

Initializing Data Definition Object
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

With all the above values derived, we can now create a ``DataDef`` object as below.

.. code-block:: python

   data_def = DataDef(source=source, columns=columns, granularity=granularity, time_range=time_range)

Adding Traffic filters
>>>>>>>>>>>>>>>>>>>>>>

To filter the data, it is easy to add traffic filters to the ``DataDef`` object. Firstly let us
create a traffic filter as below.

.. code-block:: python

   tf = TrafficFilter('tcp.port==80')

The above filter is a ``steelfilter`` traffic filter that output records with ``tcp.port == 80``.
Note that running the ``sources`` commmand script can show whether filters can be applied on metric
columns for each source.

It is worth mentioning that ``packets`` source also supports ``bpf`` filter and ``wireshark`` filter.
They both have their own syntax and set of filter fields. Other sources do not support either ``bpf``
filter or ``wireshark`` filter.

``bpf`` filter and ``wireshark`` filter can be created as below.

.. code-block:: python

   bpf_filter = TrafficFilter('port 80', type_='bpf')
   wireshark_filter = TrafficFilter('tcp.port==80', type_='wireshark')

Now we can add the filter to the ``DataDef`` object.

.. code-block:: python

   data_def.add_filter(tf)

You can create multiple filters and add them to the ``DataDef`` object one by one using the above method.

Running a report
>>>>>>>>>>>>>>>>

After creating the data definition object, then we are ready to run a report as below:

.. code-block:: python

   # Initialize a new report
   report = Report(ar)

   # Add one data definition object to the report
   report.add(data_def)

   # Run the report
   report.run()

   # Grab the data
   pprint.pprint(report.get_data())

Currently, we only support one data definition per each report instance. Next release
will include the ability to run multiple data definitions per each report instance. The
reason for running multiple data definitions is to reuse same data source between data
definitions and yield much performance gain as a result.

Extending the Example
---------------------

As a last item to help get started with your own scripts, we will extend our example
with one helpful feature: table outputs.

Rather than show how to update your existing example script, we will post the new
script, then walk through key differences that add the feature.

Let us create a file ``table_report.py`` and insert the following code:

.. code-block:: python

   from steelscript.appresponse.core.appresponse import AppResponse
   from steelscript.common import UserAuth
   from steelscript.appresponse.core.reports import DataDef, Report
   from steelscript.appresponse.core.types import Key, Value, TrafficFilter
   from steelscript.appresponse.core.reports import SourceProxy
   # Import the Formatter class to output data in a table format
   from steelscript.common.datautils import Formatter

   # Fill these in with appropriate values
   host = '$host'
   username = '$username'
   password = '$password'

   # Open a connection to the appliance and authenticate
   ar = AppResponse(host, auth=UserAuth(username, password))

   packets_source = ar.get_capture_job_by_name('default_job')

   source_proxy = SourceProxy(packets_source)

   columns = [Key('start_time'), Value('sum_tcp.total_bytes'), Value('avg_frame.total_bytes')]

   granularity = '10'

   resolution = '20'

   time_range = 'last 1 minute'

   data_def = DataDef(source=source_proxy, columns=columns, granularity=granularity,
                      resolution=resolution, time_range=time_range)

   data_def.add_filter(TrafficFilter('tcp.port==80'))

   report = Report(ar)
   report.add(data_def)
   report.run()

   # Get the header of the table
   header = report.get_legend()

   data = report.get_data()

   # Output the data in a table format
   Formatter.print_table(data, header)

Be sure to fill in appropriate values for ``$host``, ``$username`` and
``$password``. Run this script as follows and you should see report
result is rendered in a table format as the following:

.. code-block:: bash

   $ python table_report.py

    start_time    sum_tcp.total_bytes    avg_frame.total_bytes
    --------------------------------------------------------------
    1510685000    3602855                772.979
    1510685020    4109306                754.001
    1510685040    657524                 779.057

As can be seen from the script, there are 3 differences.

First, we import the ``Formatter`` class as below:

.. code-block:: python

   from steelscript.common.datautils import Formatter

After the report finished running, we obtain the header of the
table, which is essentially a list of column names that match the
report result, shown as below:

.. code-block:: python

   header = report.get_legend()

At last, the ``Formatter`` class is used to render the report result in
a nice table format, shown as below:

.. code-block:: python

   Formatter.print_table(data, header)
