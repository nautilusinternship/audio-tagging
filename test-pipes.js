// version1 - using module.exports in nemo.js(don't know if this is possible). Instead of using axios in nemo.js, just update module.exports after
// each round and use that
const express = require('express');
const {spawn} = require('child_process');
const app = express();
const port = 3000
//takes the information from module.exports in nemo.js where module.exports contains items songLink: song link and roundNumber: round number
const params = require('./nemo') //test


app.get('/', (req, res) => {
    var dataToSend;
    // spawn new child process to call the python script
    // params.songLink and params.roundNumber are params that can be called and used to run knn.py
    const python = spawn('python', ['knn.py', params.songLink, params.roundNumber]); 
    // collect data from script. Takes whatever is printed from python script knn.py and post on localhost:3000
    python.stdout.on('data', function (data) {
        console.log("Pipe data from python script...");
        dataToSend = data.toString();
    });
    // send data to browser
    python.on('close', (code) => {
        console.log('child process close all stdio with code ${code}');
        res.send(dataToSend)
    });
    

})
app.listen(port, () => console.log('example app listening on port ${port}!'))

//version2- using axios as in the demo

const express = require('express');
const {spawn} = require('child_process');
const app = express();
const port = 3000

var songURI = "Null";
var roundNumber = 0;
app.post("/NemoText",(req,res)=>{
    var text = req.body["text"];
    songURI = text.split(':')[0]; //this will just be the song link
    roundNumber = text.split(':')[1];
    res.end();
})

app.get('/', (req, res) => {
    var dataToSend;
    // spawn new child process to call the python script
    // params.songLink and params.roundNumber are params that can be called and used to run knn.py
    const python = spawn('python', ['knn.py', songURI, roundNumber]); 
    // collect data from script. Takes whatever is printed from python script knn.py and post on localhost:3000
    python.stdout.on('data', function (data) {
        console.log("Pipe data from python script...");
        dataToSend = data.toString();
    });
    // send data to browser
    python.on('close', (code) => {
        console.log('child process close all stdio with code ${code}');
        res.send(dataToSend)
    });
    

})
app.listen(port, () => console.log('example app listening on port ${port}!'))
