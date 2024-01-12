var http = require("http");
var fs = require("fs");
var url = require("url");
const express = require("express");
const app = express();
app.use(express.json());
const path = require("path");
const { exec } = require("child_process");
const util = require('util');

app.use("/pic", express.static(path.join(__dirname, "pic")));

const execPromisified = util.promisify(exec);

app.get("/upload", async (req, res) => {
  console.log("loading code...");
  try {
    await execPromisified(`python main.py`);
    console.log("done code...");
  } catch (error) {
    console.error(`exec error: ${error}`);
  }
  res.redirect("/resalt");
});

var temp = [];

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/WebPage/login.html");
});

app.get("/chooseunit", (req, res) => {
  res.sendFile(__dirname + "/WebPage/chooseunit.html");
});

app.get("/resalt", (req, res) => {
  res.sendFile(__dirname + "/WebPage/Result.html");
});

fs.readFile("data.json", (err, fileData) => {
  if (!err) {
    temp = JSON.parse(fileData);
  }
});

app.get("/getData", (req, res) => {
  const data1 = JSON.parse(fs.readFileSync("json/data.json", "UTF-8"));
  res.json(data1);
  res.end();
});

app.post("/senddata", (req, res) => {
  const selectedCourses = req.body.selectedValues;
  const dontDays = req.body.selecteditems;
  const dontTimes = req.body.selectedHours;
  const average = req.body.average;
  const minUnit = req.body.minUnit;
  const maxUnit = req.body.maxUnit;
  const distribution = req.body.distribution;
  const dormitory = req.body.dormitory;
  const native = req.body.native;

  let data = [
    {
      selectedCourses,
      dontDays,
      dontTimes,
      average,
      minUnit,
      maxUnit,
      distribution,
      dormitory,
      native,
    },
  ];
  if (data[0].average) {
    console.log(data);
    fs.writeFile("json/help.json", JSON.stringify(data, null), (err) => {
      if (err) {
        console.error(err);
        return;
      }
      console.log("File has been created");
    });
  }
  
  res.redirect("/upload");
  // res.end();
  // res.status(200).send('Data received successfully.');
  // res.writeHead(320, { Location: "/resalt" });
});

app.listen(8080, () => console.log("Server running on port 8080"));
