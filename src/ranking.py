class Ranking:
    def __init__(self, ranking):
        self.ranking = ranking
        self.len = len(ranking)

    def item(self, idx):
        return self.ranking[idx]

    def ground_truth_expected_value(self):
        v = 0.0
        ap = 1.0
        for i, item in enumerate(self.ranking):
            v += ap * item.ctr * item.mu
            ap *= 1 - item.ctr
        return v
