# Datastore
### Currently supported file structures: CSV WAV JSON PICKLE
Python module which loads and saves data structures based on the file extension.

### Dependencies
* json
* csv
* wave
* struct
* importlib
* os
* pickle

All of which are included with python, so there are **no installs required**


### Objective
This module attempts to follow a **generic procedure for reading and writing common data storage formats using only the file extension for guidance**.

The motivation here is as follows; Most of the time, the most generic approach to opening a file will work. It's may not be the most computationaly efficient way, but if loading time is not a bottleneck for your workflow, you might as well spend your time manipulating the data as opposed figuring out how to load it into python. The goal of Datastore is to make implementing these generic approaches as fast as possible. If it doesn't work, well at least you didn't waste much time. Otherwise, you just skipped a monotonous task and can get on with real work.



### Usage
First you need to download the folder named "Datastore" and paste it in your working directory.
```
datastore.save(data, filename)
data = datastore.load(filename)
```

Alternatively, if you want to start from scratch, making all of your own file handlers, then you only need a folder (called whatever you want the module to be named), inside of that you need an `__init__.py` (identical to the one in my `datastore` folder) and an empty folder named `extensions` into which you will place your own file handlers.

### Adding More File Handlers
To add another file extension you ...

* create a folder under datastore/extensions/ with the name of the extension. e.g. if you want to make a handler that can deal with "nonsense.foo" this folder would be named "foo" __in all lowercase letters__
* create a file named `__init__.py`
* in `__init__.py` you must make two functions `load(fname, args)` and `save(data, fname, args)` which must be able to load and save the file properly. args is a dictionary you may use to provide more control over how the functions work

Take a look through the file structure if this does not make sense. It is easier to see the pattern than it is to explain

### Example
This is obviously not a normal use case, but it shows that the procedures for opening these file structures are identical, which is a nice change in my opinion.

```
import datastore

d = [{'id': [1,2,3,4],'otherID':[4,3,2,1]}]
```

save this dict as a pickle
```
datastore.save(d, 'test.pkl')
```
open it back up as a dict
```
d = datastore.load('test.pkl')
```
save it again as a JSON
```
datastore.save(d, 'test.json')
```
open it back up as a dict
```
d = datastore.load('test.json')
```

save it as a pickle again
```
datastore.save(d, 'test.pkl')
```
open it back up
```
d = datastore.load('test.pkl')
```
save it as a csv
```
datastore.save(d, 'test.csv')
```
open it back up
```
d = datastore.load('test.csv')
```
print out the result
```
print(d)
```
