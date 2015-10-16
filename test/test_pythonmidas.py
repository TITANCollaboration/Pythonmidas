#!/usr/bin/env python
"""Unit tests for the pythonrc module."""

import mock
from unittest import TestCase
from pythonmidas import pythonmidas as Midas


class StandAloneTests(TestCase):

    def test_KeyNotFound(self):
        myException = Midas.KeyNotFound("test message")

        try:
            raise myException
        except Exception as e:
            self.assertEqual(e.value, "test message")
            self.assertEqual(str(e), "'test message'")

    def test_FailedCommand(self):
        myException = Midas.FailedCommand("test message")

        try:
            raise myException
        except Exception as e:
            self.assertEqual(e.value, "test message")
            self.assertEqual(str(e), "'test message'")

    @mock.patch('pythonmidas.pythonmidas.MidasSP')
    def test_env(self, mock_sp):
        myshell1 = mock.MagicMock()
        myshell1.communicate.return_value = ["titan01", "other"]
        myshell2 = mock.MagicMock()
        myshell2.communicate.return_value = ["mpet", "other"]
        mock_sp.Popen.side_effect = [myshell1, myshell2]

        Midas.env()

        self.assertEqual(Midas.host, "-h titan01")
        self.assertEqual(Midas.expt, "-e mpet")

        self.assertEqual(mock_sp.Popen.call_count, 2)

    @mock.patch('pythonmidas.pythonmidas.odbcommand')
    def test_varget(self, mock_odbcommand):
        mock_odbcommand.return_value = "return value"

        result = Midas.varget("key")

        self.assertEqual(result, "return value")
        mock_odbcommand.assert_called_with("ls -v", "key")

    @mock.patch('pythonmidas.pythonmidas.odbcommand')
    def test_varset(self, mock_odbcommand):
        mock_odbcommand.return_value = "ans"

        key = "/path/to/key"
        value = "value"

        result = Midas.varset(key, value)

        self.assertEqual(result, None)
        mock_odbcommand.assert_called_once_with("set", key, value)

    @mock.patch('pythonmidas.pythonmidas.odbcommand')
    def test_sendmessage(self, mock_odbcommand):
        name = "Test"
        message = "test message"

        result = Midas.sendmessage(name, message)

        self.assertEqual(result, None)
        mock_odbcommand.assert_called_once_with("msg " + name, message)

    @mock.patch('pythonmidas.pythonmidas.odbcommand')
    def test_dirlisttest(self, mock_odbcommand):
        mock_odbcommand.side_effect = ["key1          value1\n" +
                                       "key2          value2\n" +
                                       "key3          value3\n" +
                                       "key4          value4\n" +
                                       "key5          value5\n",
                                       "value1\nvalue2\nvalue3\n" +
                                       "value4\nvalue5"]

        expected = [["key1", "value1"],
                    ["key2", "value2"],
                    ["key3", "value3"],
                    ["key4", "value4"],
                    ["key5", "value5"]]
        result = Midas.dirlisttest("/path/to/dir/")

        self.assertEqual(result, expected)

        calls = [mock.call("ls", "/path/to/dir/"),
                 mock.call("ls -v", "/path/to/dir/")]
        self.assertEqual(mock_odbcommand.call_args_list, calls)

    @mock.patch('pythonmidas.pythonmidas.dirlisttest')
    @mock.patch('pythonmidas.pythonmidas.odbcommand')
    def test_dirlist(self, mock_odbcommand, mock_dirlisttest):
        mock_odbcommand.return_value = "nothing"
        mock_dirlisttest.return_value = "value"

        result = Midas.dirlist("/a/path/")

        self.assertEqual(result, "value")
        mock_odbcommand.assert_called_once_with("ls " + "", "/a/path/")
        mock_dirlisttest.assert_called_once_with("/a/path/")

    @mock.patch('pythonmidas.pythonmidas.odbcommand')
    def test_startrun(self, mock_odbcommand):
        result = Midas.startrun()

        self.assertEqual(result, None)
        mock_odbcommand.assert_called_once_with("start now")

    @mock.patch('pythonmidas.pythonmidas.odbcommand')
    def test_stoprun(self, mock_odbcommand):
        result = Midas.stoprun()

        self.assertEqual(result, None)
        mock_odbcommand.assert_called_once_with("stop now")

    @mock.patch('pythonmidas.pythonmidas.sendmessage')
    @mock.patch('pythonmidas.pythonmidas.MidasSP')
    def test_odbcommand(self, mock_sp, mock_message):
        mocks = [mock_sp, mock_message]

        myshell = mock.MagicMock()
        myshell.communicate.return_value = ["a1", "a2"]
        myshell.returncode = 0  # 0 == SUCCESS
        mock_sp.Popen.return_value = myshell

        # Call with only command:
        result = Midas.odbcommand("command")
        expected = "a1"
        command = Midas._odb + " -c " + "\"" + "command" + "\""

        self.assertEqual(result, expected)
        mock_sp.Popen.assert_called_once_with(command,
                                              shell=True,
                                              stdout=mock_sp.PIPE)

        map(lambda x: x.reset_mock(), mocks)

        # Call with command, key
        myshell = mock.MagicMock()
        myshell.communicate.return_value = ["a1", "a2"]
        myshell.returncode = 0  # 0 == SUCCESS
        mock_sp.Popen.return_value = myshell

        result = Midas.odbcommand("command", "key")
        expected = "a1"
        command = Midas._odb + " -c " + "\"" + "command" + " " +\
            "\'" + "key" + "\'" + "\""

        self.assertEqual(result, expected)
        mock_sp.Popen.assert_called_once_with(command,
                                              shell=True,
                                              stdout=mock_sp.PIPE)

        map(lambda x: x.reset_mock(), mocks)

        # Call with command, key, value
        myshell = mock.MagicMock()
        myshell.communicate.return_value = ["a1", "a2"]
        myshell.returncode = 0  # 0 == SUCCESS
        mock_sp.Popen.return_value = myshell

        result = Midas.odbcommand("command", "key", 1.0)
        expected = "a1"
        command = Midas._odb + " -c " + "\"" + "command" + " " +\
            "\'" + "key" + "\'" + " " + "\'" + str(1.0) + "\'" + "\""

        self.assertEqual(result, expected)
        mock_sp.Popen.assert_called_once_with(command,
                                              shell=True,
                                              stdout=mock_sp.PIPE)

        map(lambda x: x.reset_mock(), mocks)

        # Raise FailedCommand exception
        myshell = mock.MagicMock()
        myshell.communicate.return_value = ["a1", "a2"]
        myshell.returncode = 1  # 0 == SUCCESS
        mock_sp.Popen.return_value = myshell

        self.assertRaises(Midas.FailedCommand, Midas.odbcommand, "command")

        map(lambda x: x.reset_mock(), mocks)

        # Raise KeyNotFound exception
        myshell = mock.MagicMock()
        myshell.communicate.return_value = ["key key not found", "a2"]
        myshell.returncode = 0  # 0 == SUCCESS
        mock_sp.Popen.return_value = myshell

        self.assertRaises(Midas.KeyNotFound,
                          Midas.odbcommand,
                          "command",
                          "key")
