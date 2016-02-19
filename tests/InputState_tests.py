#
# Unit tests for console.py
#

from unittest import TestCase, TestSuite, defaultTestLoader
from InputState import InputState

class TestInputState(TestCase):
    """Test the handling of key_complete"""

    def setUp(self):
        self.state = InputState()

    def testBasicCompletion(self):
        """Test the basic insertion of completed contend in current command"""
        self.state.before_cursor = 'C:\\'
        self.state.key_complete('C:\\Windows')
        self.assertEqual(self.state.before_cursor, 'C:\\Windows')
        self.assertEqual(self.state.after_cursor, '')

    def testAvoidDuplicateFillers(self):
        """Tests the avoidance of duplicate whitespace, backslash, quites after completing"""
        self.state.before_cursor = '"c:\\Program Files (x86)\\Sysinternals Suite'
        self.state.after_cursor = '"\\'
        self.state.key_complete('"c:\\Program Files (x86)\\Sysinternals Suite"\\')
        self.assertEquals(self.state.before_cursor, '"c:\\Program Files (x86)\\Sysinternals Suite"\\')
        self.assertEquals(self.state.after_cursor, '')

    def testExtendSelection1(self):
        self.state.before_cursor = 'cd d:\\Work\\bui'
        self.state.after_cursor = 'ld && make'
        self.state.reset_selection()

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, 'cd d:\\Work\\')
        self.assertEqual(self.state.after_cursor, 'build && make')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len('build'))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, 'cd ')
        self.assertEqual(self.state.after_cursor, 'd:\\Work\\build && make')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len('d:\\Work\\build'))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, '')
        self.assertEqual(self.state.after_cursor, 'cd d:\\Work\\build && make')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len('cd d:\\Work\\build '))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, '')
        self.assertEqual(self.state.after_cursor, 'cd d:\\Work\\build && make')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len(self.state.after_cursor))

    def testExtendSelection2(self):
        self.state.before_cursor = 'cd test && mak'
        self.state.after_cursor = 'e clean > NUL'
        self.state.reset_selection()

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, 'cd test && ')
        self.assertEqual(self.state.after_cursor, 'make clean > NUL')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len('make'))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, 'cd test &&')
        self.assertEqual(self.state.after_cursor, ' make clean > NUL')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len(' make clean '))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, 'cd test &&')
        self.assertEqual(self.state.after_cursor, ' make clean > NUL')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len(' make clean > NUL'))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, '')
        self.assertEqual(self.state.after_cursor, 'cd test && make clean > NUL')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len(self.state.after_cursor))

    def testExtendSelectionInQuotes(self):
        """Tests the extend/retract selection feature (Shift-Up/Dn)"""
        self.state.before_cursor = 'cd "c:\\Program Files (x86)\\Sysinter'
        self.state.after_cursor = 'nals Suite" && ls -l'
        self.state.reset_selection()

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, 'cd "c:\\Program Files (x86)\\')
        self.assertEqual(self.state.after_cursor, 'Sysinternals Suite" && ls -l')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len('Sysinternals'))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, 'cd "c:\\Program Files (x86)\\')
        self.assertEqual(self.state.after_cursor, 'Sysinternals Suite" && ls -l')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len('Sysinternals Suite'))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, 'cd "')
        self.assertEqual(self.state.after_cursor, 'c:\\Program Files (x86)\\Sysinternals Suite" && ls -l')
        self.assertEqual(self.state.selection_start,
                         len(self.state.before_cursor) + len('C:\\Program Files (x86)\\Sysinternals Suite'))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, 'cd ')
        self.assertEqual(self.state.after_cursor, '"c:\\Program Files (x86)\\Sysinternals Suite" && ls -l')
        self.assertEqual(self.state.selection_start,
                         len(self.state.before_cursor) + len('"C:\\Program Files (x86)\\Sysinternals Suite"'))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, '')
        self.assertEqual(self.state.after_cursor, 'cd "c:\\Program Files (x86)\\Sysinternals Suite" && ls -l')
        self.assertEqual(self.state.selection_start,
                         len(self.state.before_cursor) + len('cd "C:\\Program Files (x86)\\Sysinternals Suite" '))

        self.state.key_extend_selection(None)
        self.assertEqual(self.state.before_cursor, '')
        self.assertEqual(self.state.after_cursor, 'cd "c:\\Program Files (x86)\\Sysinternals Suite" && ls -l')
        self.assertEqual(self.state.selection_start, len(self.state.before_cursor) + len(self.state.after_cursor))

def suite():
    suite = TestSuite()
    suite.addTest(defaultTestLoader.loadTestsFromTestCase(TestInputState))
    return suite

