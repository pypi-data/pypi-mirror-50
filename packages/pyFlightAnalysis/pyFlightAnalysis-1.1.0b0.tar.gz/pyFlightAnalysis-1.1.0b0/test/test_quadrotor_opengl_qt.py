#coding:utf-8
"""
creator: Marx Liu
"""

from __future__ import division
import time
import sys
from collections import OrderedDict
import random
import numpy as np
from pyulog.core import ULog
from PyQt4 import QtCore,QtGui 
import pyqtgraph as pg
from PyQt4.Qt import pyqtSignal

from widgets import QuadrotorWin

import pdb
__version__ = '0.1.0'


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
    
class MainWindow(QtGui.QMainWindow):
    
    deletePressed = pyqtSignal(bool)
    quadrotorStateChanged = pyqtSignal(object)
    motorSpeedChanged = pyqtSignal(object)
    quadrotorStateReseted = pyqtSignal(bool)
    SCALE_FACTOR = 100
    
    def __init__(self):
        """
        Frame of GUI
        =========================
        |_MenuBar_______________|
        |    |                  |
        |plot|     graph1       |
        |list|------------------|
        |----|                  |
        |data|     graph2       |
        |list|                  |
        =========================
        """
        super(MainWindow,self).__init__()
        
        self.log_data = None
        self.log_file_name = None
        self.data_dict = None

        self.main_widget = QtGui.QWidget(self)
        self.mainlayout = QtGui.QHBoxLayout()
        self.main_widget.setLayout(self.mainlayout)
        # ToolBar
        self.toolbar = self.addToolBar('FileManager')
        loadfile_action = QtGui.QAction(QtGui.QIcon('../icons/open.gif'),'Open log file',self)
        loadfile_action.setShortcut('Ctrl+O')
        loadfile_action.triggered.connect(self.callback_open_log_file)
        self.toolbar.addAction(loadfile_action)
        self.log_file_name = None
        self.show_quadrotor_3d = QtGui.QAction(QtGui.QIcon('../icons/quadrotor.gif'),'show 3d viewer',self)
        self.show_quadrotor_3d.setShortcut('Ctrl+Shift+Q')
        self.show_quadrotor_3d.triggered.connect(self.callback_show_quadrotor)
        self.toolbar.addAction(self.show_quadrotor_3d)
         
        # Left plot item widget
        self.plot_data_frame = QtGui.QFrame(self)
        self.plot_data_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.plot_data_layout = QtGui.QVBoxLayout(self.plot_data_frame)
        
        ## Data Plotting
        self.data_plotting = []
        ### There exist a Default graph
        self.line_ID = 0
        lbl_ploting_data = QtGui.QLabel('Data Plotting')
        self.plotting_data_model = QtGui.QStandardItemModel(self)
        self.plotting_data_tableView = TableView(self.plot_data_frame)
        self.plotting_data_tableView.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked | 
                                                     QtGui.QAbstractItemView.SelectedClicked)
        self.plotting_data_tableView.setModel(self.plotting_data_model)
        self.plotting_data_tableView.setSortingEnabled(False)
        self.plotting_data_tableView.horizontalHeader().setStretchLastSection(True)
        self.plotting_data_tableView.resizeColumnsToContents()
        self.plotting_data_tableView.selectionChanged = self.callback_plotting_data_selectionChanged
        self.plotting_data_model.setHorizontalHeaderLabels(['Label'])
        
        lbl_ploting_data.setBuddy(self.plotting_data_tableView)
        self.plot_data_layout.addWidget(lbl_ploting_data)
        self.plot_data_layout.addWidget(self.plotting_data_tableView)
        
        edit_layout = QtGui.QHBoxLayout()
        self.delete_btn = QtGui.QPushButton('Delete')
        self.delete_btn.clicked.connect(self.callback_del_plotting_data)
        self.clear_btn = QtGui.QPushButton('Clear')
        self.clear_btn.clicked.connect(self.callback_clear_plotting_data)
        self.clear_btn = QtGui.QPushButton('Hide')
        self.clear_btn.clicked.connect(self.callback_hide_plotting_data)
        edit_layout.addWidget(self.delete_btn)
        edit_layout.addWidget(self.clear_btn)
        self.plot_data_layout.addLayout(edit_layout)
        
        ## Data in the log file
        self.list_data_frame = QtGui.QFrame(self)
        self.list_data_frame.setMinimumWidth(300)
        self.list_data_frame.setMaximumWidth(600)
        self.list_data_frame.resize(200,500)
        self.list_data_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.list_data_layout = QtGui.QVBoxLayout(self.list_data_frame)
        ### line to search item
        self.choose_item_lineEdit = QtGui.QLineEdit(self.list_data_frame)
        self.choose_item_lineEdit.setPlaceholderText('filter by data name')
        self.choose_item_lineEdit.textChanged.connect(self.callback_filter)
        ### tree to show data to plot
        self.item_list_treeWidget = QtGui.QTreeWidget(self.list_data_frame)
        self.item_list_treeWidget.clear()
        self.item_list_treeWidget.setColumnCount(3)
        self.item_list_treeWidget.setHeaderLabels(['Flight Data','Type','Length'])
        self.item_list_treeWidget.itemDoubleClicked.connect(self.callback_tree_double_clicked)
        self.item_list_treeWidget.resizeColumnToContents(2)
        self.list_data_layout.addWidget(self.choose_item_lineEdit)
        self.list_data_layout.addWidget(self.item_list_treeWidget)
        
        # Right plot item
        self.graph_frame = QtGui.QFrame(self)
        self.graph_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.animation_layout = QtGui.QVBoxLayout(self.graph_frame)
        
        ## quadrotor 3d
        self.quadrotor_win = QuadrotorWin(self)
        self.quadrotor_win.closed.connect(self.quadrotor_win_closed_event)
        self.quadrotor_win.hide()
        self.first_load = True
        self.quadrotor_widget_isshow = False
        
        ## default plot
        self.default_graph_widget = pg.GraphicsLayoutWidget()
        ### a hidable ROI region
        self.detail_graph = self.default_graph_widget.addPlot(row=0,col=0)
        self.detail_graph.setAutoVisible(True)
        self.detail_graph.hide()
        ### main graph to plot curves
        self.main_graph = self.default_graph_widget.addPlot(row=1,col=0)
        self.main_graph.keyPressEvent = self.keyPressed
        self.deletePressed.connect(self.callback_del_plotting_data)
        self.main_graph.scene().sigMouseClicked.connect(self.callback_graph_clicked)
        self.main_graph.addLegend()
        ROI_action = QtGui.QAction('show/hide ROI graph',self.main_graph)
        ROI_action.triggered.connect(self.callback_ROI_triggered)
        self.main_graph.scene().contextMenu.append(ROI_action)
        self.ROI_region = pg.LinearRegionItem()
        self.ROI_region.setZValue(10)
        self.ROI_region.hide()
        self.ROI_showed = False
        
        def update():
            self.ROI_region.setZValue(10)
            minX, maxX = self.ROI_region.getRegion()
            self.detail_graph.setXRange(minX, maxX, padding=0)    
    
        self.ROI_region.sigRegionChanged.connect(update)
        
        def updateRegion(window, viewRange):
            rgn = viewRange[0]
            self.ROI_region.setRegion(rgn)
        self.detail_graph.sigRangeChanged.connect(updateRegion)
        
        self.main_graph.addItem(self.ROI_region,ignoreBounds=True)
        
        ## vertical line
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.vLine.hide()
        self.main_graph.addItem(self.vLine,ignoreBounds=True)
        self.vLine_detail = pg.InfiniteLine(angle=90, movable=False)
        self.vLine_detail.hide()
        self.detail_graph.addItem(self.vLine_detail,ignoreBounds=True)
        
        ## flag whether there is a curve clicked after last clicked event
        self.curve_clicked = False
        self.curve_highlighted = []
        self.animation_layout.addWidget(self.default_graph_widget)
        ## time line
        self.time_line_frame = QtGui.QFrame(self)
        self.time_line_frame.setMaximumHeight(45)
        self.time_line_frame.setMinimumHeight(45)
        self.time_line_layout = QtGui.QHBoxLayout(self.time_line_frame)
        time_line_lbl = QtGui.QLabel('x')
        time_line_lbl.setToolTip('set play speed')
        speed_combo = QtGui.QComboBox()
        speed_combo.addItems(['1','2','4','8'])
        self.speed_factor = 500
        self.time_line_layout.addWidget(time_line_lbl)
        self.time_line_layout.addWidget(speed_combo)
        speed_combo.currentIndexChanged.connect(self.callback_speed_combo_indexChanged)
        self.current_factor = 500/1
        self.time_line_button_play = QtGui.QPushButton(self.time_line_frame)
        self.time_line_button_play.setEnabled(False)
        self.time_line_button_play.setIcon(QtGui.QIcon("../icons/play.jpg"))
        self.time_line_play = False
        self.time_line_button_play.clicked.connect(self.callback_play_clicked)
        self.time_line_button_stop = QtGui.QPushButton(self.time_line_frame)
        self.time_line_button_stop.setEnabled(False)
        self.time_line_button_stop.setIcon(QtGui.QIcon("../icons/stop.jpg"))
        self.time_line_button_stop.clicked.connect(self.callback_stop_clicked)
        self.time_line_layout.addWidget(self.time_line_button_play)
        self.time_line_layout.addWidget(self.time_line_button_stop)
        self.time_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.time_slider.setRange(0,100)
        #### index for time_stamp
        self.time_line_layout.addWidget(self.time_slider)
        ## timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.animation_update)
        self.current_time = 0
        self.dt = 50
        
        self.splitter1 = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter1.addWidget(self.plot_data_frame)
        self.splitter1.addWidget(self.list_data_frame)
        
        self.splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter2.addWidget(self.graph_frame)
        self.splitter2.addWidget(self.time_line_frame)
        
        self.splitter3 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter3.addWidget(self.splitter1)
        self.splitter3.addWidget(self.splitter2)
        
        self.mainlayout.addWidget(self.splitter3)
        
        self.setCentralWidget(self.main_widget)
        self.setGeometry(200,200,800,800)
        self.setWindowTitle("pyFlightAnalysis")
        
        self.quadrotorStateChanged.connect(self.quadrotor_win.callback_update_quadrotor_pos)
        self.quadrotorStateReseted.connect(self.quadrotor_win.callback_quadrotor_state_reset)
    
    def keyPressed(self,event):
        """Key Pressed function for graph"""
        if event.key() == QtCore.Qt.Key_Delete:
            self.deletePressed.emit(True)
        elif event.key() == QtCore.Qt.Key_R:
            # ROI graph can also be triggered by press 'r'
            self.callback_ROI_triggered()
    
    @staticmethod
    def getIndex(data,item):
        for ind,d in enumerate(data):
            if d > item:
                return ind
            
        return len(data) - 1
             
    @staticmethod
    # ref:https://github.com/PX4/Firmware/blob/master/src/lib/mathlib/math/Quaternion.hpp
    def quat_to_euler(q0,q1,q2,q3):
        #321
        angles = []
        for i in range(len(q0)):
            yaw = np.arctan2(2.0 * (q0[i] * q1[i] + q2[i] * q3[i]), 1.0 - 2.0 * (q1[i]**2 + q2[i]**2))
            roll = np.arcsin(2.0 * (q0[i] * q2[i] - q3[i] * q1[i]))
            pitch = np.arctan2(2.0 * (q0[i] * q3[i] + q1[i] * q2[i]), 1.0 - 2.0 * (q2[i]**2 + q3[i]**2))
            angles.append([yaw,roll,pitch])
        return angles
        
    def callback_open_log_file(self):
        print('In open log')
        from os.path import expanduser
        home_path = expanduser('~')
        filename = QtGui.QFileDialog.getOpenFileName(self,'Open Log File',home_path,'Log Files (*.ulg)')
        
        if filename:
            try:
                self.log_file_name = filename
                self.load_data()
                self.load_data_tree()
                self.time_line_button_play.setEnabled(True)
            except Exception as ex:
                print(ex)
    
    def callback_play_clicked(self):
        """Time line play"""
        self.time_line_play = not self.time_line_play
        if self.log_file_name is not None:
            if self.time_line_play:
                self.time_line_button_play.setIcon(QtGui.QIcon("../icons/pause.jpg"))
                self.time_line_button_stop.setEnabled(True)
                if self.ROI_showed:
                    region = self.ROI_region.getRegion()
                    self.vLine.setPos(region[0])
                    self.vLine_detail.setPos(region[0])
                else:
                    self.vLine.setPos(self.time_range[0])
                    self.vLine_detail.setPos(self.time_range[0])
                self.vLine.show()
                self.vLine_detail.show()
                # start timer
                self.timer.start(self.dt)
            else:
                self.time_line_button_play.setIcon(QtGui.QIcon("../icons/play.jpg"))
                self.time_line_button_stop.setEnabled(False)
                self.timer.stop()
    
    def callback_stop_clicked(self):
        self.time_line_play = False
        self.timer.stop()
        self.time_line_button_play.setIcon(QtGui.QIcon("../icons/play.jpg"))
        self.time_line_button_stop.setEnabled(False)
        self.time_slider.setValue(0)
        self.time_index = 0
        self.vLine.hide()
        self.vLine_detail.hide()
        self.quadrotorStateReseted.emit(True)
        
    
    def animation_update(self):
        """update the quadrotor state"""
        dV = 100.0/(self.time_range[1] - self.time_range[0])
        
        if self.ROI_showed:
            start,end = self.ROI_region.getRegion() 
            t = self.current_time + start
            # emit data
            indexes = map(self.getIndex,[self.time_stamp_position,self.time_stamp_attitude,self.time_stamp_output],[t,t,t])
            state_data = [self.position_history[indexes[0]],
                          self.attitude_history[indexes[1]],self.output_history[indexes[2]]]
            self.quadrotorStateChanged.emit(state_data)
            # update slider
            self.time_slider.setValue(int(dV * (self.current_time + start - self.time_range[0])))
            # update vLine pos
            self.vLine.setPos(t)
            self.vLine_detail.setPos(t)
            if self.current_time > (end - start):
                self.current_time = 0
                self.quadrotorStateReseted.emit(True)
        else:
            t = self.current_time + self.time_range[0]
            self.time_slider.setValue(int(dV * self.current_time)) 
            # update quadrotor position and attitude and motor speed
            indexes = map(self.getIndex,[self.time_stamp_position,self.time_stamp_attitude,self.time_stamp_output],[t,t,t])
            print(indexes)
            state_data = [self.position_history[indexes[0]],
                          self.attitude_history[indexes[1]],self.output_history[indexes[2]]]
            self.quadrotorStateChanged.emit(state_data)
            # update vLine pos
            self.vLine.setPos(t)
            self.vLine_detail.setPos(t)
            # if arrive end just replay
            if self.current_time > (self.time_range[1] - self.time_range[0]):
                self.current_time = 0
                self.quadrotorStateReseted.emit(True)
    
        self.current_time += self.dt/self.current_factor
        
        
    def callback_show_quadrotor(self):
        if self.quadrotor_widget_isshow:
            self.show_quadrotor_3d.setIcon(QtGui.QIcon('../icons/quadrotor.gif'))
            self.quadrotor_widget_isshow = not self.quadrotor_widget_isshow
            self.quadrotor_win.hide()
            self.update()
        else:
            self.quadrotor_widget_isshow = not self.quadrotor_widget_isshow
            self.show_quadrotor_3d.setIcon(QtGui.QIcon('../icons/quadrotor_pressed.gif'))
            splash = ThreadQDialog(self.quadrotor_win.quadrotor_widget,self.quadrotor_win)
            splash.run()
            self.quadrotor_win.show()
            self.update()
            
    def callback_speed_combo_indexChanged(self,index):
        self.current_factor = self.speed_factor / 2**index
    
    def callback_filter(self,filtertext):
        """Accept filter and update the tree widget"""
        filtertext = str(filtertext)
        if self.data_dict is not None:
            if filtertext == '':
                self.load_data_tree()
            else:
                self.item_list_treeWidget.clear()
                for key,values_name in self.data_dict.items():
                    values_satisfied = [] 
                    for value in values_name:
                        if filtertext in value[0]:
                            values_satisfied.append(value)
                    if values_satisfied:
                        param_name = QtGui.QTreeWidgetItem(self.item_list_treeWidget,[key])
                        self.item_list_treeWidget.expandItem(param_name)
                        for data_name in values_satisfied:
                            self.item_list_treeWidget.expandItem(
                                QtGui.QTreeWidgetItem(param_name,[data_name[0],data_name[1],data_name[2]]))
                            
    def callback_plotting_data_selectionChanged(self,selected,deselected):
        """ """
        if len(selected.indexes()) > 0:
            for index in selected.indexes():
                print(index.row())
