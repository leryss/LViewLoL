from lview import *

lview_script_info = {
	"script": "Draw Enemy Attack Range",
	"author": "rootcause0",
	"description": "Draws Enemy Champion Attack Range",

}

def lview_load_cfg(cfg):
	global draw_enemy_attack_range
	draw_enemy_attack_range        = cfg.get_bool("draw_enemy_attack_range", True)
	                     
	
def lview_save_cfg(cfg):
	global draw_enemy_attack_range
	cfg.set_bool("draw_enemy_attack_range", draw_enemy_attack_range)
	
def lview_draw_settings(game, ui):
	pass
	
def lview_update(game, ui):
	if draw_enemy_attack_range:
		draw_overlay_on_champ(game,game.champs)
    
        
def draw_overlay_on_champ(game,champ):
  color = Color.GREEN
  color.a = 0.5
  for champ in game.champs:
   if champ.is_enemy_to(game.player):
   	game.draw_circle_world(champ.pos, champ.base_atk_range + champ.gameplay_radius, 100, 2, color)
   