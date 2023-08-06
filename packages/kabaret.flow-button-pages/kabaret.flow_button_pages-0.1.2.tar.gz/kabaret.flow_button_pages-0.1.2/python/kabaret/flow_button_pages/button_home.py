from kabaret import flow
from kabaret.app.actors.flow.generic_home_flow import HomeRoot, Home

from kabaret.app.ui.gui.widgets.flow.flow_view import CustomPageWidget, QtWidgets, QtCore, QtGui
from kabaret.app.ui.gui.widgets.flow_layout import FlowLayout
from kabaret.app import resources


class ProjectButton(QtWidgets.QPushButton):

    @classmethod
    def get_default_thumbnail(cls):
        return resources.get(
            'icons.fbp', '{}-{}'.format(
                IconChoice.default(),
                ColorChoice.default(),
            )
        )

    def __init__(self, home_page, name, info, button_height=100, default_thumbnail=None):
        super(ProjectButton, self).__init__(home_page)
        self.home_page = home_page
        self.name = name
        self.info = info

        settings = self.get_settings_object()
        settings = settings.as_dict()
        thumbnail = settings.get('thumbnail')
        color = settings.get('color')

        html = (
            '<center>'
            '<font size=+3><b>'
            '{}'
            '</font></b>'
            '</center>'.format(name)
        )

        status = info['status']
        if status is not None:
            if status == 'Archived':
                status = 'OOP'
            status_pict = resources.get('icons.status', status)
            html += (
                '<hr><center>'
                '<img src="{}"><br>'
                '{}'
                '</center>'.format(
                    status_pict, status,
                )
            )

        if not thumbnail:
            thumbnail = default_thumbnail
        if not thumbnail:
            thumbnail = self.get_default_thumbnail()
        if isinstance(thumbnail, (tuple, list)):
            try:
                thumbnail = resources.get(*thumbnail)
            except (TypeError, resources.NotFoundError, resources.ResourcesError):
                pass

        html = '<center><img src="{}" height={}>{}</center>'.format(
            thumbnail, button_height, html
        )

        if color:
            html = '<font color={}>{}</font>'.format(color, html)

        self.set_html_text(html)

        self.clicked.connect(self.goto_project)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self):
        m = QtWidgets.QMenu(self)
        m.addAction('Configure', self.goto_settings)
        m.exec_(QtGui.QCursor.pos())

    def set_html_text(self, html):
        text = QtGui.QTextDocument()
        text.setHtml(html)
        text.setTextWidth(text.size().width())

        pix = QtGui.QPixmap(text.size().width(), text.size().height())
        pix.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pix)
        text.drawContents(painter, pix.rect())
        painter.end()

        icon = QtGui.QIcon(pix)
        self.setText("")
        self.setIcon(icon)
        self.setIconSize(pix.rect().size())

        margins = QtCore.QSize(10, 10)
        self.setFixedSize(pix.size() + margins)

    def get_settings_object(self):
        return self.home_page.get_home().projects_settings.get_project_settings(self.name)

    def goto_settings(self):
        settings = self.get_settings_object()
        self.home_page.page.goto(settings.oid())

    def goto_project(self):
        self.home_page.page.goto('/' + self.name)


class ButtonHomePage(CustomPageWidget):

    def _get_project_infos(self):
        # This is quite uggly, we should not access actors in
        # the GUI part (it could be on another process...)
        # But I'm kind of fed up following that rule without
        # ever actually encountering a situation where it stands...
        flow_actor = self.session.get_actor('Flow')
        return flow_actor.get_projects_info()

    def get_home(self):
        # This is quite ugly, we should not access actors in
        # the GUI part (it could be on another process...)
        # But I'm kind of fed up following that rule without
        # ever actually encountering a situation where it stands...
        home = self.session.get_actor('Flow').get_object(self.oid)
        return home

    def _build_all(self):
        vlo = self.layout()

        projects_infos = self._get_project_infos()
        if projects_infos:
            layout = FlowLayout()
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            vlo.addLayout(layout)

            home_settings = self.get_home().home_settings
            show_status = home_settings.show_status.get()
            show_archived = home_settings.show_archived.get()
            button_height = home_settings.button_height.get()
            default_thumbnail = home_settings.default_thumbnail.get()
            for name, info in projects_infos:
                if not show_archived and info['status'] == 'Archived':
                    continue
                if not show_status:
                    info['status'] = None  # mmmmmouai.... c'est moche.
                b = ProjectButton(self, name, info, button_height, default_thumbnail)
                layout.addWidget(b)

            vlo.addSpacing(100)
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.on_context_menu)

        else:
            welcome = '''
            <H2>Welcome !</H2>
            It looks like you have no Project yet.<br>
            You can edit the <b>settings</b> to create one:
            '''
            l = QtWidgets.QLabel(welcome, self)
            b = QtWidgets.QPushButton('Edit Settings...')
            b.clicked.connect(self.on_goto_settings)

            vlo.addWidget(l)
            vlo.addWidget(b)

    def _clear_layout(self, lo):
        li = lo.takeAt(0)
        while li:
            w = li.widget()
            if w:
                w.deleteLater()
            clo = li.layout()
            if clo:
                self._clear_layout(clo)
            li = lo.takeAt(0)

    def _clear_all(self):
        vlo = self.layout()
        self._clear_layout(vlo)

    def build(self):
        vlo = QtWidgets.QVBoxLayout()
        self.setLayout(vlo)
        self._build_all()

    def on_context_menu(self):
        m = QtWidgets.QMenu()
        m.addAction('Admin...', self.on_goto_settings)
        m.exec_(QtGui.QCursor.pos())

    def on_goto_settings(self):
        self.get_home().use_custom_page = False
        self.page.goto(None)

    def on_touch_event(self, oid):
        if oid == self.oid:
            self.setEnabled(False)
            try:
                self._clear_all()
                self._build_all()
            finally:
                self.setEnabled(True)

    def die(self):
        pass


