#!/bin/bash
for i in {1..10}
do
    ./run < "input$i.json" > "test-out-$i.json"
    diff "output$i.json" "test-out-$i.json"
    rm "test-out-$i.json"
done