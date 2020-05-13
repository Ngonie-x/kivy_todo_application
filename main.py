#ToDo Application Using the kivy MD Library
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.properties import StringProperty
import shelve
from kivymd.icon_definitions import md_icons
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
import time
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.picker import MDDatePicker
from datetime import datetime
from kivymd.uix.menu import MDDropdownMenu



class Home(GridLayout):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

class TaskDetailDialog(BoxLayout):
    """OPENS A DIALOG BOX WITH TASK DETAILS"""
    def __init__(self, widget=None, **kwargs):
        super().__init__(**kwargs)
        self.widget=widget
        self.ids.task_detail_text.text = str(self.widget.text)
        self.ids.task_detail_date.text = str(self.widget.secondary_text)
        

    def open_edit_dialog(self):
        self.dialog = MDDialog(
            title='Edit Task',
            type="custom", 
            content_cls=TaskEditDialog(widget=self.widget), 
            size_hint=[.95, .5],
        )
        self.dialog.open()

    def delete_task_dialog(self):
        self.delete_dialog = MDDialog(
            title='Delete Item',
            type="custom", 
            content_cls=ConfirmDelete(widget=self.widget), 
            size_hint=[.95, .5],
        )
        self.delete_dialog.open()

    def close_dialog(self):
        self.dialog.dismiss()



class TaskEditDialog(BoxLayout):
    """OPENS A DIALOG BOX TO EDIT A SELECTED TASK"""

    def __init__(self, widget=None, **kwargs):
        super().__init__(**kwargs)
        self.widget = widget
        self.ids.edit_task_text.text = self.widget.text
        self.ids.edit_date_text.text = self.widget.secondary_text
        self.pk = int(self.widget.pk)
        

    def show_date_picker(self):
        """Opens the date picker, duh"""
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()

    def get_date(self, date):
        """This functions gets the date from the date picker and converts its it a
        more friendly form then changes the date label on the dialog to that"""

        date = date.strftime('%A %d %B %Y')
        self.ids.edit_date_text.text = str(date)
        print(date)

    def save_task_data(self):
        self.widget.text = str(self.ids.edit_task_text.text)
        self.widget.secondary_text = str(self.ids.edit_date_text.text)

        self.save_edit_data_to_file()

        Snackbar(text='Task Saved!').show()  

    def save_edit_data_to_file(self):
        shelf_file = shelve.open('mydata')
        todo = shelf_file['todo']

        print(self.pk)

        for k in todo:
            print(k['pk'])
            if k['pk'] == self.pk:
                k['task'] = str(self.ids.edit_task_text.text)
                k['date'] = str(self.ids.edit_date_text.text)

        shelf_file['todo'] = todo
        
        shelf_file.close()



