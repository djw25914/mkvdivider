#!/usr/bin/python3
# (c) 2011-2014 Dustin Widmann
# GPL v3
## Small python3 kde4 program to split MKV files based on chapter information.
# Version 0.3.0

try:
    import os, getopt, sys, subprocess, tempfile
    from subprocess import CalledProcessError, call
except ImportError:
    print('MKV Splitter requires the following standard modules to be present in order to function: os, getopt, sys, subprocess\nIf your version of python2 doesn\'t include these, try upgrading to a more recent version of python')
    sys.exit(2)
    
default_close_on_exit = True
default_output_directory = os.environ['HOME']

try:
    from PyKDE4.kdecore import *
    from PyKDE4.kdeui import *
    from PyKDE4.kio import KDirSelectDialog
    from PyKDE4 import kdecore, kdeui
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4 import QtCore, QtGui
except ImportError:
    print("MKV Splitter requires PyQt4 and PyKDE4 in order to work, please make sure these are installed and try to run MKV Splitter again.")
    sys.exit(2)
    
try:
    from mydirrequester import *
    from timetools import *
    from qtruncommand import *
except ImportError:
    print("Your MKV Splitter installation is incomplete. Check that mydirrequester.py, timetools.py, and qtruncommandmkvsplitter.py are present.")
    sys.exit(2)
    
    
    
class Chapter():
    start_time = 0
    length = 0
    chapter_name = ''
    
