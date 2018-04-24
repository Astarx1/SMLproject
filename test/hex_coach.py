from hex.hex_coach import HexCoach
from hex.hex_game_manager import HexGameManager

import traceback


class hex_coach_test_routine:
    @staticmethod
    def run():
        try:
            print("Coach test running ...")
            hex_coach_test_routine.test_games_to_file()
            print("Coach test OK !")
        except Exception:
            traceback.print_exc()

    @staticmethod
    def test_games_to_file():
        import os
        if os.path.isfile("hex/data/5by5self.dat"):
            os.remove("hex/data/5by5self.dat")
        c = HexCoach()
        c.trainAI()