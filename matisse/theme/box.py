#!/usr/bin/env python
"""
box.py, module definition of Box class.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
import sys
# modules not in the standard library
try:
  from yattag import Doc
except ImportError :
  sys.stderr.write("Error: can't import module 'yattag'")
  sys.exit(1)
# global variables
# regular expressions
__rebox__ = re.compile(r"\$box(?P<box>.*?)\$endbox",re.DOTALL)
__restl__ = re.compile(r"\$style\[(?P<style>.*?)\]",re.DOTALL)
__rectn__ = re.compile(r"\$content(\((?P<ctn_type>.*?)\))*(\[(?P<ctn_options>.*?)\])*\{(?P<ctn>.*?)\}",re.DOTALL)
__recap__ = re.compile(r"\$caption(\((?P<cap_type>.*?)\))*(\[(?P<cap_options>.*?)\])*(\{(?P<cap>.*?)\})*",re.DOTALL)
__cap_type__    = {'figure': 'Figure', 'table': 'Table', 'note': 'Note', 'box': ''  }
# classes definition
class Box(object):
  """
  Object for handling a box. It is an environment that can contains anythings (figures, tables, notes...).

  The syntax is:

  $box
  $style[style_options]
  $caption(caption_type)[caption_options]{caption}
  $content(content_type)[content_options]{content}
  $endbox

  Note:
  1. "$style[...]" is optional; it defines the style's options for the whole box; "style_options" are valid
     css syntax statements  (e.g. "font-variant:small-caps;");
  2. "$caption(...)[...]{...}" is optional: it defines the box's caption; the "caption_type" defines the
     caption prefixing "class" (e.g. "Fig." for figures): any sentences are valid; the "caption_options" defines
     the style's options of only caption: they are valid css syntax statements (e.g.  "padding:0 2%;"); the
     "caption" (inside the {} parenthesis) defines the caption text; note that "caption_type" and "caption_options"
     are optional thus the following statements are valid:
     + $caption[font-variant:small-caps;]{My caption without caption_type};
     + $caption{My caption without caption_type and caption_options};
  3. "$content(...)[...]{...}" is not optional: it defines the box's content; the "content_type" defines the type
     of the content that can be 'figure', 'table', 'note' and 'box' for generic environments; the "content_options"
     defines the style's options of only content: they are valid css syntax statements (e.g.  "padding:0 2%;"); the
     "content" (inside the {} parenthesis) defines the content (being text, figures, tables, etc...); note that
     "content_type" and "content_options" are optional thus the following statements are valid:
     + $content[font-variant:small-caps;]{My content without content_type};
     + $content{My content without content_type and content_options};

  There some helper (sub)classes based on Box class for handling specific environments such Figure, Table and Note.

  Note that the themes of box environments can be defined as all other theme elements in order to not have to repeat
  the styling options for each box. To this aim this module provides the "get_themes" function. The definition of such
  a theme can be stripped out by the function "strip_themes" also provided by this module.

  See Also
  --------
  Figure
  Table
  Note
  """
  def __init__(self,ctn_type='box'):
    """
    Parameters
    ----------
    ctn_type : {'figure','table','note','box'}, optional
      box content type

    Attributes
    ----------
    number : int
      box number
    style : str
      box style
    ctn_type : {'figure','table','note','box'}
      box content type
    ctn_options : str
      box content options
    ctn : str
      box content
    cap_type : {'figure','table','note'}
      box caption type
    cap_options : str
      box caption options
    cap : str
      box caption
    """
    self.number      = 0
    self.ctn_type    = ctn_type
    self.style       = None
    self.ctn_options = None
    self.cap_options = None
    self.cap_type    = None
    self.ctn         = None
    self.cap         = None
    return

  def __str__(self):
    string = []
    string.append('\nStyle: '+str(self.style))
    string.append('\nCaption('+str(self.cap_type)+')[options='+str(self.cap_options)+']: '+str(self.cap))
    string.append('\nContent('+str(self.ctn_type)+')[options='+str(self.ctn_options)+']: '+str(self.ctn))
    return ''.join(string)

  def __get_style(self,source):
    """Method for getting box style data."""
    match = re.search(__restl__,source)
    if match:
      style = match.group('style')
      if style:
        self.style = style.strip()
    return

  def __get_caption(self,source):
    """Method for getting box caption data."""
    match = re.search(__recap__,source)
    if match:
      cap_type = match.group('cap_type')
      if cap_type:
        if cap_type.lower() == 'none':
          self.cap_type = None
        else:
          self.cap_type = cap_type.strip()
      cap_options = match.group('cap_options')
      if cap_options:
        self.cap_options = cap_options.strip()
      self.cap = match.group('cap')
      if self.cap:
        self.cap = self.cap.strip()
    return

  def __get_content(self,source):
    """Method for getting box content data."""
    match = re.search(__rectn__,source)
    if match:
      ctn_type = match.group('ctn_type')
      if ctn_type:
        self.ctn_type = ctn_type.strip()
      ctn_options = match.group('ctn_options')
      if ctn_options:
        self.ctn_options = ctn_options.strip()
      self.ctn = match.group('ctn')
      if self.ctn:
        self.ctn = self.ctn.strip()
    return

  def get(self,source):
    """Method for getting box data."""
    self.__get_style(source)
    self.__get_caption(source)
    self.__get_content(source)
    return

  def caption_txt(self):
    """Method for building caption text.

    Returns
    -------
    str
      caption text
    """
    if self.cap_type and self.cap:
      txt = self.cap_type+' '+str(self.number)+': '+self.cap
    elif self.cap_type:
      txt = self.cap_type
    elif self.cap:
      txt = self.cap
    return txt

  def put_caption(self,doc):
    """Method for inserting caption into doc.

    Parameters
    ----------
    doc : yattag.Doc object
      yattag document where to put caption
    """
    if self.cap or self.cap_type:
      with doc.tag('div',klass='box caption'):
        if self.cap_options:
          doc.attr(style=self.cap_options)
        doc.text(self.caption_txt())
    return

  def to_html(self):
    """Method for inserting box to the html doc."""
    doc = Doc()
    with doc.tag('div',markdown='1',klass='box'):
      if self.style:
        doc.attr(style=self.style)
      with doc.tag('div',klass='box content'):
        if self.ctn_options:
          doc.attr(style=self.ctn_options)
        doc.text(self.ctn)
      self.put_caption(doc=doc)
    return doc.getvalue()

def parse(source):
  """Method for parsing source substituting boxes with their own html equivalent.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  str
    source string parsed
  """
  parsed_source = source
  for match in re.finditer(__rebox__,parsed_source):
    box = Box()
    box.get(source=match.group('box'))
    parsed_source = re.sub(__rebox__,box.to_html(),parsed_source,1)
  return parsed_source
