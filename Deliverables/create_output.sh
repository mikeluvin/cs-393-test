#!/bin/bash
for i in {1..5}
do
    cp "5/5.1/input$((i+5)).json" "6/6.1/input$i.json"
    cp "5/5.1/output$((i+5)).json" "6/6.1/output$i.json"
done