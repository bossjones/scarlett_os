from pdb import DefaultConfig


class Config(DefaultConfig):
    prompt = 'pdb> '
    sticky_by_default = True
    editor = 'vim'

# import readline
# import pdb
# # from pdb import DefaultConfig
#
# # This module defines utility function to assist in dynamic creation of
# # new types. It also defines names for some object types that are used by
# # the standard Python interpreter, but not exposed as builtins like int or
# # str are. Finally, it provides some additional type-related utility
# # classes and functions that are not fundamental enough to be builtins.
#
# import types
#
# from pprint import pprint
#
#
# # alias dump for attr in dir(%1): f hasattr(%1, attr): print("obj.%s = %s" % (attr, getattr(%1, attr)))
#
# def dump_instance(obj):
#     for attr in dir(obj):
#         if hasattr(obj, attr):
#             print("obj.%s = %s" % (attr, getattr(obj, attr)))
#
#
# def search_member(obj, query=None):
#     if query:
#         results = (m for m in dir(obj) if query.lower() in m.lower())
#     else:
#         results = dir(obj)
#
#     for result in results:
#         print(result)
#
#
# # pdb++ support
# class Config(pdb.DefaultConfig):
#     prompt = 'pdb> '
#     sticky_by_default = True
#     editor = 'vim'
#
# # def setup(self, pdb):
# #
# #     def do_pp(self, arg):
# #         return pprint(self._getval(arg))
# #
# #     def do_pd(self, arg):
# #         return pprint(self._getval(arg).__dict__)
# #
# #     def do_sm(self, arg):
# #         if ':' not in arg:
# #             arg, query = arg, None
# #         else:
# #             arg, query = arg.split(':')
# #
# #         return search_member(self._getval(arg), query)
# #
# #     def do_dump(self, arg):
# #         if ':' not in arg:
# #             arg, query = arg, None
# #         else:
# #             arg, query = arg.split(':')
# #         return dump_instance(self._getval(arg))
# #
# #     # NOTE: Dynamic methods in python
# #     # source: http://www.igorsobreira.com/2011/02/06/adding-methods-dynamically-in-python.html
# #     # source: https://github.com/href/dotfiles/blob/74b7ee528fd65a0f38e4baacaa3e528a6a5bc60a/.pdbrc.py
# #     # pdb.do_pp = types.MethodType(do_pp, pdb)
# #     # pdb.do_sm = types.MethodType(do_sm, pdb)
# #     # pdb.do_pd = types.MethodType(do_pd, pdb)
# #     # pdb.do_dump = types.MethodType(do_dump, pdb)
# #
# #     Pdb = pdb.__class__
# #
# #     Pdb.do_dump = dump.__get__(Pdb)
# #
# #     # pdb.do_l = pdb.do_longlist
# #     # pdb.do_st = pdb.do_sticky
#
# sm = search_member
# dump = dump_instance


# #############################################################################
# #############################################################################
# #############################################################################
# # source: http://stackoverflow.com/questions/10729909/convert-builtin-function-type-to-method-type-in-python-3
# class BoundMethod(object):
#     def __init__(self, function):
#         self.function = function
#
#     def __get__(self, obj, objtype=None):
#         print('Getting', obj, objtype)
#         return self.function.__get__(obj, objtype)
#
#
# class Config(pdb.DefaultConfig):
#     prompt = 'pdb> '
#     sticky_by_default = True
#     editor = 'vim'
#
#     def __init__(self):
#         readline.parse_and_bind('set convert-meta on')
#         readline.parse_and_bind('Meta-/: complete')
#
#         # try:
#         #     from pygments.formatters import terminal
#         # except ImportError:
#         #     pass
#         # else:
#         #     self.colorscheme = terminal.TERMINAL_COLORS.copy()
#         #     self.colorscheme.update({
#         #         terminal.Keyword:            ('darkred',     'red'),
#         #         terminal.Number:             ('darkyellow',  'yellow'),
#         #         terminal.String:             ('brown',       'green'),
#         #         terminal.Name.Function:      ('darkgreen',   'blue'),
#         #         terminal.Name.Namespace:     ('teal',        'turquoise'),
#         #     })
#
#     def setup(self, pdb):
#         # make 'l' an alias to 'longlist'
#         Pdb = pdb.__class__
#         Pdb.do_l = Pdb.do_longlist
#         Pdb.do_st = Pdb.do_sticky
#         Pdb.do_dump = dump.__get__(Pdb)
#         Pdb.do_sm = search_member.__get__(Pdb)
#
# #############################################################################
# #############################################################################
# #############################################################################
# """
# This is an example configuration file for pdb++.
# Actually, it is what the author uses daily :-). Put it into ~/.pdbrc.py to use
# it.
# """
#
# import readline
# import pdb
#
# class Config(pdb.DefaultConfig):
#
#     editor = 'e'
#     stdin_paste = 'epaste'
#     filename_color = pdb.Color.lightgray
#     #exec_if_unfocused = "play ~/sounds/dialtone.wav 2> /dev/null &"
#
#     def __init__(self):
#         readline.parse_and_bind('set convert-meta on')
#         readline.parse_and_bind('Meta-/: complete')
#
#         try:
#             from pygments.formatters import terminal
#         except ImportError:
#             pass
#         else:
#             self.colorscheme = terminal.TERMINAL_COLORS.copy()
#             self.colorscheme.update({
#                 terminal.Keyword:            ('darkred',     'red'),
#                 terminal.Number:             ('darkyellow',  'yellow'),
#                 terminal.String:             ('brown',       'green'),
#                 terminal.Name.Function:      ('darkgreen',   'blue'),
#                 terminal.Name.Namespace:     ('teal',        'turquoise'),
#                 })
#
#     def setup(self, pdb):
#         # make 'l' an alias to 'longlist'
#         Pdb = pdb.__class__
#         Pdb.do_l = Pdb.do_longlist
#         Pdb.do_st = Pdb.do_sticky
