from lview import *
from time import time
from champions import index
from commons.targeting import TargetingConfig

targeting = TargetingConfig() 

champion_combo = True
key_combo = 0
harass_toggled = False
harass_key = 0
toggled = False

lview_script_info = {
	"script": "Champion scripts",
	"author": "anonymous developer",
	"description": "Champion scripts for Lview"
}

def lview_load_cfg(cfg):
	global champion_combo, targeting, key_combo, harass_key, index, harass_toggled
	champion_combo = cfg.get_bool("champion_combo", True)
	key_combo    = cfg.get_int("key_combo", 0)
	harass_key   = cfg.get_bool("harass_key", 0)
	harass_toggled     = cfg.get_bool("harass_toggled", False)
	targeting.load_from_cfg(cfg)

def lview_save_cfg(cfg):
	global champion_combo, targeting, key_combo, harass_key, index, harass_toggled
	cfg.set_bool("champion_combo", champion_combo)
	cfg.set_bool("harass_key", harass_key)
	cfg.set_int("key_combo", key_combo)
	cfg.set_bool("harass_toggled", harass_toggled)
	targeting.save_to_cfg(cfg)

def lview_draw_settings(game, ui):
	global champion_combo, key_combo, harass_key, harass_toggled
	global targeting, index
	champ_name = game.player.name
	champion_combo = ui.checkbox(game.player.name, champion_combo)
	key_combo     = ui.keyselect("Combo activate key", key_combo)
	harass_key   = ui.keyselect("Harass", harass_key)
	harass_toggled     = ui.checkbox("Harass toggle mode", harass_toggled)
	targeting.draw(ui)

def lview_update(game, ui):
	global champion_combo, harass_toggled, key_combo, harass_key

	self = game.player

	if self.is_alive and self.is_visible and game.is_point_on_screen(self.pos):
		index.useHarrasMode(game)
				
		if not game.is_key_down(key_combo):
			return
			
		index.useComboToChampion(game)


    