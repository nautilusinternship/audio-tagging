// test code that acutally works
const express = require('express');
const {spawn} = require('child_process');
const app = express();
const port = 3000
//takes the information from module.exports in test.js
const params = require('./test')

app.get('/', (req, res) => {
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['script2.py', params.songLink, params.round]);
    // collect data from script. Takes whatever is printed from python script script2.py and post on localhost:3000
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