#       print(selection.size())
        
    def callback_graph_clicked(self,event):
        """ set the curve highlighted to be normal """
        print('in graph clicked')
        if self.curve_clicked:
            print('event:',event.modifiers())
            if event.modifiers() == QtCore.Qt.ControlModifier:
                pass
            else:
                print('no control')
                for curve in self.curve_highlighted[:-1]:
                    curve.setShadowPen(pg.mkPen((200,200,200), width=1, cosmetic=True))
                self.curve_highlighted = self.curve_highlighted[-1:]
                
        if len(self.curve_highlighted) > 0 and not self.curve_clicked:
            for curve in self.curve_highlighted:
                curve.setShadowPen(pg.mkPen((120,120,120), width=1, cosmetic=True))
                self.curve_highlighted = []
                self.plotting_data_tableView.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
                self.plotting_data_tableView.selectionModel().setCurrentIndex(self.plotting_data_model.index(1,0),
                                                                              QtGui.QItemSelectionModel.Clear)
                self.plotting_data_tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
                
        self.curve_clicked = False
        
    def callback_tree_double_clicked(self,item,col):
        """Add clicked item to Data plotting area"""
        
        def expand_name(item):
            if item.parent() is None:
                return str(item.text(0))
            else:
                return expand_name(item.parent()) + '->' + str(item.text(0))
        # When click high top label, no action will happened
        if item.parent() is None:
            return    
        item_label = expand_name(item)
        row = len(self.data_plotting)
        self.plotting_data_model.insertRow(row)
        
        # Label
        self.plotting_data_model.setData(self.plotting_data_model.index(row, 0),item_label)
        
        # Curve Color
        ## rgb + a
        color = [random.randint(0,255) for _ in range(3)] 
        
        # Curve Visible
        data_index = self.data_dict.keys().index(item_label.split('->')[0])
        data_name = item_label.split('->')[-1]
        ## ms to s
        t = self.log_data[data_index].data['timestamp']/10**6
        data = self.log_data[data_index].data[data_name]
        curve = self.main_graph.plot(t,data,pen=color,clickable=True,name=item_label)
        curve.sigClicked.connect(self.callback_curve_clicked)
        curve.curve.setClickable(True)
        ## items persistent 
        #self.plotting_data_tableView.openPersistentEditor(self.plotting_data_model.index(row,1))
        #self.plotting_data_tableView.openPersistentEditor(self.plotting_data_model.index(row,2))
        showed = True
        self.data_plotting.append([item_label,color,curve,showed,(t,data)])
        self.update_ROI_graph()
        print('end double click')
    
    
    def callback_curve_clicked(self,curve):
        """"""
        self.curve_clicked = True
        curves = [data[2] for data in self.data_plotting]
        ind = curves.index(curve)
        curve.setShadowPen(pg.mkPen((70,70,70), width=5, cosmetic=True))
        self.curve_highlighted.append(curve)
        self.plotting_data_tableView.setCurrentIndex(self.plotting_data_model.index(ind,0))
        print('curve clicked')
        
    def callback_del_plotting_data(self):
        """"""
        indexes = self.plotting_data_tableView.selectedIndexes()
        print('in plotting_data')
        rows_del = set([ind.row() for ind in indexes])
        rows_all = set(range(len(self.data_plotting)))
        rows_reserved = list(rows_all - rows_del) 
        data_plotting = []
        for row in rows_reserved:
            data_plotting.append(self.data_plotting[row])
        self.data_plotting = data_plotting
