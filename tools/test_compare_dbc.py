"""Regression checks for historical DBC comparison. Author: Neil Mitchell."""
import struct,tempfile,unittest
from pathlib import Path
from compare_dbc import compare,parse

def table(rows,strings):
    return struct.pack('<4s4I',b'WDBC',len(rows),3,12,len(strings))+b''.join(struct.pack('<3I',*r) for r in rows)+strings

class DiffTests(unittest.TestCase):
    def diff(self,a,b):
        with tempfile.TemporaryDirectory() as d:return compare({'spellvisualeffectname.dbc':a},{'spellvisualeffectname.dbc':b},Path(d)/'diff.csv.gz')[0]
    def test_offset_churn_is_not_text_change(self):
        x=self.diff(table([(1,1,3)],b'\0A\0B\0'),table([(1,3,1)],b'\0B\0A\0'))
        self.assertEqual(x['changed_fields'],0);self.assertFalse(x['byte_identical'])
    def test_decoded_text_edit(self):
        x=self.diff(table([(1,1,3)],b'\0A\0B\0'),table([(1,1,3)],b'\0C\0B\0'))
        self.assertEqual(x['changed_fields'],1)
    def test_added_and_removed_ids(self):
        x=self.diff(table([(1,1,3)],b'\0A\0B\0'),table([(2,1,3)],b'\0A\0B\0'))
        self.assertEqual(x['added_record_ids'],[2]);self.assertEqual(x['removed_record_ids'],[1])
    def test_corrupt_length_and_duplicate_id(self):
        with self.assertRaises(ValueError):parse(table([(1,1,3)],b'\0A\0B\0')+b'X')
        with self.assertRaises(ValueError):parse(table([(1,1,3),(1,1,3)],b'\0A\0B\0'))

if __name__=='__main__':unittest.main()
