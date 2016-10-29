from geopy.geocoders import Nominatim
import csv
import json
import time 

def process_csv(filename, year):
  countries = dict()
  maxIndex = 1
  minIndex = -1  
  yr_idx = 0
  # Process csv data
  with open(filename, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
      # skip first and last row
      if len(row) < 2:
        continue
      # get header row, find the year
      if row[0] == "HDI Rank":
        while row[yr_idx] != year and yr_idx < len(row):
          yr_idx += 1
        if yr_idx == len(row[0]):
          print year, "is not in the dataset"
          return
        continue
      # handle empty string 
      if row[yr_idx]:
        # get min and max index for normalization
        if row[yr_idx] > maxIndex:
          maxIndex = row[yr_idx]
        if row[len(row)-1] < minIndex:
          minIndex = row[yr_idx]
      # if there is no datapoint, the default is zero
      else:
        row[yr_idx] = "0.0"
      '''
      Extract countries
      The following script is first design to extract countries and data from the CDC dataset.
      For the UNDP dataset, a simple version is enough, but the original script still works.
      '''
      if row[1] in countries:
        # Don't wanna miss united countries
        if len(row[2]) > 4:
          countries[row[2]] = row[yr_idx]
        else:
          countries[row[1]] += row[yr_idx]
      else:
        countries[row[1]] = row[yr_idx]
  
  # print "There are", len(countries), "countries."
  # print countries
  return [minIndex, maxIndex, countries]

def normalize(x, x_min, x_max):
  return float((x - x_min)/(x_max - x_min))

def assign_geocode_to_countries(data):
  # Get geolocation of the countries
  g = Nominatim()
  geocoded = []
  for country in data[2]:
    try: 
      locator = g.geocode(country)
      # sleep between requests to prevent overwhelimg server
      # time.sleep(10)
      geocoded.extend((locator.latitude, locator.longitude, normalize(float(data[2][country]), float(data[0]), float(data[1]))))
    except Exception as error:
      print country, "not located?!"
      print repr(error)
  return geocoded

def generate_JSON(years, preprocessed):
  data = []
  for i in xrange(len(years)):
    data.append([years[i], preprocessed[i]])
  with open('../globe/edu_normalized.json', 'wb') as outfile:
    json.dump(data, outfile)

def main():
  filename = 'edu.csv'
  years = ["1990", "2000", "2014"]
  preprocessed = []
  for year in years:
    extracted = process_csv(filename, year)
    geocoded = assign_geocode_to_countries(extracted)
    preprocessed.append(geocoded)
  generate_JSON(years, preprocessed)

if __name__ == '__main__':
  main()