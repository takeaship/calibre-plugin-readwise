from calibre.utils.config import JSONConfig
from PyQt5.Qt import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

prefs = JSONConfig('plugins/readwise')
prefs.defaults['access_token'] = ''
prefs.defaults['content_server_url'] = ''

class ConfigWidget(QWidget):
  def __init__(self):
    QWidget.__init__(self)
    self.l = QVBoxLayout()
    self.setLayout(self.l)

    # Access token section
    self.l_at = QHBoxLayout()
    self.l.addLayout(self.l_at)
    self.label_at = QLabel('Access &token:')
    self.l_at.addWidget(self.label_at)
    self.at = QLineEdit(self)
    self.at.setEchoMode(QLineEdit.Password)
    self.at.setText(prefs['access_token'])
    self.l_at.addWidget(self.at)
    self.label_at.setBuddy(self.at)
    self.access_token_link_label = QLabel('<a href="https://readwise.io/access_token">Get access token</a>')
    self.access_token_link_label.setOpenExternalLinks(True)
    self.l_at.addWidget(self.access_token_link_label)
    
    # Content server url section
    self.l_cs = QHBoxLayout()
    self.l.addLayout(self.l_cs)
    self.label_cs = QLabel('Content server URL:')
    self.l_cs.addWidget(self.label_cs)
    self.cs = QLineEdit(self)
    self.cs.setText(prefs['content_server_url'])
    self.l_cs.addWidget(self.cs)
    self.label_cs.setBuddy(self.cs)
    
    
  def save_settings(self):
    prefs['access_token'] = self.at.text()
    prefs['content_server_url'] = self.cs.text()
