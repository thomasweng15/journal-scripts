const express = require('express')
const path = require('path')
const app = express()

app.use("/public", express.static(__dirname + "/public"))

var MongoClient = require('mongodb').MongoClient

// MongoClient.connect('mongodb://localhost:27017/journal_db', function (err, client) {
//   if (err) throw err

//   var db = client.db('journal_db')
  
//   db.collection('entries').find().toArray(function (err, result) {
//     if (err) throw err

//     console.log(result)
//   })
// })

app.get('/',function(req,res){
    res.sendFile(path.join(__dirname+'/index.html'));
});

// app.get('/', (req, res) => res.send('Hello World!'))

app.listen(3000, () => console.log('Example app listening on port 3000!'))