class _Choice(flow.values.ChoiceValue):

    @classmethod
    def default(cls):
        return cls.CHOICES[0]


class IconChoice(_Choice):
    CHOICES = ['clap', 'reel', 'screen']


class ColorChoice(_Choice):
    CHOICES = ['blue', 'green', 'orange', 'pink', 'red']


class SelectThumbnailAction(flow.Action):
    _value = flow.Parent()

    icon = flow.Param(IconChoice.default(), IconChoice).watched()
    color = flow.Param(ColorChoice.default(), ColorChoice).watched()

    def get_buttons(self):
        self._revert_thumbnail = self._value.get()
        return ['Close', 'Revert']

    def child_value_changed(self, child_value):
        name = '{}-{}'.format(
            self.icon.get(), self.color.get()
        )
        self._value.set(('icons.fbp', name))

    def run(self, button):
        if button == 'Revert':
            self._value.set(self._revert_value)
            self.root().Home.touch()
        return


class ThumbnailValue(flow.values.Value):
    presets = flow.Child(SelectThumbnailAction)


class ProjectSettings(flow.Object):
    doc = flow.Label(
        '''
        Color:
            Use an html compatible value, like "#0088FF".

        Thumbnail:
            Use a resource identifier like "['icons.gui', 'star']", 
            or a file path (but avoid backslashes !),
            or a data URI for the thumbnail.

        To further more configure the Home, right click an empty space
        close to one of the Projects and select "Admin...".
        '''
    )
    color = flow.Param('').watched()
    thumbnail = flow.Param('', ThumbnailValue).watched()

    def child_value_changed(self, child_value):
        self.root().Home.touch()

    def as_dict(self):
        d = dict(
            color=self.color.get(),
            thumbnail=self.thumbnail.get(),
        )
        return d


class ProjectsSettings(flow.Map):

    @classmethod
    def _create_value_store(cls, parent, name):
        '''
        The DKSHome is a SessionObject (base classe of `Home`)
        so it uses a MemoryValueStore and nothing is saved to the
        db (this is needed by `Home`).
        But we need to save the settings so we re-configure to the
        default value store here (the one from the root).
        '''
        return parent.root()._mng.value_store

    @classmethod
    def mapped_type(cls):
        return ProjectSettings

    def get_project_settings(self, project_name):
        if not self.has_mapped_name(project_name):
            settings = self.add(project_name)
        else:
            settings = self.get_mapped(project_name)
        return settings

    def get_settings_dict(self, project_name):
        return self.get_project_settings().as_dict()


class HomeSettings(flow.Object):

    @classmethod
    def _create_value_store(cls, parent, name):
        '''
        The DKSHome is a SessionObject (base classe of `Home`)
        so it uses a MemoryValueStore and nothing is saved to the
        db (this is needed by `Home`).
        But we need to save the settings so we re-configure to the
        default value store here (the one from the root).
        '''
        return parent.root()._mng.value_store

    show_status = flow.BoolParam()
    show_archived = flow.SessionParam(False).ui(editor='bool')
    button_height = flow.IntParam(100)
    default_thumbnail = flow.Param('', ThumbnailValue)


class ShowButtonHomeAction(flow.Action):

    ICON = ('icons.gui', 'home-outline')
    _home = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        self._home.use_custom_page = True
        return self.get_result(goto=self._home.oid())


class ButtonHome(Home):
    home_settings = flow.Child(HomeSettings)
    projects_settings = flow.Child(ProjectsSettings)

    back = flow.Child(ShowButtonHomeAction)

    def __init__(self, *args, **kwargs):
        super(ButtonHome, self).__init__(*args, **kwargs)
        self.use_custom_page = True

    def _fill_ui(self, ui):
        if self.use_custom_page:
            ui['custom_page'] = 'kabaret.flow_button_pages.button_home.ButtonHomePage'


class ButtonHomeRoot(HomeRoot):

    Home = flow.Child(ButtonHome)

    def set_flow_actor(self, flow_actor):
        self.flow_actor = flow_actor
