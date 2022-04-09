import process from 'process';
import fs from "fs";
import { my_sort } from '../2.2/backend.js';

function frontend(inputString) {
    let inputArr = [],
        inputSubArr = [],
        currString = "",
    // create a set of valid values, 1 to 24
        validRange = new Array(24);
    for (let i = 0; i < validRange.length; i++) {
        validRange[i] = i + 1;
    }
    validRange = new Set(validRange);

    let startBracket = inputString.indexOf("{"),
        endBracket = inputString.indexOf("}", startBracket),
        oldStartBracket = startBracket,
        oldEndBracket = endBracket,
        _json = "",
        validJson = false;

    while (startBracket !== -1 && endBracket !== -1) {
        // keep trying to build a JSON object by finding the next closing bracket
        while (!validJson) {
            currString = inputString.slice(startBracket, endBracket+1).trim();
            try {
                _json = JSON.parse(currString);
                validJson = true;
            } catch {
                endBracket = inputString.indexOf("}", endBracket + 1);
            } 
        }
        oldStartBracket = startBracket;
        oldEndBracket = endBracket;
        startBracket = inputString.indexOf("{", endBracket + 1);
        endBracket = startBracket != -1? inputString.indexOf("}", startBracket + 1) : -1;
        validJson = false;
        // if the object is inside a list, ignore it
        if (inputString.charAt(oldEndBracket + 1) === "," || inputString.charAt(oldEndBracket + 1) == "]") {
            continue
        }

        if (!(typeof(_json) === "object" && Object.keys(_json).length === 1
            && typeof(_json["content"]) === "number" && validRange.has(_json["content"]))) 
        {
            continue;
        }
        inputSubArr.push(_json);
        
        if (inputSubArr.length === 10) {
            inputArr.push(inputSubArr);
            inputSubArr = [];
        }
    }

    let resArr = [];
    for (const arr of inputArr) {
        resArr.push(JSON.parse(my_sort(JSON.stringify(arr))));
    }
    return resArr;
}

function main() {
    let inputString = fs.readFileSync(0, 'utf-8');
    process.stdout.write(JSON.stringify(frontend(inputString)));
}

main();