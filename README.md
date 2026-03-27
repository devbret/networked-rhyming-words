# Networks Of Rhyming Words Visualized

![A screenshot featuring a network graph visualizing rhyming words from all of Edgar Allan Poe's poems.](https://hosting.photobucket.com/bbcfb0d4-be20-44a0-94dc-65bff8947cf2/1772e123-073d-4da9-b1ab-862f6a5253ff.png)

Analyzes a text file to detect rhymes between line-ending words, builds a network from those relationships and visualizes the resulting structure with D3.

## Overview

Analyzes a `TXT` document to construct phonetic rhyme networks based on the last word of each line. Using the CMU Pronouncing Dictionary, this application computes rhyme strength through phoneme matching, stress alignment and similarity when phonetic data is unavailable.

Words are represented as nodes annotated with frequency, positions and keys. The resulting graph is exported as JSON and visualized with an interactive D3 layout to reveal rhyme clusters, repetition and relationships across the text.

## Set Up Instructions

Below are the required software programs and instructions for installing and using this application.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/)

### Steps

1. Install the above programs

2. Open a terminal

3. Clone this repository using `git` by running the following command: `git clone git@github.com:devbret/networked-rhyming-words.git`

4. Navigate to the repo's directory by running: `cd networked-rhyming-words`

5. Create a virtual environment with this command: `python3 -m venv venv`

6. Activate your virtual environment using: `source venv/bin/activate`

7. Install the required Python packages: `pip install -r requirements.txt`

8. Place your `.txt` file into the root directory of this repo

9. Process the raw data using the Python script by running the following command: `python3 app.py -i my_file_name.txt`

10. Launch the application's frontend by starting a Python server with the following command: `python3 -m http.server`

11. Access the heatmap visualization in a browser by visiting: `http://localhost:8000`

12. Explore and enjoy

## Other Considerations

This project repo is intended to demonstrate an ability to do the following:

- Generate an interactive D3 network graph to visualize rhyming relationships between words extracted from a body of text, such as song lyrics or poetry

- Enable users to explore rhyme structures by grouping related words, highlighting connections and displaying metadata tooltips

If you have any questions or would like to collaborate, please reach out either on GitHub or via [my website](https://bretbernhoft.com/).
