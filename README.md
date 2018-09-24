# Overview

This is a simple Sokoban game environment.
The level (map or problem) consists of 7 digits as described below table.
This difinition is from [RosettaCode](www.rosettacode.org/wiki/Sokoban)

|digit(ch)|meaning|
|:--|:--|
|0( )|empty(floor)|
|1(#)|wall|
|2(@)|player|
|3($)|box|
|4(.)|goal|
|5(+)|player on a goal|
|6(*)|box on a goal|

# How to play

You can play Sokonban by below command.
In this case, an example level is running.

```sh
$ python3 sokoban.py
```

You can also play with your original level.
The level can be given by a string or a file.

When you give a level with a file, please refer the examples in level directory.
Also, when you give a level with a string, please refere the example in sokoban.py.

```sh
# with file
$ python3 sokoban.py --mdoe='ch' --level=./level/level1.dat
```