class Splitter(QWidget):
    def handle_args(self):
        """ Handle the cli args here """
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help","input-file="])

        except getopt.GetoptError:
            self.usage()
            sys.exit(2)
        if len(opts) < 1:
            self.usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.usage()
                sys.exit()
            elif opt in ("-i",  "--input-file"):
                self.input_file = arg
            else:
                self.usage()
                sys.exit(2)
    def usage(self):
        print("mkv-splitter - splits mkv files by chapter names. PyQt4 GUI.\n-i --input-file=file - the input file. **REQUIRED until I get a couple of things done.\n-h --help - print this message.")
    
    def __init__(self):
        QWidget.__init__(self, parent=None)
        self.handle_args()

        self.title_name = ''
        self.window = KMainWindow()
        self.window.setMinimumSize(490, 530)
        self.window.setCentralWidget(self) 
        self.main_layout = QVBoxLayout()
        
        self.form_retainer = QWidget()
        self.form_layout = QFormLayout(self.form_retainer)
        self.output_directory_edit = MyDirRequester(self)
        self.output_directory_edit.setText(default_output_directory)
        self.form_layout.addRow("Output Directory: ", self.output_directory_edit)
        
        self.output_file_basename_edit = QLineEdit(self)
        self.output_file_basename_edit.setText(os.path.basename(self.input_file).rsplit('.')[0])
        self.form_layout.addRow("Output Basename: ",  self.output_file_basename_edit)
        
        self.main_layout.addWidget(self.form_retainer)
        
        self.chapters_table = QTableWidget()
        self.chapters_table.setColumnCount(4)
        self.chapters_table.setShowGrid(False)
        self.chapters_table.setAlternatingRowColors(True)
        self.chapters_table.horizontalHeader().setVisible(True)
        self.chapters_table.verticalHeader().setVisible(True)
        self.chapters_table.setHorizontalHeaderItem(0, QTableWidgetItem('Split'))
        self.chapters_table.setHorizontalHeaderItem(1, QTableWidgetItem('Start Time'))
        self.chapters_table.setHorizontalHeaderItem(2, QTableWidgetItem('Length'))
        self.chapters_table.setHorizontalHeaderItem(3, QTableWidgetItem('Chapter Name'))
        
        # Column Numbers for the TableWidget
        self.SPLIT = 0
        self.START_TIME = 1
        self.LENGTH = 2
        self.NAME = 3
        
        self.chapters_table.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.chapters_backup_fd, self.chapters_backup_path = tempfile.mkstemp()
        
        self.chapters = self.read_chapters()
        self.populate_chapters()
        
        self.split_button = QPushButton()
        self.split_button.setText('Split')
        self.split_button.clicked.connect(self.perform_split)
        
        self.preview_button = QPushButton()
        self.preview_button.setText('Preview Chapter')
        self.preview_button.clicked.connect(self.preview_chapter)
        
        self.chapters_button_box_container = QWidget()
        self.chapters_button_box = QHBoxLayout(self.chapters_button_box_container)
        self.chapters_button_box.addWidget(self.preview_button)
        self.chapters_button_box.addWidget(self.split_button)
        
        self.main_layout.addWidget(self.chapters_table)
        self.main_layout.addWidget(self.chapters_button_box_container)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        
        self.main_layout.addWidget(self.progress_bar)
        self.setLayout(self.main_layout)
        self.window.show()

    def main(self):
        pass
    
    def populate_chapters(self):
        current = self.chapters_table.rowCount()
        for chapter in self.chapters:
            self.chapters_table.insertRow(current)
            self.chapters_table.setCellWidget(current, self.SPLIT, QCheckBox())
            self.chapters_table.setItem(current, self.START_TIME, QTableWidgetItem(str(self.chapters[chapter]['start_time'])))
            self.chapters_table.setItem(current, self.LENGTH, QTableWidgetItem(str(self.chapters[chapter]['length'])))
            self.chapters_table.setItem(current, self.NAME, QTableWidgetItem(str(self.chapters[chapter]['chapter_name'])))
            self.chapters_table.resizeColumnsToContents()
            current = current + 1
        
    def read_chapters(self):
        lines = ''
        try:
            results = run_command_output('mkvextract chapters -s {0}'.format(self.input_file))
            lines = results['output']
        except:
            print("Command mkvextract exited with a non-zero exit status of %d." % status)
            return
        finally:
            with open(self.chapters_backup_path,'wb') as chapters_backup_file:
                chapters_backup_file.write(lines.encode('utf-8'))
            lines = lines.split('\n')
            lines2 = []
            chapters = {}
            for line in lines:
                line = line.strip()
                if len(line) > 1:
                    lines2.append(line.strip())
            chapter_number = 1
            time_line = True
            for line in lines2:
                right = line.split('=')[1]
                if time_line == True:
                    chapters[chapter_number] = dict()
                    chapters[chapter_number]['start_time'] = right
                    time_line = False
                else:
                    chapters[chapter_number]['chapter_name'] = right
                    
                    time_line = True
                    chapter_number = chapter_number + 1

            for x in range(len(chapters)):
                if not x+1 == len(chapters): #Gets length of chapters
                    chapters[x+1]['length'] = time_subtraction(chapters[x+1]['start_time'], chapters[x+2]['start_time'])
                else: #Gets length of final chapter
                    results = run_command_output("mkvinfo %s | grep Duration | cut -d '(' -f 2 | cut -d ')' -f 1" % self.input_file)
                    end_time = results['output']
                    chapters[x+1]['length'] = time_subtraction(chapters[x+1]['start_time'], end_time)
            return chapters
        
    def write_chapters(self):
        fd, chapters_path = tempfile.mkstemp()
        with open(chapters_path,'wb') as chapter_file:
            chapter_counter = 1
            for chapter in range(0,self.chapters_table.rowCount()):
                line1 = "CHAPTER{0:0>2}={1}\n".format(chapter,self.chapters_table.item(chapter,self.START_TIME).text()).encode('utf-8')
                line2 = "CHAPTER{0}NAME={1}\n".format(chapter,self.chapters_table.item(chapter,self.NAME).text()).encode('utf-8')
                chapter_file.write(line1)
                chapter_file.write(line2)
        os.close(fd)
            
        command1="mkvpropedit {0} -c ''".format(self.input_file)
        command2="mkvpropedit {0} -c {1}".format(self.input_file,chapters_path)
        try:
            results = run_command_basic(command1)
            if results['ecode'] >0:
                raise Exception("The following command failed with error code {0}.\n {1} \n It provided the following error message: \n {2} \n\n".format(
                    results['ecode'],command1, format(results['output'])))
            
            results = run_command_basic(command2)
            if results['ecode'] >0:
                raise Exception("The following command failed with error code {0}.\n {1} \n It provided the following error message: \n {2} \n\n".format(
                    results['ecode'],command1, format(results['output'])))
        except Exception as e:
            os.remove(chapters_path)
            print("Failed to edit the chapters on the original file. See the following:\n\n{0}".format(e.args),file=sys.stderr)
            #If there's a mess we should try to fix it
            self.restore_chapters()
            sys.exit(2)
            
        chapter_file.close()
        
    def restore_chapters(self):
        command = "mkvpropedit {0} -c {1}".format(self.input_file,self.chapters_backup_path)
        try:
            results = run_command_basic(command)
            if results['ecode'] > 0:
                raise Exception("The following command failed with error code {0}.\n {1} \n It provided the following error message: \n {2} \n\n".format(
                    results['ecode'],command1, format(results['output'])))
        except:
            print("Failed to restore the chapters on the original file. See the following:\n\n{0}".format(e.args),file=sys.stderr)
            
        
    def preview_chapter(self):
        current_row = self.chapters_table.currentRow()
        run_command("mplayer -chapter %s-%s %s" % (current_row+1,  current_row+1,  self.input_file))
    
    def update_progress(self, progress):
        self.progress_bar.setValue(int(progress))
        if int(progress) == 100:
            if restore_original_chapters:
                self.restore_chapters()
            if not default_close_on_exit:
                self.progress_bar.setVisible(True)
                self.form_layout.setEnabled(True)
                self.preview_button.setEnabled(True)
                self.split_button.setEnabled(True)
                self.output_file_basename_edit.setEnabled(True)
                self.output_directory_edit.setEnabled(True)
                self.chapters_table.setEnabled(True)
                self.setCursor(Qt.ArrowCursor)
            else:
                sys.exit(0)
                
    def parse_progress(self, current_line):
        if 'Progress: ' in current_line:
            try:
                b = current_line.rsplit('Progress: ')[1]
            except: 
                raise
            b = b.rstrip()
            b = b.rstrip('%')
            self.emit(SIGNAL("update_progress(QString)"), b)
            current_line = ''
            
    def perform_split(self):
        self.write_chapters()
        counter = 0
        split_points = []
        for row in range(self.chapters_table.rowCount()):
            if self.chapters_table.cellWidget(row, self.SPLIT).isChecked():
                counter = counter + 1
                split_points.append(str(self.chapters_table.item(row, self.START_TIME).text()))
        if counter > 1: #There is something to split
            self.progress_bar.setVisible(True)
            self.form_layout.setEnabled(False)
            self.preview_button.setEnabled(False)
            self.split_button.setEnabled(False)
            self.output_file_basename_edit.setEnabled(False)
            self.output_directory_edit.setEnabled(False)
            self.chapters_table.setEnabled(False)
            self.setCursor(Qt.WaitCursor)
            
            split_points = ','.join(split_points)
            outdir = self.output_directory_edit.url()
            basename = self.output_file_basename_edit.text()
            
            
            command = 'mkvmerge -o "%s/%s.mkv" --split "timecodes:%s" "%s" 2>&1' % (outdir,  basename,  split_points,  self.input_file)
            run_command_progress(command, self.parse_progress, self.update_progress)
        else: #Assume we just want to revise chapters
            self.write_chapters()
            sys.exit(0)
            
                    
app_name = "mkv-splitter"
catalog = ""
program_name = ki18n("mkv-splitter")
version = "0.3.0"
description = ki18n("Splits MKV files by chapter information")
license = KAboutData.License_GPL
copyright = ki18n("(c) 2011-2014 Dustin Widmann")
text = ki18n("none")
home_page = ""
bug_email = "1m.0n.f1r3@gmail.com"

aboutData = KAboutData(app_name, catalog, program_name, version, description, license, copyright, text, home_page, bug_email)

KCmdLineArgs.init([sys.argv[0]] , aboutData)
app=KApplication()
splitter = Splitter()
splitter.show()
sys.exit(app.exec_())
