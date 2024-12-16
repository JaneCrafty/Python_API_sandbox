def test_phrase_length():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f"The phrase '{phrase}' is not shorter than 15 characters!"
