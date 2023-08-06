# python-scpilib
Python module to provide scpi functionality to an instrument under a **GPLv3+** license.


![license GPLv3+](https://img.shields.io/badge/license-GPLv3+-green.svg) ![4 - Beta](https://img.shields.io/badge/Development_Status-4_--_beta-yellow.svg) ![Codeship badge](https://codeship.com/projects/d4d61020-736f-0134-5151-52e76941e580/status?branch=master) 

![about](https://img.shields.io/badge/Subject-Industrial_Control_Systems-orange.svg?style=social) ![about](https://img.shields.io/badge/Subject-Instrumentation-orange.svg?style=social)


This project has started as a *toy-project* to test the [Skippy](https://github.com/srgblnch/skippy) Tango device server. But it has evolved to become a python library to provide *scpi commands tree* functionality in the **instrument side**. It has been found another project under the name [scpi](https://github.com/rambo/python-scpi) that works like the skippy but independent of any thing similar to Tango.

SCPI library is based on these standards, but *does NOT (fully) complain them yet*.
 - [SCPI-99](http://www.ivifoundation.org/docs/scpi-99.pdf)
 - [IEEE 488.2-2004](http://dx.doi.org/10.1109/IEEESTD.2004.95390)

## Basic features

- [x] Command three definition with read-only and read/write attributes.
- [x] Special commands (hint, they start by '*')
- [x] Concatenation of commands (hint ';' separator).
- [x] Listen network connections (only local/loopback or open to an interface).
- [x] Channels keywords in a command (even more than one channel separation).
- [x] Array-like answers (hint '#NMMMMMMMMMxxxxx...\n')

## Features requested (Wish/ToDo List)

- [x] Data formats for the arrays ('ASCII' but also binary floats with 1, 2, 4 or 8 Byte codification).
- [ ] List the minimum special commands to be setup for an instrument (hint '*IDN?').
- [x] Support for [IPv6](https://en.wikipedia.org/wiki/IPv6).
- [x] Enumerate type to the command setters (hint, allowedArgins).
- [ ] Listen more channels than network (TBD what other channels can be).
- [ ] "autodoc" using the scpi tree.
- [x] Read commands with parameters after the '?' separator.
- [x] Write commands without parameters (no need a ' ' separator).
- [x] Lock write access: for one of the clients or internally by the server. Side by the "SYST:LOCK" from the standard, that is included also, this is a "SYST:WLOCK".
  - [ ] Even there is an access lock, should be allowed the command "SYST:LOCK:OWNEr?"
  - Tests pending
- [x] Avoid the internal *Logger* and use the [python logging](https://docs.python.org/2/library/logging.html).
- [ ] Compatibility with [python3](https://docs.python.org/3.4/) without losing [python2](https://docs.python.org/2.7/).
- [ ] Compile with [cython](http://cython.org/) to optimise the execution.

## Other ideas to study

* [ ] Event subscription. Unknown if scpi has something about this in the specs.
* [ ] Use SSL.
* [ ] Authentication and ACLs.

## Installation

It has been thought to use setuptools (and someday cython will be introduced 
to have a compiled option to increase performance with long sets of commands).

```
$ python setup.py build
$ sudo python setup.py install
```

The install can be set with a prefix. One have to highlight the current development stage, we are using in one instrument in preproduction stage. One should use carefully before use in production.

## Usage

Different approaches has been prepared to have instrument side support. The 
most simple shall be to simply build a scpi object in your instrument:

```python
import scpilib
scpiObj = scpilib.scpi()
```

With no paramenter configuration, the object assumes the communication will be
made by network and *only* listen the localhost (in ipv4 and ipv6). See the 
help for further information.

The object created doesn't have any command configured, except the ones build 
internally for its behaviour configuration (That is the '*DataFormat*' and 
soon the *Write Lock* functionality).

There are some different ways to prepare this object to respond to specific 
requests. They can be build before and passed to the constructor, or use a 
command to add:

```python
currentObj = AttrTest()
scpiObj.addCommand('source:current:upper',
                   readcb=currentObj.upperLimit,
                   writecb=currentObj.upperLimit)
```

**IMPORTANT:** _The callbach functions to the commands must return as soon 
as possible. The developer of the instrument control must have on mind that
any delay introduced by this call will be accumulated when one request
contains multple queries._ It is recommended to write your own queue to process
any request that takes time and return a
[wilco](https://www.urbandictionary.com/define.php?term=Wilco).

The *AttrTest()* object can be found in the *commands.py* file and it's used 
in the test approach. What the previous code generates are:

* 'source' to the root in the scpi command tree,
* 'current' as an intermediate node, and 
* 'upper' a leaf that will be readable and writable.

```
SOURce:
        CURRent:
                UPPEr
```

With this sample code, the object shall be listening on the (loopback) network 
and sending to the port *5025* the string 'SOUR:CURR:UPPE?', we will receive 
back an string with the representation of the execution of 
'currentObj.upperLimit()'.


### Special commands

There is a set of minimum commands that shall be implemented in any device that
like to be scpi compiant. Those commands are tagged starting with '*' symbol.

#### 1) Identify yourself

The most important of them is the identification: '*IDN?'. As it finishes with 
a '?' symbol, it means a request to the instrument. The answer is a string 
with 4 elements coma separated:
* Manufacturer: identical for all the instruments of a single company
* Instrument: Common for all the instrument in the same class, but It shall 
never contain the word 'MODEL'.
* Serial Number: specific for the responding instrument to the request.
* Version (and revision) of the software embedded in the instrument.

To build this command, one should have an function that returns the string 
that will be sent back. For example, in the code there is a class 
InstrumentIdentification() where the 4 fields can be set and there is one 
method that returns the string. Then, to a scpi object one can add it:

```python
scpiObj.addSpecialCommand('IDN',identity.idn)
```

With this one have the most very basic functional scpi listener. And mandatory 
for the [Skippy](https://github.com/srgblnch/skippy) Tango device server, 
because this identification is used to distinguish between the supported 
instruments to load the corresponding set of commands.

#### 2) Other special commands

This section can be extended but now it is only a list of the excepted 
mandatory commands that the SCPI shall have (even many commercial products 
didn't do).

- '*CLS': Clear Status Command
- '*ESE[?]': Event Status Enable
- '*ESR?': Event Status Register
- '*OPC[?]': Operation Complete
- '*RST': Reset
- '*SRE[?]': Service Request Enable
- '*STB?': Status Byte
- '*TST?': Self-test
- '*WAI': Wait-to-continue

## Channels in the instrument

It has been shown how to setup a minimal tree of commands, but often this 
kind of instruments have components that are channels. Like an oscilloscope, 
an electrometer, or any other that one can develope.

Those commands have the peculiarity that their key work ends with a number
(specifically 2 decimal digit number string starting with a 0 if need be), at 
the same time their left part of the keyword has this variable lenght feature.

There has been implemented one way to add this channel feature, and only one
channel element can be set in the branch of the tree.

```python
nChannels = 8
chCmd = 'channel'
chObj = scpiObj.addChannel(chCmd, nChannels, scpiObj._commandTree)
chCurrentObj = ChannelTest(nChannels)
chVoltageObj = ChannelTest(nChannels)
for (subcomponent, subCmdObj) in [('current', chCurrentObj),
                                  ('voltage', chVoltageObj)]:
    subcomponentObj = scpiObj.addComponent(subcomponent, chObj)
    for (attrName, attrFunc) in [('upper', 'upperLimit'),
                                 ('lower', 'lowerLimit'),
                                 ('value', 'readTest')]:
        if hasattr(subCmdObj, attrFunc):
            cbFunc = getattr(subCmdObj, attrFunc)
            if attrName == 'value':
                default = True
            else:
                default = False
            attrObj = scpiObj.addAttribute(attrName, subcomponentObj,
                                           cbFunc, default=default)
```

With this iterative way, the scpi tree will have a component near the root that
will accept channel differentiation in the readings and writtings. The tree
representation will be like:

```
CHANnelNN:
        CURRent: (default 'value') 
                UPPEr
                LOWEr
                VALUe
        VOLTage: (default 'value') 
                UPPEr
                LOWEr
                VALUe
```

where the NN following the 'channel' key will be a string number between '01'
and '08' (supporting up to '99' if it is setup this way).

Then the command 'CHAN01:CURR:VALU?' will call a different read method than a
command 'CHAN05:CURR:VALU?'.

