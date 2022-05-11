#!/bin/bash
for i in {1..5}
do
    cp "4/4.1/input$i-g.json" "7/7.3/input$i-g.json"
    cp "4/4.1/output$i-g.json" "7/7.3/output$i-g.json"
done

for i in {6..10}
do
    cp "4/4.1/input$i-b.json" "7/7.3/input$i-b.json"
    cp "4/4.1/output$i-b.json" "7/7.3/output$i-b.json"
done