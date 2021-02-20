from lview import *
import math, itertools, time
from . import items
from enum import Enum

Version = "sdfjsdkfsd"
MissileToSpell = {}
SpellsToEvade = {}
Spells         = {}
ChampionSpells = {}

class HitChance(Enum):
	Immobile = 8
	Dashing = 7
	VeryHigh = 6
	High = 5
	Medium = 4
	Low = 3
	Impossible = 2
	OutOfRange = 1
	Collision = 0

_HitChance = HitChance.Impossible

class SFlag:
	Targeted        = 1
	Line            = 2
	Cone            = 4
	Area            = 8
	
	CollideWindwall = 16
	CollideChampion = 32
	CollideMob      = 64
	
	
	CollideGeneric   = CollideMob      | CollideChampion | CollideWindwall
	SkillshotLine    = CollideGeneric  | Line
	
class Spell:
	def __init__(self, name, missile_names, flags, delay = 0.0, danger = 1):
		global MissileToSpell, Spells
		
		self.flags = flags
		self.name = name
		self.missiles = missile_names
		self.delay = delay
		self.danger = danger
		Spells[name] = self
		for missile in missile_names:
			MissileToSpell[missile] = self
			
	delay    = 0.0
	danger 	 = 1
	flags    = 0
	name     = "?"
	missiles = []
	skills = []

class DodgeSpell:
	def __init__(self, name, slot):
		global MissileToSpell, Spells
		self.slot = slot
		self.name = name
	slot = "?"
	name = "?"


