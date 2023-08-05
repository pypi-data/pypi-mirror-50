import unittest
from osm_export_tool.feature_selection.sql import SQLValidator, OverpassFilter

class TestSql(unittest.TestCase):

    def test_basic(self):
        s = SQLValidator("name = 'a name'")
        self.assertTrue(s.valid)

    def test_identifier_list(self):
        s = SQLValidator("natural in ('water','cliff')")
        self.assertTrue(s.valid)

    #TODO OGR uses text for all things so numerical comparisons will not be correct
    def test_float_value(self):
        s = SQLValidator("height > 20")
        self.assertTrue(s.valid)

    def test_not_null(self):
        s = SQLValidator("height IS NOT NULL")
        self.assertTrue(s.valid)

    def test_and_or(self):
        s = SQLValidator("height IS NOT NULL and height > 20")
        self.assertTrue(s.valid)
        s = SQLValidator("height IS NOT NULL or height > 20")
        self.assertTrue(s.valid)
        s = SQLValidator("height IS NOT NULL or height > 20 and height < 30")
        self.assertTrue(s.valid)

    def test_parens(self):
        s = SQLValidator("(admin IS NOT NULL and level > 4)")
        self.assertTrue(s.valid)
        s = SQLValidator("(admin IS NOT NULL and level > 4) AND height is not null")
        self.assertTrue(s.valid)

    def test_colons_etc(self):
        s = SQLValidator("addr:housenumber IS NOT NULL")
        self.assertFalse(s.valid)
        self.assertEqual(s.errors,['identifier with colon : must be in double quotes.'])
        s = SQLValidator("admin_level IS NOT NULL")
        self.assertTrue(s.valid)
        s = SQLValidator('"addr:housenumber" IS NOT NULL')
        self.assertTrue(s.valid)
        s = SQLValidator('"addr housenumber" IS NOT NULL')
        self.assertTrue(s.valid)

    def test_invalid_sql(self):
        s = SQLValidator("drop table planet_osm_polygon")
        self.assertFalse(s.valid)
        self.assertEqual(s.errors,['SQL could not be parsed.'])
        s = SQLValidator("(drop table planet_osm_polygon)")
        self.assertFalse(s.valid)
        self.assertEqual(s.errors,['SQL could not be parsed.'])
        s = SQLValidator ("")
        self.assertFalse(s.valid)
        self.assertEqual(s.errors,['SQL could not be parsed.'])
        s = SQLValidator("name = 'a name'; blah")
        self.assertFalse(s.valid)
        self.assertEqual(s.errors,['SQL could not be parsed.'])

    def test_column_names(self):
        s = SQLValidator("(admin IS NOT NULL and level > 4) AND height is not null")
        self.assertTrue(s.valid)
        self.assertEqual(s.column_names,['admin','level','height'])


class TestOverpassFilter(unittest.TestCase):
    def test_basic(self):
        s = OverpassFilter("name = 'somename'")
        self.assertEqual(s.filter(),["[name='somename']"])
        s = OverpassFilter("level > 4")
        self.assertEqual(s.filter(),["[level]"])

    def test_basic_list(self):
        s = OverpassFilter("name IN ('val1','val2')")
        self.assertEqual(s.filter(),["[name~'val1|val2']"])

    def test_whitespace(self):
        s = OverpassFilter("name = 'some value'")
        self.assertEqual(s.filter(),["[name='some value']"])

    def test_notnull(self):
        s = OverpassFilter("name is not null")
        self.assertEqual(s.filter(),["[name]"])

    def test_and_or(self):
        s = OverpassFilter("name1 = 'foo' or name2 = 'bar'")
        self.assertEqual(s.filter(),["[name1='foo']","[name2='bar']"])
        s = OverpassFilter("(name1 = 'foo' and name2 = 'bar') or name3 = 'baz'")
        self.assertEqual(s.filter(),["[name1='foo']","[name2='bar']","[name3='baz']"])
