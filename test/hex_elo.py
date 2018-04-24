from .hex_ia import HexIA
from .hex_board import HexBoard

from uct import UCT
from parameters import Params

import traceback
import random
import requests
import json


class hex_elo:
    @staticmethod
    def run():
        nns = {
            "cnn525": {
                "nn": [
                    "check_b7x7v2_v1_v2_375.pth.tar",
                    "check_b7x7v2_v1_v2_450.pth.tar",
                    "check_b7x7v2_v1_v2_525.pth.tar",
                    "check_b7x7v2_v1_v2_600.pth.tar",
                    "check_b7x7v2_v1_v2_675.pth.tar"
                ],
                "id": 186
            },

            "cnn1050": {
                "nn": [
                    "check_b7x7v2_v1_v2_900.pth.tar",
                    "check_b7x7v2_v1_v2_975.pth.tar",
                    "check_b7x7v2_v1_v2_1050.pth.tar",
                    "check_b7x7v2_v1_v2_1125.pth.tar",
                    "check_b7x7v2_v1_v2_1200.pth.tar"
                ],
                "id": 180
            },

            "cnn1500": {
                "nn": [
                    "check_b7x7v2_v1_v2_1350.pth.tar",
                    "check_b7x7v2_v1_v2_1425.pth.tar",
                    "check_b7x7v2_v1_v2_1500.pth.tar",
                    "check_b7x7v2_v1_v2_1575.pth.tar",
                    "check_b7x7v2_v1_v2_1650.pth.tar"
                ],
                "id": 187
            },

            "cnn2025": {
                "nn": [
                    "check_b7x7v2_v1_v2_1875.pth.tar",
                    "check_b7x7v2_v1_v2_1950.pth.tar",
                    "check_b7x7v2_v1_v2_2025.pth.tar",
                    "check_b7x7v2_v1_v2_2100.pth.tar",
                    "check_b7x7v2_v1_v2_2175.pth.tar"
                ],
                "id": 181
            },

            "cnn2550": {
                "nn": [
                    "check_b7x7v2_v1_v2_2400.pth.tar",
                    "check_b7x7v2_v1_v2_2475.pth.tar",
                    "check_b7x7v2_v1_v2_2550.pth.tar",
                    "check_b7x7v2_v1_v2_2625.pth.tar",
                    "check_b7x7v2_v1_v2_2700.pth.tar"
                ],
                "id": 188
            },

            "cnn3000": {
                "nn": [
                    "check_b7x7v2_v1_v2_2850.pth.tar",
                    "check_b7x7v2_v1_v2_2925.pth.tar",
                    "check_b7x7v2_v1_v2_3000.pth.tar",
                    "check_b7x7v2_v1_v2_3075.pth.tar",
                    "check_b7x7v2_v1_v2_3150.pth.tar"
                ],
                "id": 182
            },

            "cnn3525": {
                "nn": [
                    "check_b7x7v2_v1_v2_3375.pth.tar",
                    "check_b7x7v2_v1_v2_3450.pth.tar",
                    "check_b7x7v2_v1_v2_3525.pth.tar",
                    "check_b7x7v2_v1_v2_3600.pth.tar",
                    "check_b7x7v2_v1_v2_3675.pth.tar"
                ],
                "id": 189
            },

            "cnn4050": {
                "nn": [
                    "check_b7x7v2_v1_v2_3900.pth.tar",
                    "check_b7x7v2_v1_v2_3975.pth.tar",
                    "check_b7x7v2_v1_v2_4050.pth.tar",
                    "check_b7x7v2_v1_v2_4125.pth.tar",
                    "check_b7x7v2_v1_v2_4200.pth.tar"
                ],
                "id": 183
            },

            "cnn4500": {
                "nn": [
                    "check_b7x7v2_v1_v2_4350.pth.tar",
                    "check_b7x7v2_v1_v2_4425.pth.tar",
                    "check_b7x7v2_v1_v2_4500.pth.tar",
                    "check_b7x7v2_v1_v2_4575.pth.tar",
                    "check_b7x7v2_v1_v2_4650.pth.tar"
                ],
                "id": 190
            },

            "cnn5025": {
               "nn": [
                   "check_b7x7v2_v1_v2_4875.pth.tar",
                   "check_b7x7v2_v1_v2_4950.pth.tar",
                   "check_b7x7v2_v1_v2_5025.pth.tar",
                   "check_b7x7v2_v1_v2_5100.pth.tar",
                   "check_b7x7v2_v1_v2_5175.pth.tar"
               ],
               "id": 184
            },

            "cnn5550": {
               "nn": [
                   "check_b7x7v2_v1_v2_5400.pth.tar",
                   "check_b7x7v2_v1_v2_5475.pth.tar",
                   "check_b7x7v2_v1_v2_5550.pth.tar",
                   "check_b7x7v2_v1_v2_5625.pth.tar",
                   "check_b7x7v2_v1_v2_5700.pth.tar"
               ],
               "id": 191
            },

            "cnn6000": {
               "nn": [
                    "check_b7x7v2_v1_v2_5850.pth.tar",
                    "check_b7x7v2_v1_v2_5925.pth.tar",
                    "check_b7x7v2_v1_v2_6000.pth.tar",
                    "check_b7x7v2_v1_v2_6075.pth.tar",
                    "check_b7x7v2_v1_v2_6150.pth.tar"
               ],
               "id": 185
            }
        }

        for n in nns.keys():
            if nns[n]["id"] < 0:
                r = requests.post("http://127.0.0.1:9080/player/")
                j = json.loads(r.text)
                print(j)
                nns[n]["id"] = j["id_player"]
                with open("checkpoint/api_id.txt", "a") as p:
                    p.write(str(n) + ":" + str(nns[n]["id"]) + "\n")

        i = 0

        while True:
            try:
                c = nns.copy()
                j1 = random.choice(list(c))
                del c[j1]
                j2 = random.choice(list(c))

                ai1 = HexIA()
                v1 = random.choice(nns[j1]["nn"])
                ai1.load_checkpoint(filename=v1)
                print(str(ai1.nnet.summary()))
                ai2 = HexIA()
                v2 = random.choice(nns[j2]["nn"])
                ai1.load_checkpoint(filename=v2)
                uct1 = UCT(ai1)
                uct2 = UCT(ai2)

                b = HexBoard()
                player = Params.FIRST_PLAYER
                w = 0

                expansions = []
                rollouts = []
                while w == 0:
                    if player == Params.FIRST_PLAYER:
                        m, infos = uct1.next_turn(b, player)
                    else:
                        m, infos = uct2.next_turn(b, player)

                    player = Params.get_next_player(player)
                    b.play_move(m)
                    b.find_if_winner(m)
                    w = b.winner()
                    Params.ongoing()
                    expansions.append(infos["expansions"])
                    rollouts.append(infos["rollouts"])

                js = {
                    "id_player_1": int(nns[j1]["id"]),
                    "id_player_2": int(nns[j2]["id"]),
                    "moves": "none",
                    "winner": w,
                }
                requests.post("http://127.0.0.1:9080/game", json=json.dumps(js))
                print(requests.get("http://127.0.0.1:9080/players").text)
                print(str(i) + " : " + str(j1) + " vs " + str(j2) + " ->  " + str(w) )
                print("Expansions  - " + str(expansions))
                print("Rollouts  - " + str(rollouts))
                i += 1

                b = HexBoard()
                player = Params.FIRST_PLAYER
                w = 0

                expansions = []
                rollouts = []
                while w == 0:
                    if player == Params.FIRST_PLAYER:
                        m, infos = uct2.next_turn(b, player)
                    else:
                        m, infos = uct1.next_turn(b, player)

                    player = Params.get_next_player(player)
                    b.play_move(m)
                    b.find_if_winner(m)
                    w = b.winner()
                    Params.ongoing()
                    expansions.append(infos["expansions"])
                    rollouts.append(infos["rollouts"])

                js = {
                    "id_player_1": int(nns[j2]["id"]),
                    "id_player_2": int(nns[j1]["id"]),
                    "moves": "none",
                    "winner": w,
                }
                requests.post("http://127.0.0.1:9080/game", json=json.dumps(js))
                print(requests.get("http://127.0.0.1:9080/players").text)
                print(str(i) + " : " + str(j2) + " vs " + str(j1 ) + " ->  " + str(w) )
                print("Expansions  - " + str(expansions))
                print("Rollouts  - " + str(rollouts))
                i += 1


            except:
                traceback.print_exc()
