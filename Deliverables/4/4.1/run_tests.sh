#!/bin/bash
for i in {1..5}
do
    ./run < "input$i-g.json" > "test-out-$i.json"
    diff "output$i-g.json" "test-out-$i.json"
    rm "test-out-$i.json"
done

for i in {6..10}
do
    ./run < "input$i-b.json" > "test-out-$i.json"
    diff "output$i-b.json" "test-out-$i.json"
    rm "test-out-$i.json"
done