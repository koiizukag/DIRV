class Ranking:
    def __init__(self, ranking):
        self.ranking = ranking
        self.len = len(ranking)

    def item(self, idx):
        return self.ranking[idx]
