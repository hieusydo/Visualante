# Visualante 

This is a fun project with [WebGL Globe](https://www.chromeexperiments.com/globe). The app visualizes the _Education Index_ of countries around the world. The index is calculated from the mean years of schooling and expected years of schooling. The dataset is from the [United Nations Human Development Programme](http://hdr.undp.org/en/data#). 

This project was made in about 10 hours and submitted to the [final round](https://www.mindsumo.com/contests/global-data-visualization) of _Capital One’s Software Engineering Summit Challenge_.

#### How I Made It

The challenge is to extract the information from the original dataset and convert it to the format compatible with WebGL. For each datapoint, in order for it to be graphed nicely, I need an array of latitudes, longitudes, and normalized values. 

The `extractor.py` script (in the `data` folder) goes through the preprocessed dataset and records the coordinates, minimum and maximum values. Noted, these coordinates are added to the original dataset by using [Bing Maps API](https://www.bingmapsportal.com) and Excel. My initial attempt was to get the coordinate while extracting the data using a Python library called `geopy` but the performance was inconsistent. In the original script (`extractor-old.py`), I use a dictionary to store the countries as keys, which makes it easy to look up and find the coordinates using the `Nominatim().geocode(country)` function of `geopy.geocoders` lib. However, I kept running into problems with server errors. 

After the values and coordinates are extracted, the values are normalized using the formula `(x - x_min)/(x_max - x_min)`. Finally, all the data are formatted and exported to a JSON file that is ready to be visualized by WebGL Globe. 

#### Other things

__Why Education Index?__

I always want to visualize something meaningful. Starting with the _Neglected Tropical Diseases_ (NTD) dataset from the [Centers for Disease Control and Prevention](https://data.cdc.gov/), I wanted to show how the diseases are concentrated in developing countries and usually ignored. The goal was to raise awareness about NTDs. However, the dataset from the CDC does not have enough entries. In contrast, the UNHDP dataset is more comprehensive (there are more countries and data dating back many years). Plus, education is an important topic. Through the visualization, we can see that the education index increases over the past years. 

__Notes for the future__

In order to get a nice visualization, I need a dataset as diverse and comprehensive as possible in terms of geography. The UNHDP education index dataset is country-based; it would have been more ideal if it's city-based, which is uncommon when it comes to education index, but it is definitely possible for population. 

