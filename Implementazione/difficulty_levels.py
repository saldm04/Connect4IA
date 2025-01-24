DIFFICULTY_LEVELS = {
    1: {
        'max_depth': 5,
        'beam_width': 4,
        'heuristic_weights': {
            'win': 10000,
            'three_in_a_row': 100,
            'two_in_a_row': 50,
            'block_opponent_win': 100,
            'block_opponent_three': 45
        },
        'time_limit': 1.0,
        'center_score_map': [3, 4, 5, 5, 5, 4, 3]
    },
    2: {
        'max_depth': 5,
        'beam_width': 4,
        'heuristic_weights': {
            'win': 10000,
            'three_in_a_row': 100,
            'two_in_a_row': 50,
            'block_opponent_win': 100,
            'block_opponent_three': 45
        },
        'time_limit': 1.0,
        'center_score_map': [3, 4, 5, 5, 5, 4, 3]
    },
    3: {
        'max_depth': 7,
        'beam_width': 6,
        'heuristic_weights': {
            'win': 10000,
            'three_in_a_row': 200,
            'two_in_a_row': 100,
            'block_opponent_win': 210,
            'block_opponent_three': 100
        },
        'time_limit': 1.2,
        'center_score_map': [6, 8, 10, 14, 10, 8, 6]
    }
}