ChampionSpells = {
	"aatrox": [
		Spell("aatroxq1",                ["aatroxq1"],                               SFlag.CollideGeneric),
		Spell("aatroxq",                [],                               SFlag.CollideGeneric),
		Spell("aatroxw",                ["aatroxw"],                               SFlag.CollideGeneric)
	],
	"rell": [
		Spell("rellq",                [],                               SFlag.CollideGeneric)
	],
	"quinn": [
		Spell("quinnq",                ["quinnq"],                               SFlag.CollideGeneric)
	],
	"aurelionsol": [
		Spell("aurelionsolq",           ["aurelionsolqmissile"],                   SFlag.SkillshotLine),
		Spell("aurelionsolr",           ["aurelionsolrbeammissile"],               SFlag.Line | SFlag.CollideWindwall)
	],
	"ahri": [                                                                      
		Spell("ahriorbofdeception",     ["ahriorbmissile"],                        SFlag.Line | SFlag.CollideWindwall),
		Spell("ahriseduce",             ["ahriseducemissile"],                     SFlag.CollideGeneric)
	],
	"ashe": [
		Spell("enchantedcrystalarrow",  ["enchantedcrystalarrow"],                 SFlag.Area | SFlag.Cone)
	],
	"shen": [                           
		Spell("shene",           ["shene"], 			SFlag.Line)
	],
	"elise": [                           
		Spell("elisehumane",           ["elisehumane"], 			SFlag.SkillshotLine)
	],
	"kennen": [                           
		Spell("kennenshurikenhurlmissile1",           ["kennenshurikenhurlmissile1"], 			SFlag.SkillshotLine)
	],
	"darius": [                           
		Spell("dariuscleave",           [],	SFlag.Area | SFlag.CollideWindwall),
		Spell("dariusaxegrabcone",      ["dariusaxegrabcone"], SFlag.Cone | SFlag.CollideWindwall)
	],
	"brand": [
		Spell("brandq",                 ["brandqmissile"],                         SFlag.SkillshotLine),
		Spell("brandw",                 [],                                        SFlag.Area | SFlag.CollideWindwall),
		Spell("brand_.+_w.+tar_red",                 [],                                        SFlag.Area | SFlag.CollideWindwall)
	],
	"pyke": [
		Spell("pykeqrange",                 ["pykeqrange"],                         SFlag.SkillshotLine),
		Spell("pykee",                 ["pykee"],                                        SFlag.SkillshotLine),
		Spell("pykessr",                 [],                                        SFlag.SkillshotLine),
	],
	"amumu": [
		Spell("bandagetoss",                 ["sadmummybandagetoss"],                         SFlag.SkillshotLine),
		Spell("curseofthesadmummy",                 [],                                        SFlag.Area)
	],
	"caitlyn": [
		Spell("caitlynpiltoverpeacemaker", ["caitlynpiltoverpeacemaker", "caitlynpiltoverpeacemaker2"],          SFlag.Line | SFlag.CollideWindwall),
		Spell("caitlynyordletrap",         [],                                                                   SFlag.Area),
		Spell("caitlynentrapment",         ["caitlynentrapmentmissile"],                                         SFlag.SkillshotLine)
	],
	"chogath": [                        
		Spell("rupture",                [],                                        SFlag.Area, delay = 0.627),
		Spell("feralscream",            [],                                        SFlag.Cone | SFlag.CollideWindwall)
	],
	"drmundo": [
		Spell("infectedcleavermissilecast", ["infectedcleavermissile"],            SFlag.SkillshotLine)
	],
	"diana": [
		Spell("dianaq",                 ["dianaqinnermissile", "dianaqoutermissile"], 	SFlag.Cone),
		Spell("dianaarcarc",                 ["dianaarcarc"], 	SFlag.Cone)
	],
	"ekko": [
		Spell("ekkoq",                  ["ekkoqmis"],                              SFlag.Line | SFlag.CollideChampion),
		Spell("ekkow",                  ["ekkowmis"],                              SFlag.Area, delay=0.0, danger=3),
		Spell("ekkor",                  ["ekkor"],                              SFlag.Area, delay=0.0, danger=3)
	],
	"kogmaw": [
		Spell("kogmawq",                  ["kogmawq"],                              SFlag.SkillshotLine | SFlag.CollideChampion),
		Spell("kogmawvoidooze",                  ["kogmawvoidoozemissile"],                              SFlag.SkillshotLine | SFlag.CollideChampion),
		Spell("kogmawlivingartillery",                  ["kogmawlivingartillery"],                              SFlag.Area)
	],
	"fizz": [
		Spell("fizzr",                  ["fizzrmissile"],                          SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall, delay=0.0, danger=3)
	],
	"irelia": [
		Spell("ireliae",                ["ireliaemissile"],                        SFlag.Area),
		Spell("ireliar",                ["ireliar"],                               SFlag.SkillshotLine, delay=0.0, danger=3)
	],
	"illaoi": [
		Spell("illaoiq",                [],                                        SFlag.Area),
		Spell("illaoie",                ["illaoiemis"],                            SFlag.SkillshotLine)
	],
	"jarvaniv": [
		Spell("jarvanivdragonstrike",                [],                        SFlag.SkillshotLine),
		Spell("jarvaniveq", [],                                       SFlag.SkillshotLine),
		Spell("jarvanivdemacianstandard", [],                                       SFlag.Area)
	],
	"janna": [
		Spell("jannaq",                ["howlinggalespell"],                        SFlag.SkillshotLine)
	],
	"khazix": [
		Spell("khazixw",                ["khazixwmissile"],                        SFlag.SkillshotLine),
		Spell("khazixwlong",            ["khazixwmissile"],                        SFlag.SkillshotLine)
	],
	"ezreal": [                         
		Spell("ezrealq",                ["ezrealq"],                               SFlag.Line),
		Spell("ezrealw",                ["ezrealw"],                               SFlag.Line),
		Spell("ezrealr",                ["ezrealr"],                               SFlag.Line, delay=0.0, danger=2)
	],
	"kalista": [                         
		Spell("kalistamysticshot",                ["kalistamysticshotmis"],                               SFlag.SkillshotLine),
	],
	"lissandra": [                         
		Spell("lissandraq",                ["lissandraqmissile"],                               SFlag.SkillshotLine),
		Spell("lissandraqshards",                ["lissandraqshards"],                               SFlag.SkillshotLine),
		Spell("lissandrae",                ["lissandraemissile"],                               SFlag.SkillshotLine),
	],
	"galio": [
		Spell("galioq", 					[], 							SFlag.Area),
		Spell("galioe", 					[], 							SFlag.SkillshotLine)
	],
	"evelynn": [
		Spell("evelynnq",               ["evelynnq"],                              SFlag.SkillshotLine),
		Spell("evelynnr",               ["evelynnr"],                              SFlag.Cone)
	],
	"graves": [                         
		Spell("gravesqlinespell",       ["gravesqlinemis", "gravesqreturn"],       SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall),
		Spell("gravessmokegrenade",     ["gravessmokegrenadeboom"],                SFlag.Area | SFlag.CollideWindwall),
		Spell("graveschargeshot",       ["graveschargeshotshot"],                  SFlag.Line | SFlag.CollideWindwall),
		Spell("graveschargeshotfxmissile2",       ["graveschargeshotfxmissile2"],                  SFlag.Cone)
	],
	"twistedfate": [                    
		Spell("wildcards",              ["sealfatemissile"],                       SFlag.Cone)
	],
	"leesin": [                         
		Spell("blindmonkqone",          ["blindmonkqone"],                         SFlag.SkillshotLine)
	],
	"leona": [
		Spell("leonazenithblade",       ["leonazenithblademissile"],               SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall),
		Spell("leonasolarflare",        [],                                        SFlag.Area)
	],
	"leblanc": [
		Spell("leblancw",               [],                                        SFlag.Area),
		Spell("leblancrw",              [],                                        SFlag.Area),
		Spell("leblance",               ["leblancemissile"],                       SFlag.SkillshotLine),
		Spell("leblancre",              ["leblancremissile"],                      SFlag.SkillshotLine)
	],
	"lucian": [
		Spell("lucianq",                ["lucianq"],                          SFlag.SkillshotLine, delay=0.4),
		Spell("lucianw",                ["lucianwmissile"],                          SFlag.SkillshotLine)
	],
	"gragas": [
		Spell("gragasq",                ["gragasqmissile"],                          SFlag.Area),
		Spell("gragase",                ["gragase"],                          SFlag.SkillshotLine),
		Spell("gragasr",                [],                          SFlag.Area, delay=0.0, danger=3),
		Spell("gragasrfow",                ["gragasrboom"],                          SFlag.Area)
	],
	"tristana": [
		Spell("tristanaw",                ["rocketjump"],                          SFlag.Area | SFlag.CollideWindwall)
	],
	"rengar": [
		Spell("rengare",                ["rengaremis"],                            SFlag.SkillshotLine),
		Spell("rengareemp",             ["rengareempmis"],                         SFlag.SkillshotLine),
	],
	"ryze": [
		Spell("ryzeq",           ["ryzeq"],                                 SFlag.SkillshotLine)
	],
	"blitzcrank": [
		Spell("rocketgrab",           ["rocketgrabmissile"],                                 SFlag.SkillshotLine),
	],
	"corki": [
		Spell("phosphorusbomb",           ["phosphorusbombmissile"],                                 SFlag.Area),
		Spell("missilebarrage",           ["missilebarragemissile"],                                 SFlag.SkillshotLine),
		Spell("missilebarrage2",           ["missilebarragemissile2"],                                 SFlag.SkillshotLine),
	],
	"varus": [
		Spell("varusq",                 ["varusqmissile"],                         SFlag.Line | SFlag.CollideWindwall),
		Spell("varuse",                 ["varusemissile"],                         SFlag.Area),
		Spell("varusr",                 ["varusrmissile"],                         SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall, delay=0.0, danger=3)
	],
	"veigar": [                         
		Spell("veigarbalefulstrike",    ["veigarbalefulstrikemis"],                SFlag.SkillshotLine),
		Spell("veigardarkmatter",       [],                                        SFlag.Area),
		Spell("veigareventhorizon",     [],                                        SFlag.Area)
	],
	"velkoz": [
		Spell("velkozq",                 ["velkozqmissile"],                         SFlag.Line | SFlag.CollideWindwall),
		Spell("velkozqsplit",                 ["velkozqmissilesplit"],                         SFlag.Line | SFlag.CollideWindwall),
		Spell("velkozqsplitactivate",                 ["velkozqmissilesplit"],                         SFlag.Line | SFlag.CollideWindwall),
		Spell("velkozw", 								["VelkozWMissile"], 				SFlag.Line | SFlag.CollideWindwall			),
		Spell("velkoze",                 					["velkozemissile"],                         SFlag.Area)
	],
	"lux": [                            
		Spell("luxlightbinding",        ["luxlightbindingmis"],                    SFlag.SkillshotLine),
		Spell("luxlightstrikekugel",    ["luxlightstrikekugel"],                   SFlag.Area),
		Spell("luxmalicecannonmis",        ["luxrvfxmis"],                       SFlag.CollideGeneric),
	],
	"nautilus": [                            
		Spell("nautilusanchordragmissile",        ["nautilusanchordragmissile"],                    SFlag.SkillshotLine)
	],
	"malzahar": [                            
		Spell("malzaharq",        ["malzaharq"],                    SFlag.SkillshotLine)
	],
	"ziggs": [                          
		Spell("ziggsq",                  ["ziggsqspell", "ziggsqspell2", "ziggsqspell3"],                              SFlag.Area | SFlag.CollideWindwall),
		Spell("ziggsw",                 ["ziggsw"],                                                                   SFlag.Area | SFlag.CollideWindwall),
		Spell("ziggse",                 ["ziggse2"],                                                                  SFlag.Area | SFlag.CollideWindwall),
		Spell("ziggsr",                 ["ziggsrboom", "ziggsrboommedium", "ziggsrboomlong", "ziggsrboomextralong"],  SFlag.Area),
	],
	"jhin": [                           
		Spell("jhinw",                  ["jhinwmissile"],                                 SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall, delay=0.5),
		Spell("jhine",                  ["jhinetrap"],                             SFlag.Area | SFlag.CollideWindwall),
		Spell("jhinrshot",              ["jhinrshotmis", "jhinrshotmis4"],         SFlag.Line | SFlag.CollideWindwall | SFlag.CollideChampion)
	],
	"swain": [                           
		Spell("swainw",                  [],                                 SFlag.Area),
		Spell("swaine",                  ["swaine"],                             SFlag.SkillshotLine),
		Spell("swainereturn",              ["swainereturnmissile"],         SFlag.SkillshotLine)
	],
	"nasus": [
		Spell("nasuse",                 [],                                        SFlag.Area)
	],
	"nami": [
		Spell("namiq",                  ["namiqmissile"],                          SFlag.Area),
		Spell("namir",                  ["namirmissile"],                          SFlag.Line | SFlag.CollideWindwall)
	],
	"nidalee": [
		Spell("javelintoss",            ["javelintoss"],                           SFlag.SkillshotLine),
		Spell("bushwhack",              [],                                        SFlag.Area)
	],
	"malphite": [
		Spell("ufslash",                [],                                        SFlag.Cone)
	],
	"reksai": [
		Spell("reksaiqburrowed",                ["reksaiqburrowedmis"],                                        SFlag.SkillshotLine)
	],
	"thresh": [
		Spell("threshq",                ["threshqmissile"],                        SFlag.SkillshotLine)
	],
	"morgana": [                        
		Spell("morganaq",               ["morganaq"],                              SFlag.SkillshotLine),
		Spell("morganaw",               [],                       SFlag.Area, delay=0.95)
	],
	"mordekaiser": [                        
		Spell("mordekaiserq",               [],                              SFlag.SkillshotLine),
		Spell("mordekaisere",               [],                       SFlag.SkillshotLine)
	],
	"missfortune": [                        
		Spell("missfortunericochetshot",               ["missfortunericochetshot"],                              SFlag.Cone)
	],
	"samira": [                        
		Spell("samiraqgun",               ["samiraqgun"],                              SFlag.SkillshotLine),
	],
	"pantheon": [
		Spell("pantheonq",              ["pantheonqmissile"],                      SFlag.Line | SFlag.CollideWindwall),
		Spell("pantheonr",              ["pantheonrmissile"],                      SFlag.Area)
	],
	"annie": [                                                                     
		Spell("anniew",                 [],                                        SFlag.Cone | SFlag.CollideWindwall),
		Spell("annier",                 [],                                        SFlag.Area)
	],
	"hecarim": [                                                                     
		Spell("hecarimr",                 ["hecarimultmissile"],                                        SFlag.SkillshotLine),
		Spell("hecarimrcircle",                 [],                                        SFlag.Area)
	],
	"olaf": [
		Spell("olafaxethrowcast",       ["olafaxethrow"],                          SFlag.Line | SFlag.CollideWindwall)
	],
	"anivia": [
		Spell("flashfrost",             ["flashfrostspell"],                       SFlag.Line | SFlag.CollideWindwall),
		Spell("aniviar",            [],                                        SFlag.Area, delay=0.25),
		Spell("aniviar2",           [],                                        SFlag.Area)
	],
	"zed": [
		Spell("zedq",       ["zedqmissile"],                          SFlag.Line)
	],
	"xerath": [
		Spell("xeratharcanopulse",             [],                       SFlag.SkillshotLine),
		Spell("xeratharcanebarrage2",            ["xeratharcanebarrage2"],                                        SFlag.Area),
		Spell("xerathmagespear",           ["xerathmagespearmissile"],                                        SFlag.SkillshotLine),
		Spell("xerathrmissilewrapper",           ["xerathlocuspulse"],                                        SFlag.Area),
	],
	"urgot": [
		Spell("urgotq",                 ["urgotqmissile"],                         SFlag.Area | SFlag.CollideWindwall, delay = 0.2),
		Spell("urgotr",                 ["urgotr"],                                SFlag.Line | SFlag.CollideWindwall | SFlag.CollideChampion)
	],
	"senna": [
		Spell("sennaqcast",             ["sennaqcast"],                                SFlag.SkillshotLine),
		Spell("sennaw",                 ["sennaw"],                                SFlag.SkillshotLine),
		Spell("sennar",                 ["sennar"],                                SFlag.Line)
	],
	"shyvana": [
		Spell("shyvanafireball",        ["shyvanafireballmissile"],                SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall),
		Spell("shyvanafireballdragon2", ["shyvanafireballdragonmissile"],          SFlag.Line | SFlag.Area | SFlag.CollideChampion | SFlag.CollideWindwall)
	],
	"singed": [
		Spell("megaadhesive",           ["singedwparticlemissile"],                SFlag.Area)
	],
	"sivir": [
		Spell("sivirq",                 ["sivirqmissile"],                         SFlag.Cone)
	],
	"kaisa": [
		Spell("kaisaw",                 ["kaisaw"],                         SFlag.Line | SFlag.CollideWindwall)
	],
	"karma": [
		Spell("karmaq",                 ["karmaqmissile"],                         SFlag.Line | SFlag.CollideWindwall),
		Spell("karmaqmantracircle",                 [],                         SFlag.Line | SFlag.CollideWindwall)
	],
	"braum": [
		Spell("braumq",                 ["braumqmissile"],                         SFlag.SkillshotLine),
		Spell("braumrwrapper",                 ["braumrmissile"],                         SFlag.SkillshotLine)
	],
	"soraka": [
		Spell("sorakaq",                ["sorakaqmissile"],                        SFlag.Area),
		Spell("sorakae",                [],                                        SFlag.Area)
	],
	"rakan": [
		Spell("rakanq",                ["rakanqmis"],                        SFlag.SkillshotLine),
		Spell("rakanw",                [],                                        SFlag.Area, delay=0.5)
	],
	"xayah": [
		Spell("xayahq",                ["xayahqmissile1", "xayahqmissile2"],      SFlag.SkillshotLine)
	],
	"sona": [
		Spell("sonar",                  ["sonar"],                                 SFlag.Line | SFlag.CollideWindwall)
	],
	"akali": [
		Spell("akalie",                  ["akaliemis"],                                 SFlag.Line | SFlag.CollideWindwall)
	],
	"kayle": [
		Spell("kayleq",                 ["kayleqmis"],                             SFlag.SkillshotLine)
	],
	"yasuo": [
		Spell("yasuoq",                  [],                             SFlag.Line | SFlag.CollideWindwall),
		Spell("yasuoq2",                 [],                             SFlag.Line | SFlag.CollideWindwall),
		Spell("yasuoq3",                 ["yasuoq3mis"],                             SFlag.SkillshotLine)
	],
	"yone": [
		Spell("yoneq",                 [],                             SFlag.SkillshotLine),
		Spell("yoneq3",                 [],                             SFlag.SkillshotLine),
		Spell("yoner",                 [],                             SFlag.SkillshotLine)
	],
	"zac": [
		Spell("zacq",                   ["zacqmissile"],                           SFlag.SkillshotLine),
		Spell("zace",                   [],                                        SFlag.Area)
	],
	"zyra": [
		Spell("zyraq",                  ["zyraq"],                                        SFlag.SkillshotLine),
		Spell("zyraw",                  [],                                        SFlag.Area),
		Spell("zyrae",                  ["zyrae"],                                 SFlag.SkillshotLine),
		Spell("zyrar",                  ["zyrar"],                                         SFlag.Area | SFlag.CollideChampion | SFlag.CollideWindwall),
		Spell("zyrapassivedeathmanager",                  ["zyrapassivedeathmanager"],                                        SFlag.SkillshotLine)
	],
	"zilean": [
		Spell("zileanq",                ["zileanqmissile"],                        SFlag.Area | SFlag.CollideWindwall)
	],
	"orianna": [
		Spell("orianaizunacommand",     ["orianaizuna"],                           SFlag.Line | SFlag.Area | SFlag.CollideWindwall)
	],
	"warwick": [
		Spell("warwickr",               [],                                        SFlag.Area | SFlag.CollideChampion),
		Spell("warwickrchannel",               [],                                        SFlag.Area | SFlag.CollideChampion)
	],
	"taric": [
		Spell("tarice", 			["tarice"], 			SFlag.SkillshotLine, delay=0.1)
	],
	"viego": [
		Spell("viegoq", 			[], 			SFlag.SkillshotLine, delay=0.4),
		Spell("viegowcast", ["viegowmis"], SFlag.SkillshotLine),
		Spell("viegorr", [], SFlag.Area)
	],
	"syndra": [
		Spell("syndraq", 			["syndraqspell"], 			SFlag.Area),
		Spell("syndrae5", 			["syndrae5"], 			SFlag.Area),
		Spell("syndraqe", 			["syndrae"], 			SFlag.Area)
	],
	"draven": [
		Spell("dravendoubleshot", 			["dravendoubleshotmissile"], 			SFlag.SkillshotLine),
		Spell("dravenrcast", 			["dravenr"], 			SFlag.SkillshotLine)
	],
	"kayn": [
		Spell("kaynw", 			[], 			SFlag.SkillshotLine),
		Spell("kaynassw", 			[], 			SFlag.SkillshotLine),
	],
	"jinx": [
		Spell("jinxw", 			["jinxw"], 			SFlag.SkillshotLine),
		Spell("jinxwmissile", 			["jinxwmissile"], 			SFlag.SkillshotLine),
		Spell("jinxr", 			["jinxr"], 			SFlag.SkillshotLine)
	],
	"cassiopeia": [
		Spell("cassiopeiaq", 			["cassiopeiaq"], 			SFlag.Area),
		Spell("cassiopeir", 			["cassiopeiar"], 			SFlag.Cone),
	],
	"seraphine": [
		Spell("seraphineq", 			["seraphineqinitialmissile"], 			SFlag.Area | SFlag.CollideWindwall),
		Spell("seraphineecast", 			["seraphineemissile"], 			SFlag.SkillshotLine),
		Spell("seraphiner", 			["seraphiner"], 			SFlag.SkillshotLine | SFlag.CollideWindwall),
		Spell("seraphinerfow", 			[], 			SFlag.SkillshotLine | SFlag.CollideWindwall),
	],
	"lulu": [
		Spell("luluq", 			["luluqmissile"], 			SFlag.SkillshotLine),
		Spell("luluqpix", 			["luluqmissiletwo"], 			SFlag.SkillshotLine)
	],
	"neeko": [
		Spell("neekoq", 			["neekoq"], 			SFlag.Area),
		Spell("neekoe", 			["neekoe"], 			SFlag.Line | SFlag.CollideWindwall)
	],
	"allchampions": [
		Spell("6656cast", 			[], 			SFlag.SkillshotLine)
	],
	"lillia": [
		Spell("lilliaw", 			[], 			SFlag.Area | SFlag.CollideWindwall),
		Spell("lilliae", 			["lilliae"], 			SFlag.SkillshotLine),
		Spell("lilliae2", 			["lilliaerollingmissile"], 			SFlag.SkillshotLine)
	],
	"tahmkench": [
		Spell("tahmkenchq", 			["tahmkenchqmissile"], 			SFlag.SkillshotLine)
	]
}

