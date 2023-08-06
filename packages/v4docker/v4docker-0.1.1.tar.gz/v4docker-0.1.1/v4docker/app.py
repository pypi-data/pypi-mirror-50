#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docker import client
from docker.models.images import Image
from picotui.basewidget import ACTION_OK
from picotui.defs import C_WHITE, C_GREEN, C_RED, C_MAGENTA
from picotui.screen import Screen
from picotui.widgets import Dialog, WDropDown, WButton, WLabel, WListBox


class MyListBox(WListBox):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        super().__init__(*args, **kwargs)

    def handle_edit_key(self, key):
        if key == b'd' and self.items:
            to_delete = self.items.pop(self.choice)
            try:
                self.app.info('deleting %s...' % to_delete)
                self.app.delete_image(to_delete)
                self.app.info('delete success:' + to_delete)
                self.set_lines(self.items)
                if self.total_lines == 0:
                    # no items
                    self.cur_line = 0
                    self.row = 0
                elif self.row == self.total_lines:
                    # delete last item
                    self.cur_line = self.row = self.cur_line - 1
            except Exception as e:
                self.app.warn('delete %s fail: %s' % (to_delete, e))
                self.set_lines(self.items + [to_delete])

        return super().handle_edit_key(key)


class App(object):
    def __init__(self):
        self.docker_client = client.from_env()
        self._init_screen()
        self._init_widgets()

    def _init_screen(self):
        self.screen = Screen()
        self.screen.init_tty()
        self.screen.enable_mouse()
        self.screen.attr_color(C_WHITE, C_MAGENTA)
        self.screen.cls()
        self.screen.attr_reset()
        self.width, self.height = Screen.screen_size()

    def _init_widgets(self):
        # filter choices
        self.dialog = Dialog(0, 0, self.width, self.height, title="Docker Image list")

        start_x, start_y = 1, 1
        self._init_image_list(start_x, start_y + 2)
        self._init_quit_button(start_x + 2, self.height - 5)
        self._init_info_bar(start_x + 1, self.height - 3)

    def _init_image_list(self, x, y):
        self.dialog.add(x, y, "Image List:")
        w_listbox = MyListBox(self, self.width - 5, self.height - 20,
                              ["%s    %s" % (i.short_id, i.base_url) for i in self.load_images()])
        w_listbox.focus = True
        self.dialog.add(x, y + 1, w_listbox)

    def _init_info_bar(self, x, y):
        self.info_bar = WLabel("信息", w=self.width - 5)
        self.dialog.add(x, y, self.info_bar)

    def _init_quit_button(self, x, y):
        b = WButton(8, "Quit")
        self.dialog.add(x, y, b)
        b.finish_dialog = ACTION_OK

    def load_images(self):
        images = []
        for i in self.docker_client.images.list():
            if i.tags:
                for tag in i.tags:
                    images.append(ImageObj(tag, i.short_id, i))
            else:
                images.append(ImageObj(i.short_id, i.short_id, i))
        sorted(images, key=lambda x: x.short_id)
        return images

    def delete_image(self, name):
        self.docker_client.images.remove(name.split()[1])

    def info(self, message):
        self.log(message, C_GREEN)

    def warn(self, message):
        self.log(message, C_RED)

    def log(self, message, color):
        self.info_bar.attr_color(color)
        self.info_bar.t = str(message)
        self.info_bar.redraw()
        self.info_bar.attr_reset()

    def run(self):
        try:
            self.dialog.loop()
        finally:
            self.docker_client.close()
            self.screen.goto(0, 50)
            self.screen.cursor(True)
            self.screen.disable_mouse()
            self.screen.deinit_tty()


class ImageObj:
    base_url: str
    short_id: str
    image_url: str
    tag: str
    created: str
    author: str
    version: str
    _image: Image

    def __init__(self, base_url: str, short_id: str, image: Image):
        self.base_url = base_url
        self.short_id = short_id
        self.image_url, self.tag = self.base_url.split(':')
        self._image = image
        self.created = image.attrs.get('Created')
        self.author = image.attrs.get('Author')
        self.version = image.attrs.get('Version')

    def __repr__(self):
        return f'{self.short_id}    {self.base_url}'
