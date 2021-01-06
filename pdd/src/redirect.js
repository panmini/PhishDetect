//var url ='https://tls.tc/n5d9w958';
'use strict';

const args = process.argv.slice(2);

var url ='https://www.google.com';
url ='https://tls.tc/yplbfsgn';
//url = 'https://segurocombeneficiosresgate.club/promocao/descontao/card/home.php'

//url = args[0];

var fs = require('fs');
var util = require('util');
var log_file = fs.createWriteStream(__dirname + '/file/slr.txt', {flags : 'w'});
var log_stdout = process.stdout;

//console.log = function(d) { //
//  log_file.write(util.format(d) + '\n');
  //log_stdout.write(util.format(d) + '\n');
//};
//console.log(url)
const request = require("request");
//console.log("Starting, Landing and Redirection Chain Links:")
var chain = [];

request({
  url: url,
  method: "GET",
  followRedirect: function(response){
    console.log(response.request.href)
    //chain.push(response.request.href)
    //console.log(chain)
    return true
  }
}, function(error, response, body){
//chain.push(response.request.href)
//console.log(response)
if (response !== 'undefined' && response) {
console.log( response.request.href);}
	else{
		console.log(url)
	}
//console.log(chain)}
//return chain
//return chain
})
//console.log(chain)
//return chain
