from lview import *
from commons.targeting import TargetingConfig
from time import time
import itertools, math
from commons.skills import *
from copy import copy
from math import *
from champions import index

lview_script_info = {
	"script": "Evader",
	"author": "anonymous developer",
	"description": "Evade module with LviewLoL"
}

is_top = True
draw_evade_line = False

bound_max = 0
evades = False
targeting = TargetingConfig()

def lview_load_cfg(cfg):
	global evades, is_top, draw_evade_line
	evades            = cfg.get_bool("evades", True)
	is_top = cfg.get_bool("is_top", True)
	draw_evade_line = cfg.get_bool("draw_evade_line", draw_evade_line)
	
def lview_save_cfg(cfg):
	global evades, is_top, draw_evade_line
	cfg.set_bool("evades",            evades)
	is_top = cfg.set_bool("is_top", is_top)
	draw_evade_line = cfg.set_bool("draw_evade_line", draw_evade_line)
	
def lview_draw_settings(game, ui):
	global evades, is_top, draw_evade_line
	ui.separator()
	ui.text("Evader (Experimental)")
	evades            = ui.checkbox("Evade skills", evades)
	is_top            = ui.checkbox("Standart dodge", is_top)
	draw_evade_line            = ui.checkbox("Draw line", draw_evade_line)
	draw_prediction_info(game, ui)
			
def evade(game, evade_pos, main_pos):
	game.move_cursor(game.world_to_screen(evade_pos))
	game.press_right_click()

def evade_skills(game, player):
	global targeting, evades, is_top, draw_evade_line
	player_pos = game.world_to_screen(game.player.pos)
	game.draw_text(player_pos, "Evade: ON", Color.CYAN)
	for missile in game.missiles:
		if not player.is_alive or missile.is_ally_to(player):
			continue
		if not is_skillshot(missile.name):
			continue
		spell = get_missile_parent_spell(missile.name)
		if not spell:
			continue
		end_pos = missile.end_pos.clone()
		start_pos = missile.start_pos.clone()
		curr_pos = missile.pos.clone()
		dodge_pos = player.pos.clone()
		br = player.gameplay_radius * 1
		p = game.world_to_screen(dodge_pos)
		old_cpos = game.get_cursor()
		# if dodge_pos.length() >= end_pos.length():
		# 	return
		if game.point_on_line(game.world_to_screen(start_pos), game.world_to_screen(end_pos), game.world_to_screen(dodge_pos), float(br)):
			game.draw_text(game.world_to_screen(dodge_pos), "Evade: ON", Color.RED)
			r = game.get_spell_info(spell.name).cast_radius
			percent_done = missile.start_pos.distance(curr_pos) / missile.start_pos.distance(end_pos)
			pos = getEvadePos(game, start_pos, end_pos, dodge_pos, br, missile, spell)
			if draw_evade_line:
				game.draw_line(game.world_to_screen(pos), game.world_to_screen(player.pos), 2, Color.ORANGE)
			evade(game, pos, old_cpos)
			index.useEvadeToChampion(game, pos)
				
def lview_update(game, ui):
	global evades
	
	player = game.player

	if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
		if evades:
			evade_skills(game, player)
					
				
