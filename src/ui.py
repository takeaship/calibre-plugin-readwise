from calibre.gui2 import error_dialog
from calibre.gui2.actions import InterfaceAction
from calibre_plugins.readwise.main import ReadwiseDialog, validate_content_server_url, send_to_reader
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
        triggered=self.send_selected_to_reader
      )


  def show_dialog(self):
    base_plugin_object = self.interface_action_base_plugin
    do_user_config = base_plugin_object.do_user_config
    d = ReadwiseDialog(self.gui, self.qaction.icon(), do_user_config)
    d.show()

  def apply_settings(self):
    from calibre_plugins.readwise.config import prefs
    prefs


  def send_selected_to_reader(self):
    if not validate_content_server_url():
      d = error_dialog(self.gui, _('Cannot send books'), _('No content server URL set'))
      d.exec()
      return
    rows = self.gui.library_view.selectionModel().selectedRows()
    if not rows or len(rows) == 0:
      d = error_dialog(self.gui, _('Cannot send books'), _('No book selected'))
      d.exec()
      return
    if self.gui.content_server is None or not self.gui.content_server.is_running:
      self.gui.start_content_server()
    for row in rows:
      row_id = row.row()
      db = self.gui.library_view.model().db
      mi = db.get_metadata(row_id)
      if mi.identifiers.get('readwise', None):
        self.gui.status_bar.show_message(_(f'\"{mi.title}\" has been already sent.'), 3000)
        continue
      try:
        readwise_id = send_to_reader(mi)
        mi.set_identifier('readwise', readwise_id)
        db.set_metadata(mi.id, mi, commit=True)
        self.gui.status_bar.show_message(_(f'\"{mi.title}\" was sent successfully.'), 3000)
      except Exception as e:
        d = error_dialog(self.gui, _('Cannot send books'), _('Error sending book: %s') % e)
        d.exec()
        return