import json

diag_text = '''{
  "version": 1,
  "author": "GIAN FRANCO AROCUTIPA AROCUTIPA",
  "editor": "wokwi",
  "parts": [
    {
      "type": "wokwi-arduino-nano",
      "id": "nano",
      "top": 22.2,
      "left": 11.1,
      "rotate": 90,
      "attrs": {}
    },
    { "type": "wokwi-breadboard-half", "id": "bb1", "top": 25.8, "left": 214, "attrs": {} },
    {
      "type": "wokwi-resistor",
      "id": "r1",
      "top": 139.2,
      "left": 218.57,
      "rotate": 90,
      "attrs": { "value": "220" }
    },
    {
      "type": "wokwi-resistor",
      "id": "r2",
      "top": 139.2,
      "left": 229.85,
      "rotate": 90,
      "attrs": { "value": "220" }
    },
    {
      "type": "wokwi-resistor",
      "id": "r3",
      "top": 139.2,
      "left": 239.45,
      "rotate": 90,
      "attrs": { "value": "220" }
    },
    {
      "type": "wokwi-resistor",
      "id": "r4",
      "top": 139.2,
      "left": 249.05,
      "rotate": 90,
      "attrs": { "value": "220" }
    },
    {
      "type": "wokwi-resistor",
      "id": "r5",
      "top": 139.2,
      "left": 258.65,
      "rotate": 90,
      "attrs": { "value": "220" }
    },
    {
      "type": "wokwi-resistor",
      "id": "r6",
      "top": 139.2,
      "left": 268.25,
      "rotate": 90,
      "attrs": { "value": "220" }
    },
    {
      "type": "wokwi-resistor",
      "id": "r7",
      "top": 139.2,
      "left": 277.85,
      "rotate": 90,
      "attrs": { "value": "220" }
    },
    {
      "type": "wokwi-7segment",
      "id": "sevseg1",
      "top": 91.38,
      "left": 475.48,
      "attrs": { "common": "cathode", "color": "red" }
    },
    {
      "type": "wokwi-7segment",
      "id": "sevseg2",
      "top": 91.38,
      "left": 417.88,
      "attrs": { "common": "cathode", "color": "red" }
    },
    { "type": "chip-2n2222", "id": "chip1", "top": 317.82, "left": 235.2, "attrs": {} },
    { "type": "chip-2n2222", "id": "chip2", "top": 365.82, "left": 235.2, "attrs": {} },
    {
      "type": "wokwi-resistor",
      "id": "r8",
      "top": 378.35,
      "left": 153.6,
      "attrs": { "value": "1000" }
    },
    {
      "type": "wokwi-resistor",
      "id": "r9",
      "top": 330.35,
      "left": 144,
      "attrs": { "value": "1000" }
    }
  ],
  "connections": [
    [ "nano:5V", "bb1:bp.1", "red", [ "h-19.2", "v135.3" ] ],
    [ "nano:GND.1", "bb1:bn.1", "black", [ "v0" ] ],
    [ "nano:2", "bb1:2t.a", "orange", [ "h86.4" ] ],
    [ "nano:3", "bb1:3t.a", "orange", [ "h38.4", "v-57.6", "h57.6" ] ],
    [ "nano:4", "bb1:4t.a", "orange", [ "h28.8", "v-57.6", "h76.8" ] ],
    [ "nano:5", "bb1:5t.a", "orange", [ "h19.2", "v-57.6", "h96" ] ],
    [ "nano:6", "bb1:6t.a", "green", [ "h124.8", "v9.6" ] ],
    [ "nano:7", "bb1:7t.a", "orange", [ "h9.6", "v-48", "h124.8" ] ],
    [ "nano:8", "bb1:8t.a", "orange", [ "h9.6", "v-48", "h172.8" ] ],
    [ "bb1:2b.j", "bb1:23t.a", "#8f4814", [ "h-38.4", "v-182.4", "h240" ] ],
    [ "bb1:24t.a", "bb1:3b.j", "green", [ "v-86.4", "h-249.6", "v-19.2" ] ],
    [ "bb1:4b.j", "bb1:23b.j", "green", [ "v76.8", "h182.4" ] ],
    [ "bb1:5b.j", "bb1:21b.j", "green", [ "v57.6", "h153.6" ] ],
    [ "bb1:6b.j", "bb1:20b.j", "green", [ "v48", "h134.4" ] ],
    [ "bb1:7b.j", "bb1:21t.b", "green", [ "v9.6", "h28.8", "v-134.4" ] ],
    [ "bb1:20t.b", "bb1:8b.j", "green", [ "v-19.2", "h-86.4", "v124.8", "h-28.8" ] ],
    [ "bb1:23t.a", "bb1:29t.a", "green", [ "v-9.6", "h57.6" ] ],
    [ "bb1:30t.a", "bb1:24t.a", "green", [ "v-19.2", "h-57.6" ] ],
    [ "bb1:23b.j", "bb1:29b.j", "green", [ "v9.6", "h57.6" ] ],
    [ "bb1:27b.j", "bb1:21b.j", "green", [ "v19.2", "h-48" ] ],
    [ "bb1:26b.j", "bb1:20b.j", "green", [ "v67.2", "h-57.6" ] ],
    [ "bb1:21t.b", "bb1:27t.a", "green", [ "v-67.2", "h57.6" ] ],
    [ "bb1:26t.a", "bb1:20t.b", "green", [ "v-67.2", "h-57.6" ] ],
    [ "bb1:bn.18", "bb1:22b.j", "black", [ "v0" ] ],
    [ "bb1:22t.b", "bb1:28t.b", "green", [ "v0" ] ],
    [ "r1:1", "bb1:2t.e", "", [ "$bb" ] ],
    [ "r1:2", "bb1:2b.i", "", [ "$bb" ] ],
    [ "r2:1", "bb1:3t.e", "", [ "$bb" ] ],
    [ "r2:2", "bb1:3b.i", "", [ "$bb" ] ],
    [ "r3:1", "bb1:4t.e", "", [ "$bb" ] ],
    [ "r3:2", "bb1:4b.i", "", [ "$bb" ] ],
    [ "r4:1", "bb1:5t.e", "", [ "$bb" ] ],
    [ "r4:2", "bb1:5b.i", "", [ "$bb" ] ],
    [ "r5:1", "bb1:6t.e", "", [ "$bb" ] ],
    [ "r5:2", "bb1:6b.i", "", [ "$bb" ] ],
    [ "r6:1", "bb1:7t.e", "", [ "$bb" ] ],
    [ "r6:2", "bb1:7b.i", "", [ "$bb" ] ],
    [ "r7:1", "bb1:8t.e", "", [ "$bb" ] ],
    [ "r7:2", "bb1:8b.i", "", [ "$bb" ] ],
    [ "sevseg1:COM.1", "bb1:28b.h", "", [ "$bb" ] ],
    [ "sevseg1:COM.2", "bb1:28t.c", "", [ "$bb" ] ],
    [ "sevseg1:A", "bb1:29t.c", "", [ "$bb" ] ],
    [ "sevseg1:B", "bb1:30t.c", "", [ "$bb" ] ],
    [ "sevseg1:C", "bb1:29b.h", "", [ "$bb" ] ],
    [ "sevseg1:D", "bb1:27b.h", "", [ "$bb" ] ],
    [ "sevseg1:E", "bb1:26b.h", "", [ "$bb" ] ],
    [ "sevseg1:F", "bb1:27t.c", "", [ "$bb" ] ],
    [ "sevseg1:G", "bb1:26t.c", "", [ "$bb" ] ],
    [ "sevseg1:DP", "bb1:30b.h", "", [ "$bb" ] ],
    [ "sevseg2:COM.1", "bb1:22b.h", "", [ "$bb" ] ],
    [ "sevseg2:COM.2", "bb1:22t.c", "", [ "$bb" ] ],
    [ "sevseg2:A", "bb1:23t.c", "", [ "$bb" ] ],
    [ "sevseg2:B", "bb1:24t.c", "", [ "$bb" ] ],
    [ "sevseg2:C", "bb1:23b.h", "", [ "$bb" ] ],
    [ "sevseg2:D", "bb1:21b.h", "", [ "$bb" ] ],
    [ "sevseg2:E", "bb1:20b.h", "", [ "$bb" ] ],
    [ "sevseg2:F", "bb1:21t.c", "", [ "$bb" ] ],
    [ "sevseg2:G", "bb1:20t.c", "", [ "$bb" ] ],
    [ "sevseg2:DP", "bb1:24b.h", "", [ "$bb" ] ],
    [ "nano:10", "r8:1", "green", [ "h9.6", "v-57.6", "h-76.8", "v422.4" ] ],
    [ "r9:1", "nano:9", "green", [ "v-9.6", "h-76.8", "v-364.8", "h76.8" ] ],
    [ "r9:2", "chip1:GND", "green", [ "v0" ] ],
    [ "r8:2", "chip2:GND", "green", [ "v0" ] ],
    [ "chip1:OUT", "bb1:22b.j", "green", [ "h97.81" ] ],
    [ "chip1:IN", "bb1:bn.20", "green", [ "v0", "h107.41" ] ],
    [ "chip2:OUT", "bb1:28b.j", "green", [ "h174.61" ] ],
    [ "bb1:bn.25", "chip2:IN", "black", [ "v161.9", "h-8" ] ],
    [ "r9:2", "chip1:BASE", "green", [ "v0" ] ],
    [ "r8:2", "chip2:BASE", "green", [ "v0", "h27.6" ] ],
    [ "chip1:EMI", "bb1:bn.20", "green", [ "v0", "h126.61" ] ],
    [ "chip1:COL", "bb1:22b.j", "green", [ "h97.81", "v-9.6" ] ],
    [ "chip2:COL", "bb1:28b.j", "green", [ "h165.01" ] ],
    [ "chip2:EMI", "bb1:bn.25", "green", [ "v0", "h165.01" ] ]
  ],
  "serialMonitor": { "display": "auto" },
  "dependencies": {}
}'''

