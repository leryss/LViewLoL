from . import yasuo

def useComboToChampion(game):
    if game.player.name == "yasuo":
        
def useHarrasMode(game):
    if game.player.name == "yasuo":

def useEvadeToChampion(game, save_pos):
    if game.player.name == "yasuo":
        return yasuo.Yasuo().evade(game, save_pos)

# class Legend:
#     def __init__(self, game):
#         self.game = game
        
#     def useComboToChampion(self):
#         self.game()
        
# class Yasuo(Legend):
#     def __init__(self):
#         super().__init__("Yasuo", yasuo.Yasuo().combo(self.game), yasuo.Yasuo().harras(self.game))

# yasuo = Yasuo()
# yasuo.useComboToChampion()