def draw_prediction_info(game, ui):
	global ChampionSpells, Version
	
	ui.separator()
	ui.text("Using LPrediction " + Version, Color.PURPLE)
	if is_champ_supported(game.player):
		ui.text(game.player.name.upper() + " has skillshot prediction support", Color.GREEN)
	else:
		ui.text(game.player.name.upper() + " doesnt have skillshot prediction support", Color.RED)
	
	if ui.treenode(f'Supported Champions ({len(ChampionSpells)})'):
		for champ, spells in sorted(ChampionSpells.items()):
			ui.text(f"{champ.upper()} {' '*(20 - len(champ))}: {str([spell.name for spell in spells])}")
			
		ui.treepop()

def get_skillshot_range(game, skill_name):
	global Spells
	if skill_name not in Spells:
		raise Exception("Not a skillshot")
	
	# Get the range of the missile if it has a missile
	skillshot = Spells[skill_name]
	if len(skillshot.missiles) > 0:
		return game.get_spell_info(skillshot.missiles[0]).cast_range
		
	# If it doesnt have a missile get simply the cast_range from the skill
	info = game.get_spell_info(skill_name)
	return info.cast_range*2.0 if is_skillshot_cone(skill_name) else info.cast_range

def is_skillshot(skill_name):
	global Spells, MissileToSpell
	return skill_name in Spells or skill_name in MissileToSpell
	