diag = json.loads(diag_text)
print("Parts:", len(diag["parts"]))
print("Connections:", len(diag["connections"]))

# Let's build a graph to find which Arduino Nano pin connects to which display segment!
# On breadboard:
# Columns 1-30, 't' (top rows a-e) are connected together in column i (e.g. bb1:2t.a to bb1:2t.e are in same row/col)
# 'b' (bottom rows f-j) are connected together in column i (e.g. bb1:2b.f to bb1:2b.j)
# Let's map breadboard nodes to electrical nets!

adj = {}
def add_edge(u, v):
    adj.setdefault(u, set()).add(v)
    adj.setdefault(v, set()).add(u)

# Resistors:
# r1: 1 -> bb1:2t.e, 2 -> bb1:2b.i. So r1 connects bb1:2t to bb1:2b!
# Let's add direct connection or treat resistor as passing signal
# Connections in diagram:
for c in diag["connections"]:
    u, v = c[0], c[1]
    add_edge(u, v)

# Add breadboard internal connections:
# For col 1..30:
for col in range(1, 31):
    # top: a,b,c,d,e
    top_pins = [f"bb1:{col}t.{r}" for r in "abcde"]
    for i in range(len(top_pins)-1):
        add_edge(top_pins[i], top_pins[i+1])
    # bottom: f,g,h,i,j
    bot_pins = [f"bb1:{col}b.{r}" for r in "fghij"]
    for i in range(len(bot_pins)-1):
        add_edge(bot_pins[i], bot_pins[i+1])

