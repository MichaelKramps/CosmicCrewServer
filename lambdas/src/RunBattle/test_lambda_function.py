from lambda_function import lambda_handler

class Test_LambdaFunction(unittest.TestCase):
    def test_setsPlayers(self):
        simulator = DogfightSimulator("1", "1")
        assert simulator.playerOne != None
        assert simulator.playerTwo != None