#         pdb.set_trace()
        self.update_graph()
    
    def callback_visible_changed(self,row,state):
        """"""
        print('visible changed')
        self.data_plotting[row][3] = state
        self.update_graph()
    
    def update_graph(self):
        self.plotting_data_model.removeRows(0,self.plotting_data_model.rowCount())
        for ind,item in enumerate(self.data_plotting):
            self.plotting_data_model.insertRow(ind)
            self.plotting_data_model.setData(self.plotting_data_model.index(ind,0),item[0])
            self.plotting_data_model.setData(self.plotting_data_model.index(ind,1),item[1])
            self.plotting_data_model.setData(self.plotting_data_model.index(ind,2),item[3])
        # remove curves in graph
        for item in self.main_graph.items:
            if isinstance(item,pg.PlotDataItem):
                self.main_graph.removeItem(item)
        self.main_graph.legend.scene().removeItem(self.main_graph.legend)
        self.main_graph.addLegend()
        # redraw curves
        for ind,item in enumerate(self.data_plotting):
            label,color,_,showed,data = item
            if showed:
                curve = self.main_graph.plot(data[0],data[1],pen=color,name=label)
                self.data_plotting[ind][2] = curve 
        self.update_ROI_graph()
        
    def callback_clear_plotting_data(self):
        """"""
        self.plotting_data_model.removeRows(0, self.plotting_data_model.rowCount())
        self.data_plotting = []
        self.main_graph.legend.scene().removeItem(self.main_graph.legend)
        self.main_graph.addLegend()
        self.update_ROI_graph()
    
    def callback_graph_index_combobox_changed(self,index):
        """Add clicked item to Data plotting area"""
        if index == self.graph_number:
            # choose new
            self.graph_number += 1
            # add a graph
            graph_widget = pg.GraphicsLayoutWidget()
            graph_widget.addPlot(row=0,col=0)
            self.graph_lines_dict.setdefault(graph_widget,0)
            for data in self.data_plotting:
                data[1].clear()
                for i in range(1,self.graph_number + 1):
                    data[1].addItem(str(i))
                data[1].addItem('New')
        else:
            # change current curve's graph
            pass
     
    def callback_visible_checkBox(self,checked):
        """Set the curve visible or invisible"""
        if checked:
            pass
        else:
            pass
    
    def callback_ROI_triggered(self):
        """Show the graph"""
        if self.ROI_showed:
            self.detail_graph.hide()
            self.ROI_region.hide()
            self.ROI_showed = not self.ROI_showed
        else:
            self.update_ROI_graph()
            self.detail_graph.show()
            self.ROI_region.show()
            self.ROI_showed = not self.ROI_showed
    
    def update_ROI_graph(self):
        for item in self.detail_graph.items:
            if isinstance(item,pg.PlotDataItem):
                self.detail_graph.removeItem(item)
        items = self.main_graph.items
        for item in items:
            if isinstance(item,pg.PlotDataItem):
                self.detail_graph.plot(item.xData,item.yData,pen=item.opts['pen'])
                    
    def callback_plotting_data_table_cell_clicked(self,row,column):
        print('row:%s,column:%s'%(row,column))
        
    def callback_plotting_data_table_item_clicked(self,item):
        print('clicked item:',item)
    
    def callback_plotting_data_table_entered(self,row,column):
        print('Entered row:%s,column:%s'%(row,column))
        
    
    def load_data(self):
        self.log_data = ULog(self.log_file_name).data_list
        self.data_dict = OrderedDict()
        for d in self.log_data:
            data_items_list = [f.field_name for f in d.field_data]
            data_items_list.remove('timestamp')
            data_items_list.insert(0,'timestamp')
            data_items = [(item,str(d.data[item].dtype),str(len(d.data[item]))) for item in data_items_list]
            self.data_dict.setdefault(d.name,data_items[1:])    
        
        # attitude
        index = self.data_dict.keys().index('vehicle_attitude')
        self.time_stamp_attitude = self.log_data[index].data['timestamp']/10**6
        q0 = self.log_data[index].data['q[0]']
        q1 = self.log_data[index].data['q[1]']
        q2 = self.log_data[index].data['q[2]']
        q3 = self.log_data[index].data['q[3]']
        self.attitude_history = self.quat_to_euler(q0,q1,q2,q3)
        # position
        index = self.data_dict.keys().index('vehicle_local_position')
        self.time_stamp_position = self.log_data[index].data['timestamp']/10**6
        x = self.log_data[index].data['x']
        y = self.log_data[index].data['y']
        z = self.log_data[index].data['z']
        self.position_history = [(x[i]*self.SCALE_FACTOR,y[i]*self.SCALE_FACTOR,
                                  z[i]*self.SCALE_FACTOR) for i in range(len(x))]
        # motor rotation
        index = self.data_dict.keys().index('actuator_outputs')
        self.time_stamp_output = self.log_data[index].data['timestamp']/10**6
        output0 = self.log_data[index].data['output[0]']
        output1 = self.log_data[index].data['output[1]']
        output2 = self.log_data[index].data['output[2]']
        output3 = self.log_data[index].data['output[3]']
        self.output_history = [(output0[i],output1[i],output2[i],output3[i]) for i in range(len(output0))]
        
        # get common time range
        self.time_range = max([self.time_stamp_attitude[0],self.time_stamp_output[0],self.time_stamp_position[0]]),\
                            min([self.time_stamp_attitude[-1],self.time_stamp_output[-1],self.time_stamp_position[-1]])
        
    def load_data_tree(self):
        # update the tree list table
        self.item_list_treeWidget.clear()
        for key,values in self.data_dict.items():
            param_name = QtGui.QTreeWidgetItem(self.item_list_treeWidget,[key])
            self.item_list_treeWidget.expandItem(param_name)
            for data_name in values:
                self.item_list_treeWidget.expandItem(
                    QtGui.QTreeWidgetItem(param_name,[data_name[0],data_name[1],data_name[2]]))
            param_name.setExpanded(False)
        
    def quadrotor_win_closed_event(self,closed):
        if closed:
            self.quadrotor_widget_isshow = not self.quadrotor_widget_isshow
            self.show_quadrotor_3d.setIcon(QtGui.QIcon('../icons/quadrotor.gif'))

