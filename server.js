/* Load the HTTP library */
var http = require("http");

// Load secret from config file.
var fs = require("fs");
console.log("hi!");

var fileName = "./secret.json";
var config;

try {
  config = require(fileName);
}
catch (err) {
  config = {};
  console.log("unable to read file '" + fileName + "': ", err);
}

console.log("session secret is:", config.clientSecret);

/* Create an HTTP server to handle responses */
http.createServer(function(request, response) {
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello World");
  response.write(config.clientSecret);
  response.end();
}).listen(8888);