def get_missile_parent_spell(missile_name):
	global MissileToSpell
	return MissileToSpell.get(missile_name, None)
	
def is_champ_supported(champ):
	global ChampionSpells
	return champ.name in ChampionSpells
	
def is_skillshot_cone(skill_name):
	if skill_name not in Spells:
		return False
	return Spells[skill_name].flags & SFlag.Cone
	
def is_last_hitable(game, player, enemy):
	missile_speed = player.basic_missile_speed + 1
		
	hit_dmg = items.get_onhit_physical(player, enemy) + items.get_onhit_magical(player, enemy)
	
	hp = enemy.health
	atk_speed = player.base_atk_speed * player.atk_speed_multi
	t_until_basic_hits = game.distance(player, enemy)/missile_speed#(missile_speed*atk_speed/player.base_atk_speed)

	for missile in game.missiles:
		if missile.dest_id == enemy.id:
			src = game.get_obj_by_id(missile.src_id)
			if src:
				t_until_missile_hits = game.distance(missile, enemy)/(missile.speed + 1)
			
				if t_until_missile_hits < t_until_basic_hits:
					hp -= src.base_atk

	return hp - hit_dmg <= 0
	
def castpoint_for_collision(game, spell, caster, target):
	global Spells

	if spell.name not in Spells:
		return None
	
	# Get extra data for spell that isnt provided by lview
	spell_extra = Spells[spell.name]
	if len(spell_extra.missiles) > 0:
		missile = game.get_spell_info(spell_extra.missiles[0])
	else:
		missile = spell
		
	t_delay = spell.delay + spell_extra.delay
	if missile.travel_time > 0.0:
		t_missile = missile.travel_time
	else:
		t_missile = (missile.cast_range / missile.speed) if len(spell_extra.missiles) > 0 and missile.speed > 0.0 else 0.0		
	# Get direction of target
	target_dir = target.pos.sub(target.prev_pos).normalize()
	if math.isnan(target_dir.x):
		target_dir.x = 0.0
	if math.isnan(target_dir.y):
		target_dir.y = 0.0
	if math.isnan(target_dir.z):
		target_dir.z = 0.0
	#print(f'{target_dir.x} {target_dir.y} {target_dir.z}')

	# If the spell is a line we simulate the main missile to get the collision point
	if spell_extra.flags & SFlag.Line:
		
		iterations = int(missile.cast_range/30.0)
		step = t_missile/iterations
		

		last_dist = 99999999
		last_target_pos = target.pos
		for i in range(iterations):
			t = i*step
			target_future_pos = target.pos.add(target_dir.scale((t_delay + t)*target.movement_speed))
			spell_dir = target_future_pos.sub(caster.pos).normalize().scale(t*missile.speed)
			spell_future_pos = caster.pos.add(spell_dir)
			dist = target_future_pos.distance(spell_future_pos)
			if dist < missile.width / 2.0:
				return target_future_pos
			elif dist > last_dist:
				return last_target_pos
			else:
				last_dist = dist
				last_target_pos = target_future_pos
				
		return None
		
	# If the spell is an area spell we return the position of the player when the spell procs
	elif spell_extra.flags & SFlag.Area:
		return target.pos.add(target_dir.scale((t_delay + t_missile)*target.movement_speed))
	else:
		return target.pos