class ThreadQDialog(QtCore.QThread):
    def __init__(self,loading_widget,parent=None,*args,**kwargs):
        super(ThreadQDialog,self).__init__(parent,*args,**kwargs)
        self.dialog = QtGui.QMessageBox()
        self.dialog.setWindowTitle('Info:Loading')
        self.dialog.setModal(True)
        self.dialog.hide()
        self.loading_widget = loading_widget
        self.connect(self.loading_widget,QtCore.SIGNAL('loadFinished(bool)'),self.callback_close)
    
    def run(self):
        self.dialog.setText('Loading...')
        self.dialog.setStyleSheet('QLabel{min-width: 100px;}')
        self.dialog.show()
        
    def callback_close(self,isFinished):
        if isFinished:
            self.dialog.close()
            return
 
class CheckboxDelegate(QtGui.QItemDelegate):
    """ """
    curveShowed = pyqtSignal(object,bool)
    def __init__(self, parent):
        """ """
        QtGui.QItemDelegate.__init__(self, parent)
        
    def createEditor(self,parent, option, index):
        """ """
        checkbox = QtGui.QCheckBox('True',parent)
        self.connect(checkbox,QtCore.SIGNAL('stateChanged(int)'),self,QtCore.SLOT("stateChanged()"))
        return checkbox
    
    def setEditorData(self, editor, index):
        """ """
        editor.blockSignals(True)
        if str(index.data().toString()) == 'True':
            editor.setChecked(True)
        else:
            editor.setChecked(False)
        editor.blockSignals(False)
    
    def setModelData(self, editor, model, index):
        """ """
        if editor.checkState() == QtCore.Qt.Checked:
            model.setData(index, 'True')
            self.curveShowed.emit(index.row(),True)
        elif editor.checkState() == QtCore.Qt.Unchecked:
            model.setData(index, 'False')
            self.curveShowed.emit(index.row(),False)
        
    @QtCore.pyqtSlot()
    def stateChanged(self):
        self.commitData.emit(self.sender())

