# Visualize Networks Of Rhyming Words As Interconnected Nodes

![A screenshot featuring a network graph visualizing rhyming words from all of Edgar Allan Poe's poems.](https://hosting.photobucket.com/bbcfb0d4-be20-44a0-94dc-65bff8947cf2/1772e123-073d-4da9-b1ab-862f6a5253ff.png)

Analyzes a text file to detect and score rhymes between line-ending words, builds a network from those relationships and visualizes the resulting structure interactively with D3.

# Overview

Analyzes a `TXT` document to construct phonetic rhyme networks based on the last word of each line. Using the CMU Pronouncing Dictionary, this application computes rhyme strength through phoneme matching, stress alignment and similarity when phonetic data is unavailable.

Words are represented as nodes annotated with frequency, positions and keys. The resulting graph is exported as JSON and visualized with an interactive D3 layout to reveal rhyme clusters, repetition and phonetic relationships across the text.
