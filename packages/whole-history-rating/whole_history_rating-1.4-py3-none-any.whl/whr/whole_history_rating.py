from whr.player import Player
from whr.playerday import PlayerDay
from whr.game import Game
from collections import defaultdict
import time
import math
import ast
import pickle
class UnstableRatingException(Exception):
	pass

class Base:

	def __init__(self, config=None):
		if config is None:
			self.config = defaultdict(lambda: None)
		else:
			self.config = config
			if self.config.get("debug") is None:
				self.config["debug"] = False
		if self.config.get("w2") is None:
			self.config["w2"] = 300.0
		if self.config.get("uncased") is None:
			self.config["uncased"] = False 
		self.games = []
		self.players = {}

	def print_ordered_ratings(self, current=False):
		"""displays all ratings for each player (for each of his playing days) ordered

		Args:
		    current (bool, optional): True to let only the last estimation of the elo, False gets all estimation for each day played
		"""
		players = [x for x in self.players.values() if len(x.days) > 0]
		players.sort(key=lambda x: x.days[-1].gamma())
		for p in players:
			if len(p.days) > 0:
				if current:
					print(f"{p.name} => {p.days[-1].elo()}")
				else:
					print(f"{p.name} => {[x.elo() for x in p.days]}")

	def get_ordered_ratings(self, current=False, compact=False):
		"""gets all ratings for each player (for each of his playing days) ordered
		
		Returns:
		    list[list[float]]: for each player and each of his playing day, the corresponding elo
		
		Args:
		    current (bool, optional): True to let only the last estimation of the elo, False gets all estimation for each day played
		    compact (bool, optional): True to get only a list of elos, False to get the name before
		"""
		result = []
		players = [x for x in self.players.values() if len(x.days) > 0]
		players.sort(key=lambda x: x.days[-1].gamma())
		for p in players:
			if len(p.days) > 0:
				if current and compact:
					result.append(p.days[-1].elo())
				elif current:
					result.append((p.name, p.days[-1].elo()))
				elif compact:
					result.append([x.elo() for x in p.days])
				else:
					result.append((p.name,[x.elo() for x in p.days]))
		return result

	def log_likelihood(self):
		"""gets the likelihood of the current state
		
		the more iteration you do the higher the likelihood becomes
		
		Returns:
		    float: the likelihood
		"""
		score = 0.0
		for p in self.players.values():
			if len(p.days) > 0:
				score += p.log_likelihood()
		return score

	def player_by_name(self, name):
		"""gets the player object corresponding to the name
		
		Args:
		    name (str): the name of the player
		
		Returns:
		    Player: the corresponding player
		"""
		if self.config["uncased"]:
			name = name.lower()
		if self.players.get(name, None) is None:
			self.players[name] = Player(name, self.config)
		return self.players[name]

	def ratings_for_player(self, name, current = False):
		"""gets all rating for each day played for the player
		
		Args:
		    name (str): the player's name
		    current (bool, optional): True to let only the last estimation of the elo and uncertainty, False gets all estimation for each day played
		
		Returns:
		    list[list[int, float, float]]: for each day, the time_step the elo the uncertainty
		"""
		if self.config["uncased"]:
			name = name.lower()
		player = self.player_by_name(name)
		if current:
			return (round(player.days[-1].elo()), round(player.days[-1].uncertainty*100))
		else:
			return [[d.day, round(d.elo()), round(d.uncertainty*100)] for d in player.days]

	def _setup_game(self, black, white, winner, time_step, handicap, extras={}):
		if black == white:
			raise(AttributeError("Invalid game (black player == white player)"))
			return None
		white_player = self.player_by_name(white)
		black_player = self.player_by_name(black)
		game = Game(black_player, white_player, winner, time_step, handicap, extras)
		return game

	def create_game(self, black, white, winner, time_step, handicap, extras={}):
		"""creates a new game to be added to the base
		
		Args:
		    black (str): the black name
		    white (str): the white name
		    winner (str): "B" if black won, "W" if white won
		    time_step (int): the day of the match from origin
		    handicap (float): the handicap (in elo)
		    extras (dict, optional): extra parameters
		
		Returns:
		    Game: the added game
		"""
		if self.config["uncased"]:
			black = black.lower()
			white = white.lower()
		game = self._setup_game(black, white, winner, time_step, handicap, extras)
		return self._add_game(game)

	def _add_game(self, game):
		game.white_player.add_game(game)
		game.black_player.add_game(game)
		if game.bpd is None:
			print("Bad game")
		self.games.append(game)
		return game

	def iterate(self, count):
		"""do a number of "count" iterations of the algorithm
		
		Args:
		    count (int): the number of iterations desired
		"""
		for _ in range(count):
			self._run_one_iteration()
		for name, player in self.players.items():
			player.update_uncertainty()

	def auto_iterate(self, time_limit=10, precision=10E-3):
		"""iterates automatically until it converges or reaches the time limit
		iterates iteratively ten by ten
		
		Args:
		    time_limit (int, optional): the maximal time after which no more iteration are launched
		    precision (float, optional): the precision of the stability desired
		
		Returns:
		    tuple(int, bool): the number of iterations and True if it has reached stability, False otherwise
		"""
		start = time.time()
		self.iterate(10)
		a = self.get_ordered_ratings(compact=True)
		i = 10
		while True:
			self.iterate(10)
			i += 10
			b = self.get_ordered_ratings(compact=True)
			if self._test_stability(a,b, precision):
				return i, True
			if time.time() - start > time_limit:
				return i, False
			a = b

	def _test_stability(self, v1, v2, precision=10E-3):
		"""tests if two lists of lists of floats are equal but a certain precision
		
		Args:
		    v1 (list[list[float]]): first list containing ints
		    v2 (list[list[float]]): second list containing ints
		    precision (float, optional): the precision after which v1 and v2 are not equal
		
		Returns:
		    bool: True if the two lists are close enought, False otherwise
		"""
		v1 = [x for y in v1 for x in y]
		v2 = [x for y in v2 for x in y]
		for x1,x2 in zip(v1,v2):
			if abs(x2-x1) > precision:
				return False
		return True

	def probability_future_match(self, name1, name2, handicap=0, extras={}):
		"""gets the probability of winning for an hypothetical match against name1 and name2
		
		displays the probability of winning for name1 and name2 in percent rounded to the second decimal
		
		Args:
		    name1 (str): name1's name
		    name2 (str): name2's name
		    handicap (int, optional): the handicap (in elo)
		    extras (dict, optional): extra parameters
		
		Returns:
		    tuple(int, int): the probability between 0 and 1 for name1 first then name2
		"""
		# Avoid self-played games (no info)
		if self.config["uncased"]:
			name1 = name1.lower()
			name2 = name2.lower()
		if name1 == name2:
			raise(AttributeError("Invalid game (black == white)"))
			return None
		player1 = self.player_by_name(name1)
		player2 = self.player_by_name(name2)
		bpd_gamma = 1
		bpd_elo = (math.log(1) * 400) / (math.log(10))
		wpd_gamma = 1
		wpd_elo= (math.log(1) * 400) / (math.log(10))
		if len(player1.days) > 0:
			bpd = player1.days[-1]
			bpd_gamma = bpd.gamma()
			bpd_elo = bpd.elo()
		if len(player2.days) != 0:
			wpd = player2.days[-1]
			wpd_gamma=wpd.gamma()
			wpd_elo = wpd.elo()
		player1_proba = bpd_gamma/(bpd_gamma + 10**((wpd_elo - handicap)/400.0))
		player2_proba = wpd_gamma/(wpd_gamma + 10**((bpd_elo + handicap)/400.0))
		print(f"win probability: {name1}:{player1_proba:.2f}%; {name2}:{player2_proba:.2f}%")
		return player1_proba, player2_proba


	def _run_one_iteration(self):
		"""runs one iteration of the whr algorithm
		"""
		for name,player in self.players.items():
			player.run_one_newton_iteration()

	def load_games(self, games, separator=' '):
		"""loads all games at once
		
		given a string representing the path of a file or a list of string representing all games,
		this function loads all games in the base
		all match must comply to this format:
			"black_name white_name winner time_step handicap extras"
			black_name (required)
			white_name (required)
			winner is B or W (required)
			time_step (required)
			handicap (optional: default 0)
			extras is a dict (optional)
		
		Args:
		    games (str|list[str]): a path or a list of string representing games
		    separator (str, optional): the separator between all elements of a game, space by default (every element will be trim eventually)
		"""
		data = None
		if isinstance(games, str):
			with open(games, 'r') as f:
				data = f.readlines()
		else:
			data = games
		for line in data:
			handicap = 0
			extras = None
			arguments = [x.strip() for x in line.split(separator)]
			is_correct = False
			if len(arguments) == 6:
				try:
					black, white, winner, time_step, handicap, extras = arguments
					extras = last = ast.literal_eval(extras)
					if isinstance(extras,dict):
						is_correct = True
				except Exception as e:
					raise(AttributeError(f"the extras argument couldn't be evaluated as a dict: {extras}\n{e}"))
			if len(arguments) == 5:
				black, white, winner, time_step, last = arguments
				try:
					eval_last = ast.literal_eval(last)
					if isinstance(eval_last,dict):
						extras = eval_last
						is_correct = True
					elif isinstance(eval_last,int):
						handicap = eval_last
						is_correct = True
				except Exception as e:
					raise(AttributeError(f"the last argument couldn't be evaluated as an int or a dict: {last}\n{e}"))
			if len(arguments) == 4:
				black, white, winner, time_step = arguments
				is_correct = True
			if not is_correct:
				raise(AttributeError(f"loaded game must have this format: 'black_name white_name winner time_step handicap extras' with handicap (int or dict) and extras (dict) optional. the handicap|extras argument is: {last}"))
			time_step, handicap = int(time_step), int(handicap)
			if self.config["uncased"]:
				black = black.lower()
				white = white.lower()
			self.create_game(black, white, winner, time_step, handicap, extras=extras)

	def save_base(self, path):
		"""saves the current state of the base to a file at "path"
		
		Args:
		    path (str): the path where to save the base
		"""
		pickle.dump([self.players,self.games,self.config["w2"]], open(path, 'wb'))

	@staticmethod
	def load_base(path):
		"""loads a saved base
		
		Args:
		    path (str): the path to the saved base
		
		Returns:
		    Base: the loaded base
		"""
		players, games, config = pickle.load(open(path, 'rb'))
		result = Base()
		result.config["w2"], result.games, result.players = config, games, players
		return result



