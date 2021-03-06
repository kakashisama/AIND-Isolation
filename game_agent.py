
import random
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float((2*own_moves - 3*opp_moves)*(49.0-len(game.get_blank_spaces())))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    filled_spaces = 49.0-len(game.get_blank_spaces())
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    own_dist = float((h - y)**2 + (w - x)**2)
    y, x = game.get_player_location(game.get_opponent(player))
    opp_dist = float((h - y)**2 + (w - x)**2)
    if filled_spaces < 12 :
        return float(2*opp_dist - 3*own_dist)
    elif filled_spaces < 36:
        return float(2*own_moves-3*opp_moves)
    else:
        return (2*own_moves)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp_moves = game.get_legal_moves(game.get_opponent(player))
    own_moves = game.get_legal_moves(player)
    if len(list(set(opp_moves) & set(own_moves))) > 0 and len(own_moves)>len(opp_moves) :
        return len(own_moves)*(49.0-len(game.get_blank_spaces()))*3
    elif len(list(set(opp_moves) & set(own_moves))) == 1  and len(own_moves)==1:
        return len(own_moves)*(49.0-len(game.get_blank_spaces()))*5
    else :
        return float(3*len(game.get_legal_moves(player)))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.

            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """
        Minimax implementation based on AIMA MINIMAX psuecode :
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : Integer
            Initial call will include depth defined in init

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.

        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        if len(legal_moves)==1:
            return legal_moves[0]

        # First call is always for the player you initiated the minimax algorithm, hence maximized
        _, move = max([(self.minimizedvalue(game.forecast_move(m),depth-1),m) for m in legal_moves])
        return move

    def maximizedvalue(self, game, depth):
        """
        Minimax implementation maximize utility function based on :
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : Integer
            Depth passed from minimize function

        Returns
        -------
        val : Float
            Returns float score that is maximized for this level in the three based on Player's move

        """
        legal_moves = game.get_legal_moves()

        if depth<=0 or (not legal_moves):
            return self.score(game,game.active_player)

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        val=-math.inf

        for m in legal_moves:
            newval=self.minimizedvalue(game.forecast_move(m),depth-1)
            val=max(val,newval)
        return val

    def minimizedvalue(self, game, depth):
        """
        Minimax implementation minimize utility function based on :
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : Integer
            Depth passed from original minimax function or maximize function

        Returns
        -------
        val : Float
            Returns float score that is minimized for this level in the three based on Opponent's move

        """
        legal_moves = game.get_legal_moves()

        if depth<=0 or (not legal_moves):
            return self.score(game,game.inactive_player)

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        val=math.inf

        for m in legal_moves:
            newval=self.maximizedvalue(game.forecast_move(m),depth-1)
            val=min(val,newval)
        return val

class AlphaBetaPlayer(IsolationPlayer):

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        IsolationPlayer.__init__(self, search_depth, score_fn, timeout)
        self.myname=str(score_fn)
        self.max_depth=0

    def __del__(self):
        print("Maximum depth reached by {} object was :{}".format(self.myname,self.max_depth))

    def get_move(self, game, time_left):
        """
        Method iteratively deepens and uses alphabeta technique to return the best move

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        best_move = (-1, -1)
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            for depth in range(1,50000):
                best_move = self.alphabeta(game, depth)
                if depth > self.max_depth:
                    self.max_depth=depth
        except SearchTimeout:
            return best_move

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        """
        Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        if len(legal_moves)==1:
            return legal_moves[0]

        val=-math.inf
        first_move={}
        for m in legal_moves:
            val=max(val,self.minimizedvalue(game.forecast_move(m),depth-1,alpha,beta))
            if val>=beta:
                return m
            alpha=max(alpha,val)
            first_move[m]=val
        for a,b in first_move.items():
            if b==max(first_move.values()):
                return a

    def maximizedvalue(self, game, depth, alpha, beta):
        """
        Alphabeta implementation maximize utility function based on :
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        val : Float
            Returns float score that is maximized for this level based on Player's move

        """
        legal_moves = game.get_legal_moves()
        if depth<=0 or (not legal_moves):
            return self.score(game,game.active_player)

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        val=-math.inf

        for m in legal_moves:
            val=max(val,self.minimizedvalue(game.forecast_move(m),depth-1,alpha,beta))
            if val>=beta:
                return val
            alpha=max(alpha,val)
        return val

    def minimizedvalue(self, game, depth, alpha, beta):
        """
        Alphabeta implementation minimize utility function based on :
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        val : Float
            Returns float score that is minimized for this level based on Player's move

        """
        legal_moves = game.get_legal_moves()
        if depth<=0 or (not legal_moves):
            return self.score(game,game.inactive_player)

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        val=math.inf

        for m in legal_moves:
            val=min(val,self.maximizedvalue(game.forecast_move(m),depth-1,alpha,beta))
            if val<=alpha:
                return val
            beta=min(beta,val)
        return val

