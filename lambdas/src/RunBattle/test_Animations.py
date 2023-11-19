from Animations import Animations
import unittest

class Test_Animations(unittest.TestCase):

    def test_codesAppearInOrderFailsSingle(self):
        animations = Animations();
        animations.animationsList = ["a", "b", "c", "d", "e"]
        assert animations.codesAppearInOrder(["r"]) == False

    def test_codesAppearInOrderFailsMultiple(self):
        animations = Animations();
        animations.animationsList = ["a", "b", "c", "d", "e"]
        assert animations.codesAppearInOrder(["c", "b"]) == False

    def test_codesAppearInOrderPassesSingle(self):
        animations = Animations();
        animations.animationsList = ["a", "b", "c", "d", "e"]
        assert animations.codesAppearInOrder(["c"]) == True

    def test_codesAppearInOrderPassesMultiple(self):
        animations = Animations();
        animations.animationsList = ["a", "b", "c", "d", "e"]
        assert animations.codesAppearInOrder(["b", "c", "d"]) == True