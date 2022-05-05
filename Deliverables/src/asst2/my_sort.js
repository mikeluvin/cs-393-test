export function my_sort(jsonArr) {
    var inputArr = JSON.parse(jsonArr);
    // see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
    // for how JS sort method works
    inputArr.sort((obj1, obj2) => obj1["content"] - obj2["content"]);

    return JSON.stringify(inputArr);
}