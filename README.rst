|Build Status|

Snipping
========

A tool to edit and run **python** snippet in real time.

Usage
=====

Just run Snipping like this,

::

    $ snipping

Also you can specify the snippet filename.

If the file exists, Snipping will read the content, and save to the file
when you ``Save``, if not, Snipping will start from empty snippet, and
save to the file on command.

::

    $ snipping [path/to/snippet]

Special thanks
==============

-  `prompt\_toolkit <http://github.com/jonathanslenders/python-prompt-toolkit>`__
   for the terminal interface.

Notice
======

In ``snipping``, ``sys.stdout`` and ``sys.stderr`` is redirected to a
``stringIO``, so actions related to them may be different from the
original Python.

.. |Build Status| image:: https://travis-ci.org/yittg/Snipping.svg?branch=master
   :target: https://travis-ci.org/yittg/Snipping
