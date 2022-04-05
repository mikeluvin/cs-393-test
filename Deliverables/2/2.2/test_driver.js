//import * as readline from 'readline';
import process from 'process';
import { my_sort } from './backend.js';

function main() {
    // see https://stackoverflow.com/questions/26460324/how-to-work-with-process-stdin-on
    // and https://nodejs.org/api/process.html#processstdin
    process.stdin.resume();
    let inputArr = [];
    let currString = "";
    process.stdin.on("data", (inputBytes) => {
        // read all the data, replace any newlines with an empty string
        let inputString = inputBytes.toString().replaceAll("\n", "");
        inputString = currString.concat(inputString);
        let startBracket = 0;
        let endBracket = inputString.indexOf("}", startBracket);

        while (inputArr.length < 10 && endBracket != -1) {
            currString = inputString.slice(startBracket, endBracket+1).trim();
            inputArr.push(JSON.parse(currString));
            startBracket = endBracket + 1;
            endBracket = inputString.indexOf("}", startBracket);
            currString = "";
        } 

        if (endBracket == -1) {
            currString = inputString.slice(startBracket).trim();
        }

        if (inputArr.length == 10) {
            process.stdout.write(my_sort(JSON.stringify(inputArr)));
            process.stdin.destroy();
        }
    })
}

main();