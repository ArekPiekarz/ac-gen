
## Acceptance Criteria Generator

Create a template with Gerkhin style properties:

```
GIVEN
Lights: on, off
Temperature: low, medium, high
WHEN
Action: open window, open door
Time: day, night
THEN
New lights
New temperature
```

Then use it to generate a table of combinations of scenarios:
`python3 ac-gen.py --input=inputTemplate --output=generated-acs.csv`

Output from CSV, postconditions are yours to fill:
|     | GIVEN  |             | WHEN        |       | THEN       |                 | 
|-----|--------|-------------|-------------|-------|------------|-----------------| 
| #AC | Lights | Temperature | Action      | Time  | New lights | New temperature | 
| 1   | on     | low         | open window | day   |            |                 | 
| 2   | on     | low         | open window | night |            |                 | 
| 3   | on     | low         | open door   | day   |            |                 | 
| 4   | on     | low         | open door   | night |            |                 | 
| 5   | on     | medium      | open window | day   |            |                 | 
| 6   | on     | medium      | open window | night |            |                 | 
| 7   | on     | medium      | open door   | day   |            |                 | 
| 8   | on     | medium      | open door   | night |            |                 | 
| 9   | on     | high        | open window | day   |            |                 | 
| 10  | on     | high        | open window | night |            |                 | 
| 11  | on     | high        | open door   | day   |            |                 | 
| 12  | on     | high        | open door   | night |            |                 | 
| 13  | off    | low         | open window | day   |            |                 | 
| 14  | off    | low         | open window | night |            |                 | 
| 15  | off    | low         | open door   | day   |            |                 | 
| 16  | off    | low         | open door   | night |            |                 | 
| 17  | off    | medium      | open window | day   |            |                 | 
| 18  | off    | medium      | open window | night |            |                 | 
| 19  | off    | medium      | open door   | day   |            |                 | 
| 20  | off    | medium      | open door   | night |            |                 | 
| 21  | off    | high        | open window | day   |            |                 | 
| 22  | off    | high        | open window | night |            |                 | 
| 23  | off    | high        | open door   | day   |            |                 | 
| 24  | off    | high        | open door   | night |            |                 | 


You can also automatically open the output in LibreOffice Calc:
`python3 ac-gen.py --input=inputTemplate --output=generated-acs.csv --open-output`

To choose Python automatically, perform:
`chmod +x ac-gen.py`
Now you can invoke the script with just:
`./ac-gen.py --input=inputTemplate --output=generated-acs.csv`