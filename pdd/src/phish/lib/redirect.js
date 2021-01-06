//var url ='https://tls.tc/n5d9w958';
'use strict';

const args = process.argv.slice(2);

//var url ='https://www.google.com';
//url ='https://tls.tc/yplbfsgn';
var url = args[0];

var fs = require('fs');
var util = require('util');
var log_file = fs.createWriteStream(__dirname + '/file/slr.txt', {flags : 'w'});
var log_stdout = process.stdout;

console.log = function(d) { //
  log_file.write(util.format(d) + '\n');
  //log_stdout.write(util.format(d) + '\n');
};
//console.log(url)
const request = require("request");
//console.log("Starting, Landing and Redirection Chain Links:")

request({
  url: url,
  method: "GET",
  followRedirect: function(response){
    console.log(response.request.href)
    return true
  }
}, function(error, response, body){
console.log( response.request.href);
})
