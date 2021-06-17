from src.item import Item
from src.ranking import Ranking
from src.dirv import DIRV


item1 = Item(item_id="item1")
item2 = Item(item_id="item2")
item3 = Item(item_id="item3")
rankings = [Ranking([item1, item2, item3]), Ranking([item3, item1, item2])]


def test_items():
    dirv = DIRV(rankings)
    res = dirv.interleave()
    assert set(res) == {"item1", "item2", "item3"}


def test_order_by_variance():
    dirv = DIRV(rankings)
    dirv.postclick_values["item1"] = [1, 1, 1, 2]
    dirv.postclick_values["item2"] = [1, 1, 2]
    dirv.postclick_values["item3"] = [1, 2]
    assert dirv.interleave() == ["item3", "item2", "item1"]
    assert dirv.get_scores() == [1.0 * (1 + 1 + 1 + 2) / 4.0, 1.0 * (1 + 2) / 2.0]


def test_order_by_ctr():
    dirv = DIRV(rankings)
    dirv.postclick_values["item1"] = [1, 2]
    dirv.clicks["item1"] = 1
    dirv.imps["item1"] = 2
    dirv.postclick_values["item2"] = [1, 2]
    dirv.clicks["item2"] = 1
    dirv.imps["item2"] = 3
    dirv.postclick_values["item3"] = [1, 2]
    dirv.clicks["item3"] = 1
    dirv.imps["item3"] = 4
    assert dirv.interleave() == ["item1", "item2", "item3"]
    assert dirv.get_scores() == [
        (
            1.0 * 1 / 2.0
            + (1 - 1 / 2.0) * 1.0 / 3.0
            + (1 - 1 / 2.0) * (1 - 1 / 3.0) * 1 / 4.0
        )
        * (1 + 2)
        / 2.0,
        (
            1.0 * 1 / 4.0
            + (1 - 1 / 4.0) * 1 / 2.0
            + (1 - 1 / 4.0) * (1 - 1 / 2.0) * 1 / 3.0
        )
        * (1 + 2)
        / 2.0,
    ]

    dirv.clicks["item3"] = 1
    dirv.imps["item3"] = 1
    assert dirv.interleave() == ["item3", "item1", "item2"]
    assert dirv.get_scores() == [
        (
            1.0 * 1 / 2.0
            + (1 - 1 / 2.0) * 1 / 3.0
            + (1 - 1 / 2.0) * (1 - 1 / 3.0) * 1 / 1.0
        )
        * (1 + 2)
        / 2.0,
        (
            1.0 * 1 / 1.0
            + (1 - 1 / 1.0) * 1 / 2.0
            + (1 - 1 / 1.0) * (1 - 1 / 2.0) * 1 / 3.0
        )
        * (1 + 2)
        / 2.0,
    ]
