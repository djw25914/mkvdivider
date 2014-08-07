# (c) 2011-2014 Dustin Widmann
# GPL v3
# My simplified interface to using subprocess to run commands in a seperate thread. For use with PyQt GUIs.
# Probably soon to be replaced by QProcess. 

try:
  from subprocess import CalledProcessError
  import subprocess, os
except: 
  print("Your python installation is missing subprocess and/or os, perhaps your python installation is not up to date, or perhaps TOO up to date?")
  sys.exit(2)

try: 
    from PyQt4.QtCore import *
    from PyQt4 import QtCore
except: 
    print("qt_run_command requires PyQt4.QtCore to be installed to work. Install it and try again :)")
    sys.exit(2)
    
default_log = "{0}/.run_command.log".format(os.environ['HOME'])
default_delimitors = ['\n', '\r', '^M']



class RunCommand(QThread):
    
    def reset(self):
        self.with_terminal_output = False
        self.command = ''
        self.results = {}
        self.terminal_output = ''
        self.delimitors = ''
        self.parse_progress_hook = False
        
    def __init__(self):
        QThread.__init__(self,parent=None)
        self.comand = ''
        self.with_progress = False
        self.with_logging = False
        self.with_terminal_output = False
        self.logging_file = ""
        self.results = {}
        self.results['ecode'] = 0
        self.results['output'] = ''
    
    def run(self):
        """ Entrance point for the thread """
        if self.with_logging == True:
            self.rclog("Now running command: {0}".format(self.command))
            
        if self.with_progress == True and not self.parse_progress_hook == False:
            return self.run_with_progress()
            
        elif self.with_terminal_output == True:
            return self.run_with_output()
            
        else:
            return self.run_basic()
            
    def run_with_progress(self):
        """ Might work for all cases ... lets cross our fingers """
        results = {}
        try:
            print("foo")
            p = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
            Print("bar")
            current_line = ''
            terminal_output = ""
            while True:
                print ("woot")
                char = p.stdout.read(1)
                if not char: #EOF reached, break out of the loop
                    break
                else: #EOF not yet reached
                    if self.with_terminal_output == True:
                        terminal_output = terminal_output + str(char)
                        print("aaaa")
                    if self.with_progress == True:
                        print("bbbb")
                        if not char in self.delimitors:
                            current_line =  current_line + str(char)
                            print("cccc")
                        else:
                            progress = parse_progress(current_line)
                            print("dddd")
                            if not parse_progress == False:
                                print("eeee")
                                self.emit(SIGNAL("update_progress(QString)"), progress)
                                current_line = ''
        except CalledProcessError as e:
            self.results['ecode'] = e.returncode
                            
    def run_with_output(self):
        """ Basic terminal + save terminal output """
        try:
            output = subprocess.check_output(self.command,shell=True).decode('utf-8').strip()
            self.results['ecode'] = 0 #ideally
            self.results['output'] = output
        except CalledProcessError as e:
            self.results['ecode'] = e.returncode
            self.results['output'] = e.output
        
    def run_basic(self):
        """ Basic running of command. No frills. """
        try:
            subprocess.check_call(self.command, shell=True)
            self.results['ecode'] = 0
            self.results['output'] = ''
        except CalledProcessError as e:
            self.results['ecode'] = e.returncode
            self.results['output'] = e.output
            
    def parse_progress(self,current_line):
        """     You must include a hook to an appropriate parser function. It must:
                Return False for an invalid/irrelevant current_line
                Return a number between 0 and 100 otherwise
        """
        self.parse_progress_hook(current_line)
        return

    def rclog(self,message):
        """Print some info to a log file, and the terminal"""
        print('\n\n\n' + str(message) + '\n\n\n')
        with open (self.logging_file, 'a') as f:
            f.write(str(message + '\n'))
            
def _run_command(command, with_terminal_output, with_logging, logging_file, with_progress, parse_progress_hook, update_progress_hook, delimitors):
    """Runs commands with several optional paramaters"""
    q = QEventLoop()
    run_command_thread = RunCommand()
    run_command_thread.reset()
    run_command_thread.finished.connect(q.quit)
    if with_progress:
        QtCore.QObject.connect(run_command_thread, QtCore.SIGNAL("update_progress(QString)"), update_progress_hook)

    run_command_thread.command = command
    run_command_thread.with_logging = with_logging
    run_command_thread.with_progress=with_progress
    run_command_thread.with_terminal_output = with_terminal_output
    run_command_thread.logging_file = logging_file
    run_command_thread.delimitors = delimitors          # deliminates how strings of output will be broken up (eg: \n, \r), accepts a list
    run_command_thread.start()
    q.exec_()
    results = run_command_thread.results
    return results

def run_command_progress(command, parse_progress_hook, update_progress_hook, delimitors = default_delimitors, with_logging = True, logging_file = default_log):
    return _run_command(command, False, with_logging, logging_file, True, parse_progress_hook, update_progress_hook, delimitors)
    
def run_command_output(command, with_logging = True, logging_file = default_log):
    return _run_command(command, True, with_logging, logging_file, False, False, False, False)
    
def run_command_basic(command, with_logging = True, logging_file = default_log):
    return _run_command(command, False, with_logging, logging_file, False, False, False, False)