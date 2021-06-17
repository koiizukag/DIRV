import random
import sys
import numpy as np

from collections import defaultdict


class DIRV:
    def __init__(self, rankings):
        self.rankings = rankings
        self.items = dict()
        self.imps = defaultdict(lambda: 1.0)
        self.clicks = defaultdict(lambda: 1.0)
        self.postclick_values = defaultdict(list)
        self.with_predicted_variance = False
        self.default_mean = sys.float_info.max

        for ranking_idx in range(len(rankings)):
            for rank in range(rankings[ranking_idx].len):
                item = rankings[ranking_idx].item(rank)
                self.items[item.item_id] = item

    def get_scores(self):
        scores = []
        for ranking_idx in range(len(self.rankings)):
            score = 0.0
            ap = 1.0
            for rank in range(self.rankings[ranking_idx].len):
                item = self.rankings[ranking_idx].item(rank)
                item_id = item.item_id
                values = self.postclick_values[item_id]
                if values:
                    ctr = self.clicks[item_id] / self.imps[item_id]
                    mu = np.mean(values)
                    score += ap * ctr * mu
                    print(item_id, ap * ctr, mu)
                    ap *= 1 - ctr
            print("")
            scores.append(score)
        return scores

    def interleave(self):
        item_vars = []
        for item_id, item in random.sample(self.items.items(), len(self.items.items())):
            ctr = self.clicks[item_id] / self.imps[item_id]
            if len(self.postclick_values[item_id]) <= 1:
                sigma = random.random()
            else:
                sigma = np.var(self.postclick_values[item_id])

            if len(self.postclick_values[item_id]) <= 1:
                mean = self.default_mean
            else:
                mean = np.mean(self.postclick_values[item_id])

            if self.with_predicted_variance and sigma < item.predicted_sigma:
                sigma = item.predicted_sigma
            score = self.L(
                self.clicks[item_id], self.imps[item_id], ctr, sigma, mean
            ) - self.L(
                self.clicks[item_id] + 1 * ctr,
                self.imps[item_id] + 1,
                ctr,
                sigma,
                mean,
            )
            item_vars.append((item_id, score))

        item_ids = []
        sorted_items = sorted(item_vars, key=lambda iv: -iv[1])

        for rank in range(self.rankings[0].len):
            item_ids.append(sorted_items[rank][0])

        return item_ids

    def L(self, click, imp, p, sigma, mean):
        return (p * (1 - p) / imp + p * p) * p * sigma / click + (
            p * (1 - p) * mean * mean
        ) / imp
