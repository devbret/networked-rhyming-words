# Networks Of Rhyming Words Visualized

![A screenshot featuring a network graph visualizing rhyming words from all of Edgar Allan Poe's poems.](https://hosting.photobucket.com/bbcfb0d4-be20-44a0-94dc-65bff8947cf2/1772e123-073d-4da9-b1ab-862f6a5253ff.png)

Analyze a text file to detect rhymes between line-ending words, build a network from those relationships and visualize the resulting structure with D3.

## Application Overview

This application analyzes a plain text document to identify rhyme relationships between the final words of each line. It uses the CMU Pronouncing Dictionary to compare phonetic rhyme endings, while also accounting for stress patterns, word frequency, repeated positions and fallback spelling-based similarity when pronunciation data is unavailable.

The resulting words are represented as nodes in a rhyme network, with connections weighted by rhyme strength. The application exports this structure as JSON, with optional GraphML and GEXF support, as well as visualizes it through an interactive D3 graph where users can explore rhyme families, clusters, repetitions and relationships across the source text.

## Basic Setup Instructions

Below are the required software programs and instructions for installing and using this application on a Linux machine.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/)

### Steps

1. Install the above programs

2. Open a terminal

3. Clone this repository: `git clone git@github.com:devbret/networked-rhyming-words.git`

4. Navigate to the repo's directory: `cd networked-rhyming-words`

5. Create a virtual environment: `python3 -m venv venv`

6. Activate your virtual environment: `source venv/bin/activate`

7. Install the required Python packages: `pip install -r requirements.txt`

8. Place your `.txt` file at the root of this repo

9. Process the raw data: `python3 app.py -i my_file_name.txt`

10. Start an HTTP server: `python3 -m http.server`

11. Access the heatmap visualization in a browser: `http://localhost:8000`

12. When finished, close the HTTP server: `CTRL + c`

13. Exit the virtual environment: `deactivate`

## Other Considerations

This project repo is intended to demonstrate an ability to do the following:

- Analyze song lyrics to identify rhyming words and convert them into an interactive network graph

- Detect rhyme relationships between line-ending words using pronunciation data and stress patterns

- Export rhyme data as JSON, with optional GraphML and GEXF formats

- Visualize rhyme families with D3.js, allowing users to explore connected rhyme clusters

If you have any questions or would like to collaborate, please reach out either on GitHub or via [my website](https://bretbernhoft.com/).