def getEvadePos(game, start_pos, end_pos, current, br, missile, spell):
	# spell_extra = Spells[spell.name]
	# if len(spell_extra.missiles) > 0:
	# 	missile = game.get_spell_info(spell_extra.missiles[0])
	# else:
	# 	missile = spell

	# t_delay = spell.delay + spell_extra.delay
	# if missile.travel_time > 0.0:
	# 	t_missile = missile.travel_time
	# else:
	# 	t_missile = (missile.cast_range / missile.speed) if len(spell_extra.missiles) > 0 and missile.speed > 0.0 else 0.0		
	
	
	direction = end_pos.sub(start_pos)
	pos3 = end_pos.add(Vec3(direction.z * -float(1.0), direction.y, direction.x * float(1.0)))
	pos4 = end_pos.add(Vec3(direction.z * float(1.0), direction.y, direction.x * -float(1.0)))
	
	direction2 = pos3.sub(pos4)
	direction2 = game.clamp2d(direction2, br)
	direction3 = Vec3(0, 0, 0)
	
	direction3.x = -direction2.x 
	direction3.y = -direction2.y
	direction3.z = -direction2.z
	
	# player_dir = game.player.pos.sub(game.player.prev_pos).normalize()
	# if math.isnan(player_dir.x):
	# 	player_dir.x = 0.0
	# if math.isnan(player_dir.y):
	# 	player_dir.y = 0.0
	# if math.isnan(player_dir.z):
	# 	player_dir.z = 0.0
	
	# iterations = int(missile.cast_range/30.0)
	# step = t_missile/iterations

	# for i in range(iterations):
	# 	t = i*step
	# 	if game.is_left(game.world_to_screen(start_pos), game.world_to_screen(end_pos), game.world_to_screen(current)):
	# 		return current.add(direction3.add(player_dir.scale((t_delay + t)*game.player.movement_speed)))
	# 	else:
	# 		return current.add(direction2.add(player_dir.scale((t_delay + t)*game.player.movement_speed)))
	if game.is_left(game.world_to_screen(start_pos), game.world_to_screen(end_pos), game.world_to_screen(current)):
		return current.add(direction3)
	else:
		return current.add(direction2)