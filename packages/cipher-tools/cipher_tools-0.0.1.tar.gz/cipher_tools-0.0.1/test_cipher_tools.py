from cipher_tools import shift, shift_letter, rot13


def test_shift_lower():
    assert shift("abc", 5) == "fgh"


def test_shift_upper():
    assert shift("ABC", 5) == "FGH"


def test_shift_mixedcase():
    assert shift("aBc", 5) == "fGh"


def test_shift_with_non_letter_charaters():
    assert shift("acc1234acc", 5) == "fhh1234fhh"


def test_rot13_against_shift():
    assert rot13("abc123ABC!'£") == shift("abc123ABC!'£", 13)


def test_rot13_double_equals_original():
    string = "234lkjfdFKDJLKSD@'dfs&(*khjsfdHKJ"
    assert rot13(rot13(string)) == string
