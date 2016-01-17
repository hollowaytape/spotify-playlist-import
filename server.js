/* Load the HTTP library */
var http = require("http");

// Load secret from config file.
var fs = require("fs");

fs.readFile('secret.json', function processClientSecrets(err, content) {
	if (err) {
		console.log('Error loading client secret file: ' + err);
		return;
	}
	// Authorize a client with the loaded credentials, then call the
	// Spotify API.
	authorize(JSON.parse(content), call)
	}
})

/* Create an HTTP server to handle responses */
http.createServer(function(request, response) {
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello World");
  response.write(config.clientSecret);
  response.end();
}).listen(8888);