if __name__ == "__main__":
	print("test creating the base with modified w2 and uncased")
	whr = Base(config={"w2":14, "uncased":True})
	print("Done")
	print("-------------------------------------------------------")
	print("test creating one game")
	whr.create_game("shusaku", "shusai", "B", 4, 0)
	print("Done")
	print("-------------------------------------------------------")
	print("test creating one game with winner uncased (b instead of B)")
	whr.create_game("shusaku", "shusai", "w", 5, 0)
	print("Done")
	print("-------------------------------------------------------")
	print("test creating one game with cased letters (ShUsAkU instead of shusaku and ShUsAi instead of shusai)")
	game = whr.create_game("ShUsAkU", "ShUsAi", "W", 6, 0)
	print("Done")
	print("-------------------------------------------------------")
	print("test loading several games at once")
	games = ["shusaku; shusai; B; 1", "shusaku;shusai;W;2;0", " shusaku ; shusai ;W ; 3; {'w2':300}", "shusaku;nobody;B;3;0;{'w2':300}"]
	whr.load_games(games, separator=";")
	print("Done")
	print("-------------------------------------------------------")
	print("test auto iterating to get convergence")
	print(whr.auto_iterate())
	print("Done")
	print("-------------------------------------------------------")
	print("test getting ratings for player shusaku (day, elo, uncertainty)")
	print(whr.ratings_for_player("shusaku"))
	print("Done")
	print("-------------------------------------------------------")
	print("test getting ratings for player shusai, only current elo and uncertainty")
	print(whr.ratings_for_player("shusai", current=True))
	print("Done")
	print("-------------------------------------------------------")
	print("test getting probability of future match between shusaku and nobody2 (which default to 1 win 1 loss)")
	print(whr.probability_future_match("shusai", "nobody2", 0))
	print("Done")
	print("-------------------------------------------------------")
	print("test getting log likelihood of base")
	print(whr.log_likelihood())
	print("Done")
	print("-------------------------------------------------------")
	print("test printing ordered ratings")
	whr.print_ordered_ratings()
	print("Done")
	print("-------------------------------------------------------")
	print("test printing ordered ratings, only current elo")
	whr.print_ordered_ratings(current=True)
	print("Done")
	print("-------------------------------------------------------")
	print("test getting ordered ratings, compact form")
	print(whr.get_ordered_ratings(compact=True))
	print("Done")
	print("-------------------------------------------------------")
	print("test getting ordered ratings, only current elo with compact form")
	print(whr.get_ordered_ratings(compact=True, current=True))
	print("Done")
	print("-------------------------------------------------------")
	print("test saving base")
	Base.save_base(whr,"test_whr")
	print("Done")
	print("-------------------------------------------------------")
	print("test loading base")
	whr2 = Base.load_base('test_whr')
	print("Done")
	print("-------------------------------------------------------")
	print("test inspecting the first game")
	print(whr2.games[0].inspect())
	print("Done")
	print("-------------------------------------------------------")
