"""CSC111 Project 2: Issei, Jada, Theo"""
from __future__ import annotations
import random
from itertools import combinations, islice
from collections import defaultdict
from typing import Optional
from datetime import datetime
import requests
from matplotlib import pyplot as plt
import networkx as nx


class Card:
    """
    A Pokemon card object represented as a vertex

    instance attributes:
        - id: the id number of the card given by API
        - name: the name of the pokemon
        - types: pokemon's type(s)
        - subtypes: substype(s) of the pokemon i.e. basic, mega evolution, stage 2, etc.
        - hp: amount of pokemon's hitpoints
        - rel_date: a datetime object representing the day the card was released
        - price: the average market price of the card on
        - image: link for the image of the card
    """
    id: str
    name: str
    types: list[str]
    subtype: list[str]
    hp: int
    rarity: Optional[str]
    reldate: datetime
    price: float
    neighbours: dict[Card, float]

    def __init__(self, idd: str, name: str, types: list[str], subtype: list[str], hp: int, rarity: str,
                 reldate: datetime, price: float) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        self.id = idd
        self.name = name
        self.types = types
        self.subtype = subtype
        self.hp = hp
        self.rarity = rarity
        self.reldate = reldate
        self.price = price
        self.neighbours = {}
        # apikey = "c3235621-8f10-4e19-abba-fc8028faae15"

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def getneighbours(self) -> dict[Card, float]:
        """
        getter method for a card's neighbours
        """
        return self.neighbours