class DialogContent(BoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))


    def save_task(self, value):
        the_task = Task(value)
        the_task.save_data_to_shelf()
    
    def show_date_picker(self):
        """Opens the date picker, duh"""
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()

    def get_date(self, date):
        """This functions gets the date from the date picker and converts its it a
        more friendly form then changes the date label on the dialog to that"""

        date = date.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)
        print(date)

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    """Custom list item"""
    icon = StringProperty('bullseye')

    def __init__(self,check = False, pk=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.check.active = check
        self.pk = pk


        

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container'''

class ConfirmDelete(BoxLayout):
    """"""
    def __init__(self, widget=None, **kwargs):
        super().__init__(**kwargs)
        self.widget = widget

    def delete_the_task(self):
        self.widget.parent.remove_widget(self.widget)
        self.delete_data_in_file()

        Snackbar(text= 'Task Deleted!').show()

    def delete_data_in_file(self):
        shelf_file = shelve.open('mydata')
        todo = shelf_file['todo']

        for k in todo:
            if k['pk'] == self.widget.pk:
                todo[todo.index(k)] = 'deleted'

        shelf_file['todo'] = todo
        shelf_file.close()

            



"""TASK LOGIC"""
class Task:

    """This class is responsible for creating a task"""

    def __init__(self, task=None, date=None, completed=False, pk=1):
        self.task = str(task)
        self.completed = completed
        self.date = date
        self.pk = pk

    
    def save_data_to_shelf(self):
        """By saving data to a shelve file, a task is successfully created, the task are loaded from the
        shelve file"""

        shelf_file = shelve.open('mydata')

        try:

            todo = shelf_file['todo']

            todo.append({'pk':self.pk,'task': self.task, 'completed': self.completed, 'date': self.date})

            print(todo)

            shelf_file['todo'] = todo

            shelf_file.close()
        
        except  KeyError:
            todo = []
            todo.append({'pk':1,'task': self.task, 'completed': self.completed, 'date': self.date})
            
            print(todo)

            shelf_file['todo'] = todo

            shelf_file.close()
    
    def retrive_everything(self):
        try:
            shelf_file = shelve.open('mydata')
            todo = shelf_file['todo']
            print(todo)
            shelf_file.close()
            
            return True
        
        except KeyError:
            print('Nothing in the shelf file yet')
            return False




"""END TASK LOGIC"""
        

class MainApp(MDApp):

    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = 'Green'
        # self.theme_cls.theme_style = "Dark" or "Light"
        self.root = root = Home()
        return root


    def on_start(self):
        if Task().retrive_everything() == True:
            shelf_file = shelve.open('mydata')
            todo = shelf_file['todo']

            for k in todo:
                try:

                    if k['completed'] == True:
                        self.root.ids.completed_container.add_widget(
                                ListItemWithCheckbox(text=k['task'], secondary_text="Due: "+k['date'], check=True, pk=k['pk'])
                            )
                    
                    elif k['completed'] == False:
                        self.root.ids.container.add_widget(
                                ListItemWithCheckbox(text=k['task'], secondary_text="Due: "+k['date'], pk=k['pk'])
                            )


                    shelf_file.close()
            
                except TypeError:
                    continue


    def show_task_dialog(self):
        """Shows the task creation dialog"""
        self.dialog = MDDialog(title="Create a new task", 
        type="custom", 
        content_cls=DialogContent(), 
        size_hint=[.95, .8],
        auto_dismiss=False,
        )
        self.dialog.open()
    
    def close_dialog(self):
        """Closes the task creation dialog"""
        self.dialog.dismiss()

    def save_task(self, value, date):
        """Saves tasks by creating a list item and adding it to the container"""

        try:
            #we want to generate a primary key for each widget from the number of items
            #in the shelf file list

            #open shelf file
            shelf_file = shelve.open('mydata')

            print("Getting todo list")

            todo = shelf_file['todo']

            print(todo)

            pk = len(todo)+1

            print(pk)

            shelf_file.close()

            if value and date:
                self.root.ids.container.add_widget(
                            ListItemWithCheckbox(text=value, secondary_text="Due: "+date, pk=pk)
                        )

                Task(value, date, pk=pk).save_data_to_shelf()
                Snackbar(text="Your Task Has Been Saved").show()
            
            else:
                MDDialog(title="Alert",
                    text='Please add a task name!',
                    size_hint=[.9, None]
                ).open()

        except KeyError:
            if value and date:
                self.root.ids.container.add_widget(
                            ListItemWithCheckbox(text=value, secondary_text="Due: "+date, pk=1)
                        )

                Task(value, date).save_data_to_shelf()
                Snackbar(text="Your Task Has Been Saved").show()
            
            else:
                MDDialog(title="Alert",
                    text='Please add a task name!',
                    size_hint=[.9, None]
                ).open()
            
        

    def confirm_delete_task(self, widget):
        self.root.ids.container.remove_widget(widget)

    def mark(self, instance_check, widget):
        """Does something when the task checkbox is marked or unmarked"""
        if instance_check.active == True:
            print(True)
            print(widget.text)
            print(widget.secondary_text)
            self.root.ids.container.remove_widget(widget)
            self.root.ids.completed_container.add_widget(widget)
            Snackbar(text="Task Complete").show()


            #################update the information in the shelve file#########################
            shelf_file = shelve.open('mydata')
            todo = shelf_file['todo']
            for k in todo:
                try:
                    if k['pk'] == widget.pk:
                        k['completed'] = True
                    
                except TypeError:
                    continue
            
            shelf_file['todo'] = todo
            shelf_file.close()

            ####################################################################################



        if instance_check.active == False:
            print(False)
            
            self.root.ids.completed_container.remove_widget(widget)
            self.root.ids.container.add_widget(widget)
            Snackbar(text="Task Unmarked!").show()


            ##############UPDATE DATA IN THE SHELVE FILE###################

            shelf_file = shelve.open('mydata')
            todo = shelf_file['todo']
            for k in todo:
                try:
                    if k['pk'] == widget.pk:
                        k['completed'] = False
                except TypeError:
                    continue
            
            shelf_file['todo'] = todo
            shelf_file.close()

            ################################################################




    def show_detail(self, widget):
        """Shows the details of a selected task"""
        self.detail_dialog = MDDialog(
            title="Task Detail", 
            type="custom", 
            content_cls=TaskDetailDialog(widget=widget),
            size_hint=[.8, .8],
            auto_dismiss=True,
        )

        self.detail_dialog.open()

    def close_detail_dialog(self):
        """Closes the task detail dialog"""
        self.detail_dialog.dismiss()

        





MainApp().run()