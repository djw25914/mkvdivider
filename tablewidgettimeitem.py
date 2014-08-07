class tableWidgetTimeItem( QTableWidgetItem):
    def __init__(self,parent=none):
        QTableWidgetItem.__init__(self,parent)
        
    def __lt__(self, other_item):
        column = self.tableWidget.sortColumn()
        
        current = self.text()
        other = other_item.text()
        
        length = time_subtraction(current,other)
        [hours,minutes,seconds] = length.split(':')
        if int(hours) > 0:
            return true
        else:
            return false