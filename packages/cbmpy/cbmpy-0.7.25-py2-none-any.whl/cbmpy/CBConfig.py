"""
CBMPy: CBConfig module
======================
PySCeS Constraint Based Modelling (http://cbmpy.sourceforge.net)
Copyright (C) 2009-2018 Brett G. Olivier, VU University Amsterdam, Amsterdam, The Netherlands

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

Author: Brett G. Olivier
Contact email: bgoli@users.sourceforge.net
Last edit: $Author: bgoli $ ($Id: CBConfig.py 689 2019-06-28 14:16:52Z bgoli $)

"""
## gets rid of "invalid variable name" info
# pylint: disable=C0103
## gets rid of "line to long" info
# pylint: disable=C0301
## use with caution: gets rid of module xxx has no member errors (run once enabled)
# pylint: disable=E1101

# preparing for Python 3 port
from __future__ import division, print_function
from __future__ import absolute_import
#from __future__ import unicode_literals

# release

try:
    STATUS = '$Rev: 689 $'.replace('Rev: ', '').replace('$', '').strip()
except Exception:
    STATUS = ''

__CBCONFIG__ = {'VERSION_MAJOR' : 0,
                'VERSION_MINOR' : 7,
                'VERSION_MICRO' : 25,
                'VERSION_STATUS' : STATUS,
                'VERSION' : None,
                'DEBUG' : False,
                'SOLVER_PREF' : 'CPLEX',
                #'SOLVER_PREF' : 'GLPK',
                'SOLVER_ACTIVE' : None,
                'REVERSIBLE_SYMBOL' : '<==>',
                'IRREVERSIBLE_SYMBOL' : '-->',
                'HAVE_SBML2' : False,
                'HAVE_SBML3' : False,
                'CBMPY_DIR' : None,
                'CBMPY_CGLPK_VER' : 'w452',
                'SYMPY_DENOM_LIMIT' : 10**32
               }

def current_version():
    """
    Return the current CBMPy version as a string

    """
    #return '%s.%s.%s [r%s]' % (__CBCONFIG__['VERSION_MAJOR'], __CBCONFIG__['VERSION_MINOR'], __CBCONFIG__['VERSION_MICRO'], __CBCONFIG__['VERSION_STATUS'])
    if STATUS == '':
        return '{}.{}.{}'.format(__CBCONFIG__['VERSION_MAJOR'], __CBCONFIG__['VERSION_MINOR'], __CBCONFIG__['VERSION_MICRO'])
    else:
        return '{}.{}.{}.{}'.format(__CBCONFIG__['VERSION_MAJOR'], __CBCONFIG__['VERSION_MINOR'], __CBCONFIG__['VERSION_MICRO'], STATUS)

def current_version_tuple():
    """
    Return the current CBMPy version as a tuple (x, y, z)

    """
    return (__CBCONFIG__['VERSION_MAJOR'], __CBCONFIG__['VERSION_MINOR'], __CBCONFIG__['VERSION_MICRO'])

__CBCONFIG__['VERSION'] = current_version()