class Cardgraph:
    """
    Class representing the graph holding all of the pokemon cards

    instance attributes:
        - _vertices: a mapping of all vertices, cards, in the cardgraph.
    """
    _vertices: dict[str, Card]

    def __init__(self) -> None:
        self._vertices = self.loaddata()
        self.connectneighbours()

    def loaddata(self) -> dict[str, Card]:
        """
        loads the data from the API and organizes into a dictionary corresponding to Cards.
        """
        apikey = "c3235621-8f10-4e19-abba-fc8028faae15"
        response3 = requests.get("https://api.pokemontcg.io/v2/cards?q=nationalPokedexNumbers:[1 TO 151]&"
                                 "pageSize=250&page=1", headers={"X-Api-Key": apikey})
        result = response3.json()["data"]
        ret = {}
        for j in result:
            try:
                a = j["rarity"]
            except KeyError:
                a = None
            try:
                b = j["cardmarket"]["prices"]["averageSellPrice"]
            except KeyError:
                b = None
            if b is not None:
                ret[j["id"]] = Card(j["id"], j["name"], j["types"], j["subtypes"], int(j["hp"]), a,
                                    datetime.strptime(j["set"]["releaseDate"], "%Y/%m/%d"),
                                    j["cardmarket"]["prices"]["averageSellPrice"])
        # Pick a random page from
        pgs = random.sample(range(2, 18), 2)
        for i in pgs:
            response2 = requests.get("https://api.pokemontcg.io/v2/cards?q=nationalPokedexNumbers:[1 TO 151]&"
                                     f"pageSize=250&page={i}", headers={"X-Api-Key": apikey})
            result = response2.json()["data"]
            # print(result)
            for j in result:
                try:
                    a = j["rarity"]
                except KeyError:
                    a = None
                try:
                    b = j["cardmarket"]["prices"]["averageSellPrice"]
                except KeyError:
                    b = None
                if b is not None:
                    ret[j["id"]] = Card(j["id"], j["name"], j["types"], j["subtypes"], int(j["hp"]), a,
                                        datetime.strptime(j["set"]["releaseDate"], "%Y/%m/%d"),
                                        j["cardmarket"]["prices"]["averageSellPrice"])
        return ret

    def connectneighbours(self) -> None:
        """
        temp
        """
        hps = defaultdict(set)
        types = defaultdict(set)
        subtypes = defaultdict(set)
        relyrs = defaultdict(set)
        for card in self._vertices.values():
            for typ in card.types:
                types[typ].add(card.id)
            for typ2 in card.subtype:
                subtypes[typ2].add(card.id)
            hps[card.hp // 10].add(card.id)
            relyrs[int(card.reldate.year)].add(card.id)
        for i in types:
            for j in types[i]:
                for k in types[i]:
                    if k != j:
                        self.addedge(self._vertices[k], self._vertices[j], 1)
        for a in subtypes:
            for b in subtypes[a]:
                for c in subtypes[a]:
                    if b != c:
                        self.addedge(self._vertices[b], self._vertices[c], 2)
        for d in hps:
            for e in hps[d]:
                for f in hps[d]:
                    if e != f:
                        self.addedge(self._vertices[e], self._vertices[f], 3)
        for y in relyrs:
            for h in relyrs[y]:
                for m in relyrs[y]:
                    if h != m:
                        self.addedge(self._vertices[h], self._vertices[m], 4)

    def addedge(self, v1: Card, v2: Card, weight: int) -> None:
        """
        Adds a weighted edge between two given cards, if an edge already exists, increases the weight of
        said edge.
        """
        if v1 in self._vertices.values() and v2 in self._vertices.values():
            if v2 in v1.neighbours:
                v1.neighbours[v2] += weight
                v2.neighbours[v1] += weight
            else:
                v1.neighbours[v2] = weight
                v2.neighbours[v1] = weight

    def findcard(self, id0: str) -> Card:
        """
        Getter method for returning a card object given id
        """
        return self._vertices[id0]

    def searchname(self, name: str) -> list[str]:
        """
        Takes in a name of a pokemon and returns a list of ID numbers of cards of that pokemon
        """
        return [card.id for card in self._vertices.values() if card.name.lower() == name.lower()]

    def findsimilartrait(self, comp: str, trait: str) -> list[str]:
        """
        Returns a list containing all the ids of pokemon that share the same given trait with the card
        corresponding to comp
        """
        if trait == "type":
            result = [card.id for card in self._vertices[comp].getneighbours() if
                      self._vertices[comp].getneighbours()[card] == 2]
        elif trait == "subtype":
            result = [card.id for card in self._vertices[comp].getneighbours() if
                      self._vertices[comp].getneighbours()[card] == 1]
        elif trait == "hp":
            result = [card.id for card in self._vertices[comp].getneighbours() if
                      self._vertices[comp].getneighbours()[card] == 3]
        elif trait == "relyear":
            result = [card.id for card in self._vertices[comp].getneighbours() if
                      self._vertices[comp].getneighbours()[card] == 4]
        else:
            result = ["Please enter a valid trait, <type>, <subtype>, <hp>, <relyear>"]
        return result

    def fetchimage(self, id3: str) -> str:
        """
        returns the URL for a card image
        """
        idi = id3.split("-")
        reponse = f"https://images.pokemontcg.io/{idi[0]}/{idi[1]}.png"
        return reponse

    def mostsimilar(self, id4: str) -> dict[Card, int]:
        """
        Returns a dictionary representing all of id's neighbours sorted in order of most to least similarity
        """
        compcard = self.findcard(id4)
        dct = {}
        for card in compcard.getneighbours():
            if card in dct:
                dct[card] += int(compcard.neighbours[card])
            else:
                dct[card] = int(compcard.neighbours[card])
        return dict(sorted(dct.items(), key=lambda item: item[1], reverse=True))

    def analyzeprice(self, idi: str) -> str:
        """
        compares id to top 10 most similar cards and calculates differences in price to see if the user
        should or should not invest in a card
        """
        res = ""
        closestcards = dict(islice(self.mostsimilar(idi).items(), 10))
        res += (f"\n\n================================="
                f"\n---Analyzing prices for cards similar to {self.findcard(idi).name}---\n\n")
        total = float(sum(closestcards.values()))
        prices = 0.0
        minprice = (11.0, 10000.0)
        totals = 0.0
        for card in closestcards:
            if (closestcards[card] / total) * card.price < minprice[1]:
                minprice = list(closestcards.keys()).index(card), (closestcards[card] / total) * card.price
            prices += (closestcards[card] / total) * card.price
            totals += closestcards[card] / total
        percdiff = ((prices - self.findcard(idi).price) / self.findcard(idi).price) * 100
        res += (f"Original price: {self.findcard(idi).price} \nAverage price of top 10 closest "
                f"cards: {round(prices, 5)} \nPercent difference: {round(percdiff, 5)}\n")
        if percdiff > 40:
            res += (f"\nCompared to similar cards, {self.findcard(idi).name} (id: {idi}) is very overvalued."
                    f"\nIt's probably not a good idea to buy this card now.")
        elif percdiff > 0:
            res += f"\nCompared to similar cards, {self.findcard(idi).name} (id: {idi}) is slightly overvalued."
        elif percdiff > -40:
            res += f"\nCompared to similar cards, {self.findcard(idi).name} (id: {idi}) is slightly undervalued."
        else:
            res += (f"\nCompared to similar cards, {self.findcard(idi).name} (id: {idi}) is slightly overvalued."
                    f"\nThis card is likely to be a good investment!")
        res += "\n=================================\n"
        return res

    def visualize(self, main_card: Card, similar_cards: list[Card]) -> None:
        """
        Visualizes a graph where:
        - The main card is connected to all similar cards.
        - Similar cards are also connected to each other if they share a trait.
        """
        gr = nx.Graph()

        # Add main card as a node
        main_card_id = main_card.id
        gr.add_node(main_card_id, label=main_card.name, color="red")
        similar_cards = list(self.mostsimilar(main_card_id).keys())[:20]
        # Add similar cards as nodes
        for card in similar_cards:
            card_id = card.id
            gr.add_node(card_id, label=card.name, color="blue")
            gr.add_edge(main_card_id, card_id, weight=main_card.neighbours[card])  # Connect main card to similar cards

        # Connect similar cards if they share a trait
        for card1, card2 in combinations(similar_cards, 2):
            if card2 in card1.getneighbours().keys() and card1.neighbours[card2] > 5:
                gr.add_edge(card1.id, card2.id, weight=card1.neighbours[card2])

        # Draw the graph
        pos = nx.spring_layout(gr, weight="weight")  # Layout for better visualization
        colors = [gr.nodes[n].get("color", "gray") for n in gr.nodes]  # Default to gray if missing
        nx.draw(gr, pos, with_labels=True, labels=nx.get_node_attributes(gr, 'label'),
                node_color=colors, node_size=2500, font_size=11, font_color="green", edge_color="gray")

        plt.show()


if __name__ == '__main__':
    # Important: dataset only contains pokemon with pokedex numbers 1-151.
    g = Cardgraph()
    print("")
    # Testing searchname
    examplelist = g.searchname("ponyta") + g.searchname("pidgey") + g.searchname("geodude")
    print(examplelist)

    # example card
    tcard = g.findcard("ex8-8")
    # tcard = g.findcard(examplelist[random.randint(0, len(examplelist))])

    print(tcard.id, tcard.name, tcard.types, tcard.subtype, tcard.hp, tcard.price)
    print(g.fetchimage(tcard.id))
    print()
    # testing similar traits with year
    print(f"Cards with the same year as {tcard.id}:")
    print(g.findsimilartrait(tcard.id, "relyear"))
    print()
    print(g.analyzeprice(tcard.id))
    g.visualize(tcard, list(tcard.getneighbours().keys()))
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [
            "random", "PIL.Image", "itertools", "io", "networkx",
            "matplotlib.pyplot", "collections", "typing", "requests",
            "datetime", "matplotlib.image"
        ],
        'allowed-io': ['analyzeprice', 'input', 'print', 'output'],
        'max-line-length': 120,
        'disable': ['R1702']
    })
