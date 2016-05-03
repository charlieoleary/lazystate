# lazyState

lazyState is a simple Python class that allows you to track the state of something (anything!) and get an exit code based on supplied variables.

## Wait, what?

Here's the problem.  You're using Sensu to monitor your infrastructure but you don't want to use the Sensu Plugin for one reason or another.  Maybe it's because you're re-writing your checks in Python instead of Ruby and don't want to use the Python version of the plugin, or you simply want to make it easier to write quick checks - doesn't matter.

When you're not using the Sensu Plugin you don't have the ability to track how many times a check has failed, so you can't escalate warnings to critical alerts, and this is obviously not desirable.  This is where lazyCheck comes in.  Simply process your check in a manner that it returns success or failure then let lazyState do the rest.

## Installation

Simply copy the lazystate.py to your /etc/sensu/plugins directory (or whatever else you're using lazyState for) and import it into your Python script.

```python
#! /usr/bin/python

import sys
from lazystate import lazyState
```

## Usage

1. Perform a simple check.
2. When you check for success or failure, include lazyState in the exit code.

```python
#! /usr/bin/python

import sys
from lazystate import lazyState

if (check_succeeded == True):
  print("The check succeeded!")
  sys.exit( lazyState("my_check_name").updateState() )
else:
  print("The check failed!")
  sys.exit( lazyState("my_check_name", True).updateState() )
```

It's important to note that the check name ("my_check_name" in this example) MUST be a consistent string.

Additionally, some customization can be done by passing additional parameters into the lazyState class.  These include:

* Fails before warning (default: 3)
* Fails before critical (default: 5)
* State file storage directory (default: /tmp/states)
* State file storage extension (default: .lazystate)

These are passed into the class as follows:

```python
lazyState("my_check_name", True, 5, 10, "/tmp/lazystate", ".lzyst").updateState() 
```

## Contributing

1. Fork it.
2. Create your feature branch using bugs/ or features/ prefix.
3. Commit your changes.
4. Push to the branch.
5. Create a pull request with an explanation of your changes.

## History

2016-05-02: Initial Release

## To Do

* Hash file identifier.
* Handle argument passing better.

## Credits

Written by Charlie O'Leary, inspired by Sensu.

## License

MIT License
