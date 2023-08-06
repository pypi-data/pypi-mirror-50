mypsl
========

**Maintainer:** k dot shenk at gmail dot com

The aim of **mypsl** is to provide a simple interface for querying and filtering the MySQL process list. Over time
the available options have become bloated, so some cases may not be *so simple*.

Installation
------------

**Via PIP:**
``pip install mypsl``

Usage
-----

    ::

        usage: mypsl [-h] [-H HOST] [-p PORT] [-u USER] [-P PASSWD] [-ch CHARSET]
             [--config CONNECT_CONFIG] [-sm SALT_MINION]
             [-l LOOP_SECOND_INTERVAL] [-lm LOOP_MAX] [-dft] [-c COMMAND]
             [-s STATE] [-t TIME] [-d DATABASE] [-q QUERY] [-i] [-isr]
             [--debug] [-o ORDER_BY] [-T] [-v] [--slack] [--kill]
             [-kt KILL_THRESHOLD] [-ka] [-ky] [-kl KILL_LOG] [-klo]

        (mypsl: mypsl: 0.19) :: MySQL Process list watcher & query
        killer.

        optional arguments:
          -h, --help            show this help message and exit

        Connection Options:
          -H HOST, --host HOST  The host to get the process list from. If localhost,
                                we will attempt to find and use the socket file first.
                                (default: localhost)
          -p PORT, --port PORT  The host's port. If the host is localhost, we will
                                attempt to find and use the socket file first.
                                (default: 3306)
          -u USER, --user USER  The user to connect to the host as. (default: root)
          -P PASSWD, --pass PASSWD
                                The password for authentication. (default: )
          -ch CHARSET, --charset CHARSET
                                Charset to use with the database. (default: utf8)
          --config CONNECT_CONFIG
                                Load connection configuration from a file in
                                /root/.mypsl. Just provide the filename. This will
                                override any other connection information provided
                                (default: None)
          -sm SALT_MINION, --salt-minion SALT_MINION
                                Connect to mysql running on a salt minion. Do not use
                                any other connection options with this.
                                mysql:connection:user and mysql:connection:pass must
                                exist in pillar data. (default: None)

        Configuration Options:
          -l LOOP_SECOND_INTERVAL, --loop LOOP_SECOND_INTERVAL
                                Time in seconds between getting the process list.
                                (default: 0)
          -lm LOOP_MAX, --loop_max LOOP_MAX
                                If specified we will stop execution when the loop
                                interval reaches this number (default: None)
          -dft, --default       Run with defaults. Loop interval: 3 seconds, command
                                like query or connect, order by time asc, id asc,
                                truncate query to 1000. (default: False)
          -c COMMAND, --command COMMAND
                                Lookup processes running as this command. (default:
                                None)
          -s STATE, --state STATE
                                Lookup processes running in this state. (default:
                                None)
          -t TIME, --time TIME  Lookup processes running longer than the specified
                                time in seconds. (default: None)
          -d DATABASE, --database DATABASE
                                Lookup processes running against this database.
                                (default: None)
          -q QUERY, --query QUERY
                                Lookup processes where the query starts with this
                                specification. (default: None)
          -i, --id              Only print back the ID of the processes. (default:
                                False)
          -isr, --ignore_system_user
                                Ignore the 'system user' (default: False)
          --debug               Provide debug output. (default: False)
          -o ORDER_BY, --order_by ORDER_BY
                                Order the results by a particular column: "user", "db
                                asc", "db desc", "time desc"...etc (default: None)
          -T, --trim_info       Trim the info field (the query) to 1000 (default:
                                False)
          -v, --version         Show the installed program version and quit. (default:
                                False)
          --slack               Send a notification to slack anytime we kill a query.
                                Slack Auth/Config file must exist @ ~/.slack_auth
                                (default: False)

        Kill Options:
          --kill                Kill the queries that we find. (default: False)
          -kt KILL_THRESHOLD, --kill_threshold KILL_THRESHOLD
                                The kill threshold. If a number is provided, we'll
                                need to hit that many total connections before killing
                                queries. You can set this to 'off' as well, which
                                kills queries no matter how many connections there
                                are. (default: 100)
          -ka, --kill_all       If this flag is provided, we'll attempt to kill
                                everything, not only select queries. Use with
                                caution! (default: False)
          -ky, --kill_yes       If this is provided we won't stop to ask if you are
                                sure that you want to kill queries. (default: False)
          -kl KILL_LOG, --kill_log KILL_LOG
                                Where to log killed queries to, granting permissions
                                to write to this file. (default:
                                /var/log/killed_queries.log)
          -klo, --kill_log_only
                                Only log the queries that would be killed, do not
                                actually kill them (default: False)



Contributing
------------
Suggestions and contributions are welcome. Please fork me and create PRs back to the ``develop`` branch.

