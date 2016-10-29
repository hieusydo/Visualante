var express = require('express');
var request = require('request');
var jsonfile = require('jsonfile')

var app = express();
 
var port = process.env.PORT || 8080;

// Render HTML
app.use('/', express.static(__dirname + '/globe'));

// Parse data
for (var i = 0; i < 5; i++) {
  // console.log("Request: " + i);
  request.get({
    url: "https://api.nytimes.com/svc/search/v2/articlesearch.json",
    qs: {
      'api-key': "103562eaa9d8447ca62218fbae4b0f0a",
      'q': "violence,murder,shooting,death",
      'sort': "newest",
      'fl': "web_url,source,snippet,_id,pub_date", 
      'page': i.toString()
    },
  }, function(err, response, body) {
    var file = i + 'data.json'
    jsonfile.writeFile(file, body, function (err) {
      console.error(err)
    })
    // body = JSON.parse(body);
    // console.log(body);
  })
}

app.listen(port, function() {
  console.log('App is running on http://localhost:' + port);
}); 