# Resistors r1-r7:
for i, r in enumerate(["r1", "r2", "r3", "r4", "r5", "r6", "r7"], start=1):
    add_edge(f"{r}:1", f"{r}:2") # through resistor

# Resistors r8, r9:
add_edge("r8:1", "r8:2")
add_edge("r9:1", "r9:2")

# Now let's find connected components!
visited = set()
nets = []
for node in adj:
    if node not in visited:
        comp = []
        q = [node]
        visited.add(node)
        for curr in q:
            comp.append(curr)
            for nxt in adj.get(curr, []):
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        nets.append(comp)

print("\n--- TRACING ARDUINO PINS TO SEGMENTS ---")
for pin in ["nano:2", "nano:3", "nano:4", "nano:5", "nano:6", "nano:7", "nano:8", "nano:9", "nano:10"]:
    for net in nets:
        if pin in net:
            # find all sevseg pins in this net
            s1_pins = [x for x in net if x.startswith("sevseg1:")]
            s2_pins = [x for x in net if x.startswith("sevseg2:")]
            chips = [x for x in net if "chip" in x]
            print(f"{pin} -> sevseg1: {s1_pins}, sevseg2: {s2_pins}, chips: {chips}")

print("\n--- TRACING SEVSEG COM PINS ---")
for com in ["sevseg1:COM.1", "sevseg2:COM.1"]:
    for net in nets:
        if com in net:
            nano_pins = [x for x in net if x.startswith("nano:")]
            chips = [x for x in net if "chip" in x]
            ground = [x for x in net if "GND" in x or "bn." in x]
            print(f"{com} -> nano: {nano_pins}, chips: {chips}, gnd: {bool(ground)}")
