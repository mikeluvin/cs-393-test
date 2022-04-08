import process from 'process';
import { my_sort } from './backend.js';

function main() {
    // see https://stackoverflow.com/questions/26460324/how-to-work-with-process-stdin-on
    // and https://nodejs.org/api/process.html#processstdin
    process.stdin.resume();
    let inputArr = [];
    let inputSubArr = [];
    let currString = "";
    process.stdin.on("data", (inputBytes) => {
        let inputString = inputBytes.toString();
        inputString = currString.concat(inputString);
        let startBracket = inputString.indexOf("{");
        let endBracket = inputString.indexOf("}", startBracket);

        while (inputSubArr.length < 10 && endBracket != -1) {
            currString = inputString.slice(startBracket, endBracket+1).trim();
            inputSubArr.push(JSON.parse(currString));
            startBracket = inputString.indexOf("{", endBracket);
            endBracket = inputString.indexOf("}", startBracket);
            currString = "";
        } 

        //
        if (endBracket == -1) {
            currString = inputString.slice(startBracket).trim();
        }

        if (inputSubArr.length == 10) {
            inputArr.push(inputSubArr);
            inputSubArr = [];
            //process.stdin.destroy();
        }
    })
}

main();