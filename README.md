# Pokémon Card Graph Analysis

This project builds a graph-based representation of Pokémon cards using data from the [Pokémon TCG API](https://pokemontcg.io/). Each card is a node in the graph, and edges represent shared traits like types, subtypes, HP ranges, and release years. The graph structure is then used to identify similar cards, analyze price trends, and visualize connections.

## Features

- **Graph Construction**: 
  - Each Pokémon card (from Pokedex numbers 1–150) is a vertex.
  - Edges are created between cards sharing common traits:
    - Type (e.g., Fire, Water)
    - Subtype (e.g., Basic, Stage 1)
    - HP (bucketed by 10s)
    - Release Year

- **Similarity Analysis**:
  - Find cards most similar to a given card based on edge weights.
  - Identify cards with specific shared traits.
  
- **Investment Advice**:
  - Analyze the price of a card compared to the average price of its most similar cards.
  - Return qualitative insights into whether a card is overvalued or undervalued.

- **Visualization**:
  - Uses NetworkX and matplotlib to render graphs showing relationships between cards.
