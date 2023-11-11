from Animations import Animations
import unittest

class Test_Player(unittest.TestCase):

    def test_codesAppearInOrderFailsSingle(self):
        Animations.animationsList = ["a", "b", "c", "d", "e"]
        assert Animations.codesAppearInOrder(["r"]) == False

    def test_codesAppearInOrderFailsMultiple(self):
        Animations.animationsList = ["a", "b", "c", "d", "e"]
        assert Animations.codesAppearInOrder(["c", "b"]) == False

    def test_codesAppearInOrderPassesSingle(self):
        Animations.animationsList = ["a", "b", "c", "d", "e"]
        assert Animations.codesAppearInOrder(["c"]) == True

    def test_codesAppearInOrderPassesMultiple(self):
        Animations.animationsList = ["a", "b", "c", "d", "e"]
        assert Animations.codesAppearInOrder(["b", "c", "d"]) == True