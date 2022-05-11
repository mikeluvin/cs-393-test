#!/bin/bash
toDelete=(2 4 5 9 10)
toDeleteBad=(13 16 17 18 19)
for i in ${toDelete[@]}
do
    rm "7.1/input$i-g.json"
    rm "7.1/output$i-g.json"
done

for i in ${toDeleteBad[@]}
do
    rm "7.1/input$i-b.json"
    rm "7.1/output$i-b.json"
done
