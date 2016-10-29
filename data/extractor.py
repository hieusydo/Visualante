from geopy.geocoders import Nominatim
import csv
import json
import time 

def process_csv(filename, year):
  # [lat, long, value]
  extracted = []
  maxIndex = -1
  minIndex = 1  
  yr_idx = 0
  # Process csv data
  with open(filename, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
      if len(row) < 2:
        continue
      # skip first and last row
      if row[0] == "Education index":
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
        if float(row[yr_idx]) > maxIndex:
          maxIndex = float(row[yr_idx])
        if float(row[yr_idx]) < minIndex:
          minIndex = float(row[yr_idx])
      # if there is no datapoint, the default is zero
      else:
        row[yr_idx] = "0.0"
      '''
      Extract countries
      The following script is first design to extract countries and data from the CDC dataset.
      For the UNDP dataset, a simple version is enough, but the original script still works.
      '''
      l = len(row)
      entry = [int(float(row[l-2])), int(float(row[l-1])), float(row[yr_idx])]
      extracted.extend(entry)  
  print len(extracted), minIndex, maxIndex
  # print extracted
  return [extracted, 0.0, maxIndex]

def _normalize(x, x_min, x_max):
  return float((x - x_min)/(x_max - x_min))

def normalize_data(data):
  for i in range(2, len(data[0]), 3):
    # print i
    # print data[0][i], data[1], data[2]
    data[0][i] = round(_normalize(float(data[0][i]), float(data[1]), float(data[2])), 3)
  return data

def generate_JSON(years, preprocessed):
  data = []
  for i in xrange(len(years)):
    data.append([years[i], preprocessed[i]])
  with open('../globe/edu_normalized.json', 'wb') as outfile:
    json.dump(data, outfile)

def main():
  filename = 'edu_coord.csv'
  years = ["1990", "2000", "2014"]
  preprocessed = []
  # extracted = process_csv(filename, "2014")
  for year in years:
    extracted = process_csv(filename, year)
    normalized = normalize_data(extracted)
    preprocessed.append(normalized[0])
  generate_JSON(years, preprocessed)

if __name__ == '__main__':
  main()