class ColorDelegate(QtGui.QItemDelegate):
    """ """
    def __init__(self,parent):
        QtGui.QItemDelegate.__init__(parent)
        
    def createEditor(self, parent,option,index):
        button = pg.ColorButton(parent)
        print(button.color(mode='float'))
        button.sigColorChanged.connect(self.colorChanged)
        return button
    
    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        editor.setColor(index.data())
        editor.blockSignals(False)
        
    def setModelData(self,editor,model,index):
        
        print('in set model')
        
        
class LabelDelegate(QtGui.QItemDelegate):
    """ """
    def __init__(self,parent):
        """ """
        self.color = None
        QtGui.QItemDelegate.__init__(self, parent)
        
    def createEditor(self,parent,option,index):
        """ """
        label = Label(' ',parent)
        label.color = str(index.data().toString())
        print('label.color',label.color)
        label.setStyleSheet("color:rgb(" + label.color + ')')
        self.connect(label,QtCore.SIGNAL('colorChanged(bool)'),self.colorChanged)
        return label
        
    def setEditorData(self,editor,index):
        """ """
        editor.blockSignals(True)
        print('in set editor',id(editor))
        color = QtGui.QColorDialog().getColor()
        r = color.red()
        g = color.green()
        b = color.blue()
        color = ','.join(map(str,[r,g,b]))
        editor.setStyleSheet("color:rgb(" + color + ')')
        editor.blockSignals(False)
        
    def setModelData(self,editor,model,index):
        """ """
        print('in set model')
        print(editor.color)
        model.setData(index,editor.color)
        print(model.data(index).toString())
        
    @QtCore.pyqtSlot()
    def colorChanged(self):
        print('in colorChanged:')
        self.commitData.emit(self.sender())


class Label(QtGui.QLabel):
    """ Add Clicked signal to Label
    """
    clicked = pyqtSignal(bool)
    colorChanged = pyqtSignal(bool)
    def __init__(self,*args,**kwargs):
        super(Label,self).__init__(*args,**kwargs)
        self.color = None
        self.clicked.connect(self.changeColor)
        
    def mousePressEvent(self, event):
        print('in label press',id(self))
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit(True)
    
    def changeColor(self):
        print('in change color')
        color = QtGui.QColorDialog().getColor()
        r = color.red()
        g = color.green()
        b = color.blue()
        self.color = ','.join(map(str,[r,g,b]))
        print('color',self.color)
        self.colorChanged.emit(True)

class TableView(QtGui.QTableView):
    """
    A simple table to demonstrate the QComboBox delegate.
    """
    def __init__(self, *args, **kwargs):
        QtGui.QTableView.__init__(self, *args, **kwargs)

        # Set the delegate for column 0 of our table
        self.setItemDelegateForColumn(2, CheckboxDelegate(self))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    sys.exit(app.exec_())
