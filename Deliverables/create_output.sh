#!/bin/bash
for i in {1..10}
do
    touch "5/5.1/input$i.json"
    touch "5/5.1/output$i.json"
    touch "5/5.2/input$i.json"
    touch "5/5.2/output$i.json"
done