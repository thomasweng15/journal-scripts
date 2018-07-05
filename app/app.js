const express = require('express')
const path = require('path')
const app = express()

app.use("/public", express.static(__dirname + "/public"))

var MongoClient = require('mongodb').MongoClient

app.get('/',function(req, res) {
    res.sendFile(path.join(__dirname+'/index.html'));
});

app.get('/api/v1.0/entries', function(req, res) {
    MongoClient.connect('mongodb://localhost:27017/journal_db', function (err, client) {
        if (err) throw err
        var db = client.db('journal_db')
        db.collection('entries').find().toArray(function (err, result) {
            if (err) throw err
            res.send(result)
        })
    })
})

app.listen(3000, () => console.log('Example app listening on port 3000!'))