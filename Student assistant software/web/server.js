var http = require("http");
var fs = require("fs");
var url = require("url");
const express = require("express");
const app = express();
app.use(express.json());

const { exec } = require('child_process');
app.get('/upload', (req, res) => {
  exec(`python main.py`, (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return;
    }

  });
  res.end();
});

var temp =[];

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/login.html');
});

app.get('/chooseunit', (req, res) => {
    res.sendFile(__dirname + '/chooseunit.html');
});

fs.readFile("data.json", (err, fileData) => {
    if (!err) {
      temp = JSON.parse(fileData);
    }
  });

  app.get("/getData", (req, res) => {
    const data1 = JSON.parse(fs.readFileSync("data.json", "UTF-8"));
    res.json(data1);
    res.end();
  });


  app.post('/senddata', (req, res) => {
    const selectedCourses = req.body.selectedValues;
    const grade = req.body.grade;
    const minUnit = req.body.minUnit;
    const maxUnit = req.body.maxUnit;
    const distribution = req.body.distribution;
    const dormitory = req.body.dormitory;

    let data =[{
        selectedCourses,
        grade,
        minUnit,
        maxUnit,
        distribution,
        dormitory
    }];
    console.log(data);
    if((data[0].grade)){

        fs.writeFile('help.json', JSON.stringify(data,null),(err)=> {
            if (err) {
                console.error(err);
                return;
            };
            console.log("File has been created");
        });
    }
   
  



    // res.status(200).send('Data received successfully.');
    res.writeHead(300, { Location: "/upload" });    

});







app.listen(8080, () => console.log("Server running on port 8080"));
