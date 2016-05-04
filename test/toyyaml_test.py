# coding: utf8

import unittest

from toyyaml.toyyaml import loads


class ToyyamlTest(unittest.TestCase):
    def test_dict_data(self):
        result = loads("""hr:  65    # Home runs
avg: 0.278 # Batting average
rbi: 147   # Runs Batted In""")
        self.assertTrue(isinstance(result, dict))
        self.assertEquals(len(result), 3)
        self.assertEquals(result.keys(), ["hr", "avg", "rbi"])
        self.assertEquals(result["hr"], 65)
        self.assertEquals(result["avg"], 0.278)
        self.assertEquals(result["rbi"], 147)

    def test_dict_data(self):
        result = loads("""hr:  "65 #"    # Home runs
avg: 0.278 # Batting average
rbi: 147   # Runs Batted In""")
        self.assertTrue(isinstance(result, dict))
        self.assertEquals(len(result), 3)
        self.assertTrue(all(key in result.keys() for key in ("hr", "avg", "rbi")))
        self.assertEquals(result["hr"], "65 #")
        self.assertEquals(result["avg"], 0.278)
        self.assertEquals(result["rbi"], 147)

    def test_indentation_determines_scope(self):
        result = loads("""name: Mark McGwire
accomplishment: >
  Mark set a major league

  home run record in 1998.
stats: |
  65 Home Runs
  0.278 Batting Average""")
        self.assertEquals(len(result), 3)
        self.assertTrue(all([key in result.keys() for key in ["name", "accomplishment", "stats"]]))
        self.assertEquals(result["accomplishment"], "Mark set a major league\n\nhome run record in 1998.")
        self.assertEquals(result["stats"], "65 Home Runs\n0.278 Batting Average")

    def test_mapping_scalars_to_sequences(self):
        result = loads("""american:
  - Boston Red Sox

  - Detroit Tigers
  - New York Yankees
national:
  - New York Mets
  - Chicago Cubs
  - Atlanta Braves""")
        self.assertEquals(len(result), 2)
        self.assertTrue(all([key in result.keys() for key in ["american", "national"]]))
        self.assertTrue(isinstance(result["national"], list))
        self.assertTrue(isinstance(result["american"], list))
        self.assertEquals(result["american"], ["Boston Red Sox", "Detroit Tigers", "New York Yankees"])
        self.assertEquals(result["national"], ["New York Mets", "Chicago Cubs", "Atlanta Braves"])

    def test_sequence_of_mappings(self):
        result = loads("""-
  name: Mark McGwire
  hr:   65
  avg:  0.278
-
  name: Sammy Sosa
  hr:   63
  avg:  0.288""")
        self.assertTrue(isinstance(result, list))
        self.assertEquals(len(result), 2)
        self.assertTrue(all(key in result[0].keys() for key in ("name", "hr", "avg")))
        self.assertTrue(result[0]["name"], "Mark McGwire")
        self.assertTrue(result[0]["hr"], 65)
        self.assertTrue(result[0]["avg"], 0.278)
        self.assertTrue(all(key in result[1].keys() for key in ("name", "hr", "avg")))
        self.assertTrue(result[1]["name"], "Sammy Sosa")
        self.assertTrue(result[1]["hr"], 63)
        self.assertTrue(result[1]["avg"], 0.288)

    def test_sequence_of_sequences(self):
        result = loads("""- [name        , hr, avg  ]
- [Mark McGwire, 65, 0.278]
- [Sammy Sosa  , 63, 0.288]""")
        self.assertTrue(isinstance(result, list))
        self.assertEquals(len(result), 3)
        self.assertTrue(all(isinstance(row, list) for row in result))
        self.assertTrue(all(key in result[0] for key in ("name", "hr", "avg")))
        self.assertTrue(all(key in result[1] for key in ("Mark McGwire", 65, 0.278)))
        self.assertTrue(all(key in result[2] for key in ("Sammy Sosa", 63, 0.288)))

    def test_mapping_of_mappings(self):
        result = loads("""Mark McGwire: {hr: 65, avg: 0.278}
Sammy Sosa: {
    hr: 63,
    avg: 0.288
  }""")
        self.assertTrue(isinstance(result, dict))
        self.assertEquals(len(result), 2)
        self.assertTrue(all(isinstance(row, dict) for row in result.values()))

    def test_mapping_of_mappings_with_comment(self):
        result = loads("""Mark McGwire: {hr: 65, avg: 0.278}
Sammy Sosa: {
    hr: 63, #aaaa
    avg: 0.288 #bbb
  }""")
        self.assertTrue(isinstance(result, dict))
        self.assertEquals(len(result), 2)
        self.assertTrue(all(isinstance(row, dict) for row in result.values()))
        self.assertTrue(all(key in result for key in ("Mark McGwire", "Sammy Sosa")))
        self.assertEquals(result["Sammy Sosa"]["hr"], 63)
        self.assertEquals(result["Sammy Sosa"]["avg"], 0.288)

    def test_two_documents_in_a_stream(self):
        result = loads("""# Ranking of 1998 home runs
---
- Mark McGwire
- Sammy Sosa
- Ken Griffey

# Team ranking
---
- Chicago Cubs
- St Louis Cardinals""")
        self.assertTrue(isinstance(result, list))
        self.assertEquals(len(result), 2)
        self.assertTrue(all(isinstance(row, list) for row in result))
        self.assertEquals(len(result[0]), 3)
        self.assertEquals(len(result[1]), 2)

