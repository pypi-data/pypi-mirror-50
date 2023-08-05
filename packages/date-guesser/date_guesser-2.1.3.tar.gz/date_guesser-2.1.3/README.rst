Date Guesser
============

|Build Status| |Coverage| 

A library to extract a publication date from a web page, along with a measure of the accuracy.
This was produced as a part of the `mediacloud project <https://mediacloud.org/>`_, in order to accurately extract dates from content. 

Installation
------------

The library is available `on PyPI <https://pypi.org/project/date-guesser/>`_, and may be installed with 

.. code-block:: bash

    pip install date_guesser

Quickstart
----------
The date guesser uses both the url and the html to work, and uses some heuristics to decide which of many possible dates might be the best one.

.. code-block:: python
    
    from date_guesser import guess_date, Accuracy
    
    # Uses url slugs when available
    guess = guess_date(url='https://www.nytimes.com/2017/10/13/some_news.html', 
                       html='<could be anything></could>')

    #  Returns a Guess object with three properties
    guess.date      # datetime.datetime(2017, 10, 13, 0, 0, tzinfo=<UTC>)
    guess.accuracy  # Accuracy.DATE
    guess.method    # 'Found /2017/10/13/ in url'

In case there are two trustworthy sources of dates, :code:`date_guesser` prefers the more accurate one

.. code-block:: python
 
    html = '''                                                                     
        <html><head>                                                                   
        <meta property="article:published" itemprop="datePublished" content="2017-10-13T04:56:54-04:00" />         
        </head></html>'''
    guess = guess_date(url='https://www.nytimes.com/2017/10/some_news.html',
                       html=html)
    guess.date  # datetime.datetime(2017, 10, 13, 4, 56, 54, tzinfo=tzoffset(None, -14400))
    guess.accuracy is Accuracy.DATETIME  # True

But :code:`date_guesser` is not led astray by more accurate, less trustworthy sources of information

.. code-block:: python
 
    html = '''                                                                     
        <html><head>                                                                   
        <meta property="og:image" content="foo.com/2016/7/4/whatever.jpg"/>         
        </head></html>'''
    guess = guess_date(url='https://www.nytimes.com/2017/10/some_news.html',
                       html=html)
    guess.date  # datetime.datetime(2017, 10, 15, 0, 0, tzinfo=<UTC>)
    guess.accuracy is Accuracy.PARTIAL  # True   


Future Work
-----------

Languages
^^^^^^^^^

The code does quite poorly on foreign news sources. This page is Ukranian and has a date on it that 
a non-Ukranian could identify, but it is not extracted:

.. code-block:: python
 
    import requests

    guess = guess_date(url='https://www.dw.com/uk/коментар-націоналізм-родом-зі-східної-європи/a-42081385',
                       html=requests.get(url).text)
    guess.date  # None
    guess.accuracy is Accuracy.NONE  # True
    guess.method == 'Did not find anything'  # True


Reckless Mode
^^^^^^^^^^^^^

We keep track of the accuracy of extracted dates, but we do not keep track of the confidence of extracted 
dates being accurate. This may be a way to do more tuning given a particular use case. For example, one
strategy we do *not* employ is a regex for all the date patterns we recognize, since that was far too
error-prone. Such an approach might be preferable to returning :code:`None` in certain cases.


Performance
-----------
We benchmarked the accuracy against the wonderful :code:`newspaper` library, using one hundred urls gathered from each of four very different topics in the :code:`mediacloud` system. This includes blogs and news articles, as well as many urls that have no date (in which case a guess is marked correct only if it returns :code:`None`).  

Vaccines
^^^^^^^^

+---------+--------------+------------+
|         | date_guesser | newspaper  |
+=========+==============+============+
| 1 days  |   **57**     |   48       |
+---------+--------------+------------+
| 7 days  |   **61**     |    51      |
+---------+--------------+------------+
| 15 days |   **66**     |    53      |
+---------+--------------+------------+

Aadhar Card in India
^^^^^^^^^^^^^^^^^^^^

+---------+--------------+------------+
|         | date_guesser | newspaper  |
+=========+==============+============+
| 1 days  |   **73**     |   44       |
+---------+--------------+------------+
| 7 days  |   **74**     |    44      |
+---------+--------------+------------+
| 15 days |   **74**     |    44      |
+---------+--------------+------------+

Donald Trump in 2017
^^^^^^^^^^^^^^^^^^^^

+---------+--------------+------------+
|         | date_guesser | newspaper  |
+=========+==============+============+
| 1 days  |  **79**      |   60       |
+---------+--------------+------------+
| 7 days  |  **83**      |    61      |
+---------+--------------+------------+
| 15 days |  **85**      |    61      |
+---------+--------------+------------+

Recipes for desserts and chocolate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------+--------------+------------+
|         | date_guesser | newspaper  |
+=========+==============+============+
| 1 days  |   **83**     |    65      |
+---------+--------------+------------+
| 7 days  |   **85**     |    69      |
+---------+--------------+------------+
| 15 days |   **87**     |    69      |
+---------+--------------+------------+



.. |Build Status| image:: https://travis-ci.org/mitmedialab/date_guesser.png?branch=master
   :target: https://travis-ci.org/mitmedialab/date_guesser
.. |Coverage| image:: https://coveralls.io/repos/github/mitmedialab/date_guesser/badge.svg?branch=master
   :target: https://coveralls.io/github/mitmedialab/date_guesser?branch=master
