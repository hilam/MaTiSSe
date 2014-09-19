#!/usr/bin/env python
"""
header.py, module definition of Header class.
This defines the theme of the slide header element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
# MaTiSSe.py modules
from ..theme_element import ThemeElement
# class definition
class Header(ThemeElement):
  """
  Object for handling the presentation theme slide header, its attributes and methods.
  """
  def __init__(self,number,source=None):
    """
    Parameters
    ----------
    number : int
      number of header in the global numeration
    source : str, optional
      string (as single stream) containing the source

    Attributes
    ----------
    number : int
      number of header in the global numeration
    """
    self.number = number
    super(Header,self).__init__(data_tag=r'theme_slide_header_'+str(self.number),class_name='slide-header_'+str(self.number))
    self.data.data['height'] = ['0%',False]
    if source:
      self.get(source)
      self.check_specials()
    return

  def get_options(self):
    """Method for getting the available data options."""
    string = ['\n\nSlide Header']
    string.append(self.data.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """
    Method for getting css from data.

    Parameters
    ----------
    only_custom : bool, optional
      consider only the (user) customized data
    as_list : bool, optional
      return a list instead of a string

    Returns
    -------
    str
      a string containing the css code of the element if as_list = False
    list
      a list of one string containing the css code of the element if as_list = True
    """
    css = "\n.slide-header_"+str(self.number)+" {\n  padding:0;"
    css += self.data.get_css(only_custom=only_custom)
    css += "\n}\n"
    if as_list:
      return [css]
    else:
      return css