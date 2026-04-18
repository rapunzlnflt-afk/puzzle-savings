import re
import os

# Read source
with open('/home/user/workspace/puzzle-savings/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# a. Change title
html = re.sub(r'<title>.*?</title>', '<title>Puzzle Pig — Demo</title>', html)

# b. Replace IndexedDB block with in-memory store
indexeddb_pattern = r'// ---- IndexedDB ----.*?function dbGetAllChoreLogs\(\) \{.*?\n\}'
indexeddb_replacement = """// ---- IndexedDB (Demo: in-memory) ----
let _memGoals = []; let _memUsers = []; let _memSettings = {};
let _memJars = []; let _memJarTxs = []; let _memChores = []; let _memChoreLogs = [];
function openDB(){ return Promise.resolve(); }
function dbGetAll(){ return Promise.resolve([..._memGoals.map(g=>JSON.parse(JSON.stringify(g)))]); }
function dbPut(g){ const i = _memGoals.findIndex(x=>x.id===g.id); if(i>=0) _memGoals[i]=JSON.parse(JSON.stringify(g)); else _memGoals.push(JSON.parse(JSON.stringify(g))); return Promise.resolve(); }
function dbDelete(id){ _memGoals = _memGoals.filter(g=>g.id!==id); return Promise.resolve(); }
function dbGetAllUsers(){ return Promise.resolve([..._memUsers.map(u=>({...u}))]); }
function dbPutUser(u){ const i = _memUsers.findIndex(x=>x.id===u.id); if(i>=0) _memUsers[i]={...u}; else _memUsers.push({...u}); return Promise.resolve(); }
function dbDeleteUser(id){ _memUsers = _memUsers.filter(u=>u.id!==id); return Promise.resolve(); }
function dbGetSetting(k){ return Promise.resolve(_memSettings[k] !== undefined ? _memSettings[k] : null); }
function dbPutSetting(key, value){ _memSettings[key] = value; return Promise.resolve(); }
function dbPutJar(j){ const i = _memJars.findIndex(x=>x.id===j.id); if(i>=0) _memJars[i]=JSON.parse(JSON.stringify(j)); else _memJars.push(JSON.parse(JSON.stringify(j))); return Promise.resolve(); }
function dbDeleteJar(id){ _memJars = _memJars.filter(j=>j.id!==id); return Promise.resolve(); }
function dbGetAllJars(){ return Promise.resolve([..._memJars.map(j=>JSON.parse(JSON.stringify(j)))]); }
function dbPutJarTx(t){ const i = _memJarTxs.findIndex(x=>x.id===t.id); if(i>=0) _memJarTxs[i]=JSON.parse(JSON.stringify(t)); else _memJarTxs.push(JSON.parse(JSON.stringify(t))); return Promise.resolve(); }
function dbGetAllJarTxs(){ return Promise.resolve([..._memJarTxs.map(t=>JSON.parse(JSON.stringify(t)))]); }
function dbPutChore(c){ const i = _memChores.findIndex(x=>x.id===c.id); if(i>=0) _memChores[i]=JSON.parse(JSON.stringify(c)); else _memChores.push(JSON.parse(JSON.stringify(c))); return Promise.resolve(); }
function dbDeleteChore(id){ _memChores = _memChores.filter(c=>c.id!==id); return Promise.resolve(); }
function dbGetAllChores(){ return Promise.resolve([..._memChores.map(c=>JSON.parse(JSON.stringify(c)))]); }
function dbPutChoreLog(e){ const i = _memChoreLogs.findIndex(x=>x.id===e.id); if(i>=0) _memChoreLogs[i]=JSON.parse(JSON.stringify(e)); else _memChoreLogs.push(JSON.parse(JSON.stringify(e))); return Promise.resolve(); }
function dbGetAllChoreLogs(){ return Promise.resolve([..._memChoreLogs.map(e=>JSON.parse(JSON.stringify(e)))]); }"""

result = re.sub(indexeddb_pattern, indexeddb_replacement, html, flags=re.DOTALL)
if result == html:
    print("WARNING: IndexedDB pattern did not match!")
else:
    print("IndexedDB block replaced successfully.")
html = result

# c. Replace PWA block
pwa_pattern = r"// ---- PWA ----.*?document\.querySelector\('link\[rel=\"manifest\"\]'\)\.href = URL\.createObjectURL\(mBlob\);"
pwa_replacement = "// ---- PWA (Demo: disabled) ----"

result = re.sub(pwa_pattern, pwa_replacement, html, flags=re.DOTALL)
if result == html:
    print("WARNING: PWA pattern did not match!")
else:
    print("PWA block replaced successfully.")
html = result

# d. Add demo banner before <!-- ===== USER SELECT SCREEN ===== -->
banner = """<div style="position:fixed;top:0;left:0;right:0;z-index:9999;background:linear-gradient(135deg,#6E6E7E,#D8D8DE,#F4F4F8,#D8D8DE,#6E6E7E);padding:6px 16px;text-align:center;font:600 13px/1.4 'Pally',sans-serif;color:#52525E;letter-spacing:.5px;">DEMO — Data resets on refresh &nbsp;|&nbsp; <a href="https://www.etsy.com/listing/4490566794/puzzle-piggy-kids-savings-tracker-chore" style="color:#7C5AC7;text-decoration:underline;font-weight:700;">Get the Full Version</a></div>
<div style="height:32px;"></div>
"""

marker = '<!-- ===== USER SELECT SCREEN ===== -->'
if marker in html:
    html = html.replace(marker, banner + marker)
    print("Demo banner inserted successfully.")
else:
    print("WARNING: USER SELECT SCREEN marker not found!")

# e. Auto-seed demo data by calling preloadTestData() in init()
# Insert the call right after 'await openDB();' in init()
init_seed = 'await openDB();\n\n  // Demo: auto-seed test data\n  await preloadTestData();'
html = html.replace('await openDB();', init_seed, 1)
print("Demo auto-seed inserted into init().")

# Ensure output directory exists
os.makedirs('/home/user/workspace/puzzle-savings-demo', exist_ok=True)

# Write output
with open('/home/user/workspace/puzzle-savings-demo/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Written to /home/user/workspace/puzzle-savings-demo/index.html")
