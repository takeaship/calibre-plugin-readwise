from calibre.gui2.actions import InterfaceAction
from calibre_plugins.readwise.main import ReadwiseDialog
from qt.core import QMenu 

class InterfacePlugin(InterfaceAction):
  name = 'Readwise'
  action_spec = ('Readwise', None, 'Export highlights to Readwise', None)

  def genesis(self):
    icon = get_icons('images/icon.png')
    self.qaction.setIcon(icon)
    self.qaction.triggered.connect(self.show_dialog)
    self.menu = QMenu(self.gui)
    self.qaction.setMenu(self.menu)


  def initialization_complete(self):
      print(self.menu.__dict__)
      self.create_menu_action(
        self.menu, "send_to_reader", "Send to reader", 
        icon=get_icons('images/upload_book.png'),
        triggered=self.send_to_reader
      )


  def show_dialog(self):
    base_plugin_object = self.interface_action_base_plugin
    do_user_config = base_plugin_object.do_user_config
    d = ReadwiseDialog(self.gui, self.qaction.icon(), do_user_config)
    d.show()

  def apply_settings(self):
    from calibre_plugins.readwise.config import prefs
    prefs


  def send_to_reader(self):
    pass