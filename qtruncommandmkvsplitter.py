# (c) 2011 Dustin Widmann
# GPL v3
# My simplified interface to using subprocess to run commands in a seperate thread. For use with PyQt GUIs.
# With modification it could be useful elsewhere, but this is "for" mkvsplitter, effectively.
from subprocess import CalledProcessError
import subprocess,  os

try: 
    from PyQt4.QtCore import *
    from PyQt4 import QtCore
except: 
    print("qt_run_command requires PyQt4.QtCore to be installed to work. Install it and try again :)")
    sys.exit(2)
    
class RunCommand(QThread):
    def reset(self):
        self.with_output = False
        self.with_progress = False
        self.command = ''
        self.results = {}
    def check_output(self):
        try:
            output = subprocess.check_output(self.command,shell=True)
            output = output.decode('utf-8')
            output = output.strip()
            self.results['ecode']=0
            self.results['output']=output
        except CalledProcessError as e:
            self.results['ecode'] = e.returncode
            self.results['output'] = e.output
        
    def check_call(self):
        try:
            subprocess.check_call(self.command, shell=True)
            self.results['ecode'] = 0
        except CalledProcessError as e:
            self.results['ecode'] = e.returncode
    
    def run_with_progress(self):
        p = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        current_line = ''
        output = []
        output.insert(0, '')
        while True:
            char = p.stdout.read(1)
            if not char:
                break
            if not char in ['\n', '\r', '^M']:
                current_line =  current_line + str(char)
            else:
                if 'Progress: ' in current_line:
                    try:
                        b = current_line.rsplit('Progress: ')[1]
                    except: 
                        raise
                    b = b.rstrip()
                    b = b.rstrip('%')
                    self.emit(SIGNAL("update_progress(QString)"), b)
                    current_line = ''
                    
        for line in output:
            print(line)
    def run(self):
        if not self.with_progress:
            if self.with_output == True:
                self.check_output()
            else:
                self.check_call()
        else:
            self.run_with_progress()
def run_command(command):
    rclog("Now running command: %s" % command)
    run_command_nolog(command)
        
def run_command_nolog(command):
    q = QEventLoop()
    run_command_thread = RunCommand()
    run_command_thread.reset()
    run_command_thread.finished.connect(q.quit)
    run_command_thread.command = command
    run_command_thread.with_output = True
    run_command_thread.with_progress = False
    run_command_thread.start()
    q.exec_()
    results = run_command_thread.results
    if results['ecode'] != 0:
        raise CalledProcessError(results['ecode'], '')
def run_command_with_output(command):
    rclog("Now running command: %s" % command)
    return run_command_with_output_nolog(command)
         
def run_command_with_output_nolog(command):
    q = QEventLoop()
    run_command_thread = RunCommand()
    run_command_thread.reset()
    run_command_thread.finished.connect(q.quit)
    run_command_thread.command = command
    run_command_thread.with_output = True
    run_command_thread.with_progress = False
    run_command_thread.start()
    q.exec_()
    
    results = run_command_thread.results
    output = subprocess.check_output(command,shell=True)
    output = output.decode('utf-8')
    output = output.strip()
    return output

def run_command_progress(command, progressfunction):
    rclog("Now running command: %s" % command)
    q = QEventLoop()
    run_command_thread = RunCommand()
    QtCore.QObject.connect(run_command_thread, QtCore.SIGNAL("update_progress(QString)"), progressfunction)
    run_command_thread.reset()
    run_command_thread.finished.connect(q.quit)
    run_command_thread.command = command
    run_command_thread.with_output = False
    run_command_thread.with_progress = True
    run_command_thread.start()
    q.exec_()
    
def rclog(message):
    """Print some info to a log file, and the terminal"""
    print('\n\n\n' + str(message) + '\n\n\n')
    with open ('%s/.run_command.log' % (os.environ['HOME']), 'a') as f:
        f.write(str(message + '\n'))
