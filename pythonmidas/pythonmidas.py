############################
#
# Name: pythonmidas
#
# Author: Aaron Gallant, Summer 2013
#
# Description:
# Pythonmidas is a class to control a midas session. The commands
# are based on the 'perlmidas' subroutines, ported to python.
#
# 2015.09.25 ATG
# Added Exception classes to handle errors if odb commands fail
#
# 2015.09.28 ATG
# Added dirlisttest(key) which returns (key, value) pairs in a
# directory without needing to split on whitespace.
# This is useful for changing tunes.
############################

import subprocess as MidasSP
import re

dquote = "\""
squote = "\'"
_ODB_SUCCESS = 0
host = ""
expt = ""
midasHost = ""
midasExpt = ""

# Command to access odb
_odb = "odbedit"


# Here we define two classes to handle errors associated with sending commands
# to the odb.

# This error is for when a key is not found.
class KeyNotFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# This error is for when a commands fails for any reason.
class FailedCommand(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def env():
    global host, expt, midasHost, midasExpt

    shell = MidasSP.Popen("echo " + "$MIDAS_SERVER_HOST",
                          shell=True, stdout=MidasSP.PIPE)
    midasHost = shell.communicate()[0].rstrip()
    if midasHost != "":
        host = "-h " + midasHost
    print midasHost

    shell2 = MidasSP.Popen("echo " + "$MIDAS_EXPERIMENT",
                           shell=True, stdout=MidasSP.PIPE)
    midasExpt = shell2.communicate()[0].rstrip()
    if midasExpt != "":
        expt = "-e " + midasExpt
    print midasExpt


def varget(key):
    """
    varget(key) gets the value of the variable \'key\' and returns the
    result.
    """
    result = odbcommand("ls -v", key)
    #print result
    return result


def varset(key, value):
    "varset(key,value) sets the variable \'key\' to the supplied \'value\'."
    #result = odbcommand("set", key, value)
    #print result
    #return result
    odbcommand("set", key, value)


def sendmessage(name, message):
    """
    sendmessage(name,message) sends message with the identifier name to the odb
    message stream.
    """
    #result = odbcommand("msg " + name, message)
    #print result
    #return result
    odbcommand("msg " + name, message)


def dirlisttest(key):
    """
    dirlisttest returns all of the (key, value) pairs in a directory.
    It is constructed in a way that the amount of whitespace in a key name
    or in a value will not cause issues when splitting.
    """
    keyvar = odbcommand("ls", key).split("\n")
    values = odbcommand("ls -v", key).split("\n")

    dirkeys = [[x.rsplit(y, 1)[0].rstrip(), y] for x, y in zip(keyvar, values)]

    #print dirkeys
    return dirkeys


def dirlist(key, flag=""):
    """
    dirlist(key) lists the contents of \'key\'.
    """
    result = odbcommand("ls " + flag, key)
    print result
    # Split on whitespaces of 10 spaces.
    # Hope some user didn't put in the same amount
    #return [re.split("\s{10,}", x) for x in result.split("\n")]
    return dirlisttest(key)


def startrun():
    "startrun() starts a midas run."
    #result = odbcommand("start now")
    #print result
    #return result
    odbcommand("start now")


def stoprun():
    "stoprun() stops the current midas run."
    #result = odbcommand("stop now")
    odbcommand("stop now")


def odbcommand(command, key=None, value=None):
    """
    odbcommand(command,key=None,value=None) constructs an odb command
    from the user given 'command'. The command is built depending on
    if 'key' and 'value' are assigned. The general form is:\n
           command, command 'key', command 'key' 'value'
    """
    if key is None:
        cmd = dquote + command + dquote
    elif value is None:
        cmd = dquote + command + " " + squote + key + squote + dquote
    else:
        cmd = (dquote + command + " " + squote + key + squote + " " +
               squote + str(value) + squote + dquote)

    shell = MidasSP.Popen(_odb + " -c " + cmd, shell=True, stdout=MidasSP.PIPE)
    # wait until profess is finished, and get the response
    ans = shell.communicate()[0].rstrip()

    # test that command executed successfully
    if shell.returncode != _ODB_SUCCESS:
        #msg = "Command "+cmd+" not sent to the odb correctly."
        #sendmessage("pythonmidas",msg)
        print "Error sending " + cmd
        #raise Exception("pythonmidas: Execution of command \'"
        #                + cmd + "\' failed.")
        raise FailedCommand("pythonmidas: Execution of command '"
                            + cmd + "' failed.")

    # Check that key exists.
    # If not raise an exception and send a message to MIDAS.
    if re.search("^key\s.{1,1024}\snot found$", ans):
        sendmessage("pythonmidas", "Key: " + key + " not found.")
        #raise Exception("pythonmidas: Key " + key + " not found.")
        raise KeyNotFound("pythonmidas: Key " + key + " not found.")

    return ans
