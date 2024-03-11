# Full Name Splitter

Human names are complicated. They don't necessarily follow any rules. Here's [a good article about the complexities of names](https://www.w3.org/International/questions/qa-personal-names).

As that article advises, it's ideal to just store a user's full name, and not assume anything about the form the name takes.

However, there are times when it is necessary to have a split given name and family name. Such as when integrating with another system that made different design choices.

This package does a best-guess attempt to split a full name string into given name and family name. For many Western names, it will get it right. It knows about some common family name prefixes used in many European-language names, and initials. It removes salutations (`Miss`, `Doctor`, etc) and suffixes (`III`, `Jr`, etc).


## Web service

```
$ docker-compose up -d --build
$ curl 'localhost:8080?full_name=Sasha%20Kantoriz'
{"first_name":"Sasha","last_name":"Kantoriz"}
```

## Examples

```python
from splitter import FullNameSplitter

splitter("George H. W. Bush")
# => ["George H. W.", "Bush"]

splitter("Kevin J. O'Connor")
# => ["Kevin J.", "O'Connor"]

splitter("Thomas G. Della Fave")
# => ["Thomas G.", "Della Fave"]

splitter("Gabriel Van Helsing")
# => ["Gabriel", "Van Helsing"]

# If full name isn't complete, it tries to split partially:

splitter("George W.")
# => ["George W.", null]

splitter("George")
# => ["George", null]

splitter("Van Helsing")
# => [null, "Van Helsing"]

splitter("d'Artagnan")
# => [null, "d'Artagnan"]
```

If it can't split a name correctly, it is possible to split by comma:

```python
splitter("John Quincy Adams")
# => ["John Quincy", "Adams"]

splitter("John, Quincy Adams")
# => ["John", "Quincy Adams"]
```

## Copyright

[Original Ruby version](https://github.com/pahanix/full-name-splitter) created by Pavel Gorbokon, with contributions by Michael S. Klishin and Trevor Creech.

This Python port by [Felipe Hertzer](https://www.linkedin.com/in/felipehertzer/).

Released under the MIT license.
