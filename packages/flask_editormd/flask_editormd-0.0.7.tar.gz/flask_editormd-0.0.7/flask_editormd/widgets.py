#!/usr/bin/env python
# -*-coding:utf-8-*-

from wtforms.widgets import HTMLString, TextArea


class Editormd(TextArea):
    def __call__(self, field, **kwargs):
        html = ''

        editormd_pre_html = '<div id="{0}">'.format(field.editor_id)
        editormd_post_html = '</div>'

        class_ = kwargs.pop('class', '').split() + \
                 kwargs.pop('class_', '').split()
        html += editormd_pre_html + super(Editormd, self).__call__(
            field, class_=' '.join(class_), **kwargs) + editormd_post_html
        return HTMLString(html)
