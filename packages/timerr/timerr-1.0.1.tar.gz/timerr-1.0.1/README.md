# Timer Package for Python

This is a simple timer package for python that counts `Down`  
from the time set.  

## Usage

### Scripting

```python
# Import the timer module
import timer

# Create a variable named 'timer' and call the class 'timer'
# Arguments are (hours, mins, secs, log)
# Default is a 1h timer and not to print the time left
# To print the time left, if all args are passsed, use 'log' otherwise copy below
# This sets a timer for 3h 45mins and to print the time left
timer = timer.Timer(3, 45,log='log')
# Run the 'timer' function from the variable
timer.timer()
```

### Interpreter

```python
>>> import timer
>>> timer.Timer(3, 45, 15, 'log').timer()
```

## License & Copyright

Copyright (c) 2019 ItzAfroBoy
This package is under the [MIT License](http://github.com/ItzAfroBoy/timer/LICENSE).  
Under the license, you are able to modify the file  
and serve it as closed-source
