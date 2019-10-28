// server.js
// load the things we need
var express = require('express');
var app = express();
const fs = require('fs');
// set the view engine to ejs
app.set('view engine', 'ejs');

const graphData = './graphs/';


data = [];
fs.readdirSync(graphData).forEach(file => {
    var contents = fs.readFileSync(graphData + file, 'utf8');
    data.push(JSON.parse(contents))
})

// use res.render to load up an ejs view file

// index page
app.get('/', function (req, res) {
    res.render('pages/index',{
        classes : JSON.stringify(data)
    });
});
app.use('/static', express.static('assets'));

app.listen(8080);
console.log('8080 is the magic port');
