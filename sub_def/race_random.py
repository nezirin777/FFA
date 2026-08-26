"""旧版Perl互換のレース用乱数計算。"""

import random


def legacy_rand(limit):
    """Perlのint(rand(x))と同じく、上限を含めない整数を返す。"""
    limit = float(limit)
    return int(random.random() * limit) if limit > 0 else 0


def legacy_rand_float(limit):
    """Perlのrand(x)と同じ、整数化しない乱数を返す。"""
    limit = float(limit)
    return random.random() * limit if limit > 0 else 0.0


def legacy_rand_plus(limit):
    """Perlのint(rand(x) + x)と同じ値を返す。"""
    limit = float(limit)
    return int(random.random() * limit + limit) if limit > 0 else 0
