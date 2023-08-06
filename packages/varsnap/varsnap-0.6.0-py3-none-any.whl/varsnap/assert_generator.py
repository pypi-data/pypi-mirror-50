import unittest

from . import core


class TestVarSnap(unittest.TestCase):
    def test_varsnap(self):
        results = []
        for consumer in core.CONSUMERS:
            consumer.last_snap_id = None
            result = consumer.consume()
            if not result:
                continue
            results.append(result)
        if not results:
            raise unittest.case.SkipTest('No Snaps found')
        results = [x[1] for x in results if not x[0]]
        if not results:
            self.assertTrue(True)
            return
        result_log = "\n\n".join(results)
        self.assertTrue(False, result_log)
