import sys as s
import json
from tkinter.filedialog import askopenfile as openDlg
from tkinter.filedialog import asksaveasfilename as saveDlg

try:
	with openDlg(title="Choose a Chart", filetypes=[("Chart Json", "json")]) as f: c = json.load(f)
	with openDlg(title="Pick the Chart Metadata accordingly", filetypes=[("Chart Metadata Json (-metatdata)", "json")]) as mF: m = json.load(mF)
except:
	print("An unexpected error ocurred or no chart was choosen.")
	s.exit(127)

def repeatInput(msg: str) -> str:
	inputVar = ""
	while inputVar == "": inputVar = input(msg)
	return inputVar

# Someone, please make this part better - [
diff = repeatInput("Difficulty to convert: ").lower()
while not diff in c['notes']:
	print("\n'" + diff.capitalize() + "' difficulty doesn't exist in chart! Try again.")
	diff = repeatInput("Difficulty to convert: ").lower() # ]

sepVcls = bool(repeatInput("Split Vocals (true/false): "))

# The conversion happens bellow, edit it only if you know what you're doing

tmpJ = {"events": [], "scrollSpeed": c['scrollSpeed'][diff], "codenameChart": True, "strumLines": [], "noteTypes": []}

pS = {
	"notes": [],
	"position": "boyfriend",
	"type": 1,
	"characters": [str.removesuffix(m['playData']['characters']['player'], "-playable")],
	"strumLinePos": 0.7
}
oS = {
	"notes": [],
	"position": "dad",
	"type": 0,
	"characters": [m['playData']['characters']['opponent']],
	"strumLinePos": 0.2
}

if sepVcls:
	for s in [pS, oS]: s["vocalsSuffix"] = "-" + s["characters"][0]

for n in c['notes'][diff]:
	tS = 				 oS if n['d'] >= 4 else pS
	tD = n['d'] - 4 if n['d'] >= 4 else n['d']

	cN = {"time": n['t'], "id": tD}
	if 'l' in n and n['l'] != 0: cN["sLen"] = n['l']

	list.append(tS["notes"], cN)
	# print('add note ' + str(n) + ' to ' + tS['position'] + ' strumline')

for e in c['events']:
	if e['e'] != "FocusCamera": break

	match e['v']['char']:
		case 2: tC = e['v']['char']
		case _: tC = 1 - e['v']['char']

	list.append(tmpJ["events"], {"name": "Camera Movement", "params": [tC], "time": e['t']})

list.append(tmpJ['strumLines'], oS)
list.append(tmpJ['strumLines'], pS)
if 'girlfriend' in m['playData']['characters'] and str.lower(m['playData']['characters']['girlfriend']) != "none":
	list.append(tmpJ['strumLines'], {
		"visible": False,
		"position": "girlfriend",
		"type": 2,
		"characters": [m['playData']['characters']['girlfriend']]
	})

indent = int(repeatInput("Identation (tab spacing) to use: "))
with open(saveDlg(initialfile=diff + ".json", title="Save the Converted Chart", filetypes=[("Chart Json", "json")], confirmoverwrite=False), mode="w", encoding="utf-8") as fF:
	json.dump(tmpJ, fF, ensure_ascii=False, indent=indent)