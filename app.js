var express = require('express');
 
var app = express();
 
var port = process.env.PORT || 8080;

app.use('/', express.static(__dirname + '/globe'));

app.listen(port, function() {
  console.log('Our app is running on http://localhost:' + port);
}); 