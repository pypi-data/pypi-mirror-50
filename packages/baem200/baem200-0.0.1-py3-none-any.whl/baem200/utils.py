"""This module illustrates how to write your docstring in OpenAlea
and other projects related to OpenAlea."""

__license__ = "Cecill-C"
__revision__ = " $Id: actor.py 1586 2009-01-30 15:56:25Z cokelaer $ "
__docformat__ = 'reStructuredText'


def meineFunc(txt):
	"""this function print the given argument

	usage:
	>>> meineFunc('Hallo Welt!')
	meineFunc :Hallo Welt!
	>>>
	"""
	print("meineFunc :" + txt)

def nochEineFunc(txt):
    """returns (arg1 / arg2) + arg3

    This is a longer explanation, which may include math with latex syntax
    :math:`\\alpha`.
    Then, you need to provide optional subsection in this order (just to be
    consistent and have a uniform documentation. Nothing prevent you to
    switch the order):

    - parameters using ':param <name>: <description>'
    - type of the parameters ':type <name>: <description>'
    - returns using ':returns: <description>'
    - examples (doctest)
    - seealso using '.. seealso:: text'
    - notes using '.. note:: text'
    - warning using '.. warning:: text'
    - todo '.. todo:: text'

    note:
    Ein Hinweis von mir

	>>> nochEineFunc('Hallo Welt!')
	nochEineFunc :Hallo Welt!


    """
    print("nochEineFunc :" + txt)

# pybach
# pybae

if __name__ == '__main__':
	import doctest
	doctest.testmod()

