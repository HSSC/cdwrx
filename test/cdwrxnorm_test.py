## -------------------------------------------
## package  : cdwlib
## author   : evan.phelps@gmail.com
## created  : Tue Mar 20 18:04:28 EST 2016
## vim      : ts=4


import os, sys
import unittest


sys.path.insert(0,os.path.abspath(__file__+"/../../src"))


class cdwrx_test(unittest.TestCase):

    def test_rxnorm_req(self):
        import rxnorm_wrappers as rxnwrap
        assert rxnwrap.rxnorm_req('', json=False).ok

    def test_coerce_rxcui(self):
        from rxnorm_wrappers import coerce_rxcui
        assert coerce_rxcui(1297400) == '1661345'

    def test_get_status(self):
        from rxnorm_wrappers import get_status
        assert get_status(1297400) == 'Remapped'

    def test_get_TTY(self):
        from rxnorm_wrappers import get_TTY
        assert get_TTY(161) == 'IN'

    def test_get_ins(self):
        from rxnorm_wrappers import get_ins
        assert get_ins(161)[0] == (u'161', u'Acetaminophen')

    def test_get_props(self):
        from rxnorm_wrappers import get_props
        assert get_props(161)['name'] == u'Acetaminophen'

        #check that skip_coerce works
        assert get_props(1297400, skip_coerce=True) is None
        assert get_props(1297400, skip_coerce=False)['tty'] == u'SBD'
        #check that skip_coerce default is False
        assert get_props(1297400)['tty'] == u'SBD'


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(cdwrx_test)
    unittest.TextTestRunner(verbosity=2).run(suite)
