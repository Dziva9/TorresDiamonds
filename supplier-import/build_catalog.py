from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json,re,html,csv,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1]
IMPORT=ROOT/'supplier-import'
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,d):self.parts.append(d)
def clean(s):
 p=Text();p.feed(s);return re.sub(r'\s+',' ',' '.join(p.parts)).strip()
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
records=[]
for file in [IMPORT/'imported-products.json',*sorted(IMPORT.glob('imported-[0-9]*.json'))]:
 records.extend(json.loads(file.read_text()))
# Later successful retries replace earlier failed entries.
byindex={r['index']:r for r in records}
for repair in sorted(IMPORT.glob('repaired-*.json')):
 for r in json.loads(repair.read_text()):
  if r.get('url') and r.get('photos'):byindex[r['index']]=r
records=sorted(byindex.values(),key=lambda x:x['index'])
unique={};failed=[]
for r in records:
 if not r.get('url') or not r.get('photos'):
  failed.append({'index':r['index'],'title':r['title'],'url':r.get('url'),'photos':len(r.get('photos',[]))});continue
 handle=urlparse(r['url']).path.split('/products/')[-1].strip('/')
 if handle not in unique or len(r['photos'])>len(unique[handle]['photos']):unique[handle]=r
places=['Harbour','Cove','Northline','Seabright','Cascade','Solara','Tidal','Vista','Aurelia','Lumin','Sierra','Valora','Shoreline','Marina','Summit','Horizon','Isla','Beacon','Crest','Arc']
seen_names=set();products=[]
labels=['Total carat','Total diamond weight','Centre stone','Center stone','Centre diamond','Center diamond','Accent diamonds','Side stones','Stone count','Stone size','Shape','Cut','Setting','Color grade','Colour grade','Color','Colour','Clarity grade','Clarity','Certification','Diamond type','Metal options','Metal','Finish','Clasp','Length','Width','Dimensions','Weight','Sizing','Production']
pattern=re.compile(r'\b('+'|'.join(re.escape(x) for x in sorted(labels,key=len,reverse=True))+r')\s+',re.I)
for n,(handle,r) in enumerate(unique.items()):
 title=html.unescape(r['title']);low=title.lower();raw=r['raw']
 lines=[re.sub(r'^L\d+:\s*','',x).strip() for x in raw.splitlines() if re.match(r'^L\d+:',x)]
 facts=[];spec=''
 for i,line in enumerate(lines):
  if line.startswith('Full Specifications'):
   spec=next((x for x in lines[i+1:i+5] if x and not x.startswith('【')),'');break
 matches=list(pattern.finditer(spec))
 parsed={}
 for i,m in enumerate(matches):
  value=spec[m.end():matches[i+1].start() if i+1<len(matches) else len(spec)].strip(' ·|')
  if value and len(value)<180:parsed[m.group(1).lower()]=value
 if 'bracelet' in low:cat='tennis';kind='Bracelet'
 elif re.search(r'earring|\bstuds?\b|\bhoop',low):cat='earrings';kind='Earrings'
 elif re.search(r'necklace|\bchain\b|pendant|lariat',low):cat='chains';kind='Necklace' if re.search(r'necklace|chain|lariat',low) else 'Pendant'
 elif re.search(r'\bring|\bband|bridal',low):cat='engagement' if re.search(r'engagement|bridal|solitaire',low) else 'rings';kind='Ring'
 else:cat='custom';kind='Atelier Piece'
 shapes=[x for x in ['Round','Oval','Emerald','Radiant','Pear','Marquise','Princess','Cushion','Asscher','Baguette','Heart'] if re.search(r'\b'+x+r'\b',title,re.I)]
 shape=shapes[0] if shapes else ''
 design=next((label for rx,label in [(r'toi et moi|two stone|two.stone','Toi et Moi'),(r'hidden halo','Hidden Halo'),(r'tapered baguette','Baguette Trilogy'),(r'shield side','Shield Trilogy'),(r'five.stone|5.stone','Five-Stone'),(r'seven.stone|7.stone','Seven-Stone'),(r'clover|pear cluster','Clover'),(r'cluster','Cluster'),(r'vine','Vine'),(r'twist','Twist'),(r'bezel','Bezel'),(r'eternity','Eternity'),(r'halo','Halo'),(r'cuban','Cuban Link'),(r'lariat|y drop','Lariat'),(r'cross','Cross'),(r'butterfly','Butterfly'),(r'heart','Heart'),(r'ankh','Ankh'),(r'angel','Angel Wing'),(r'dog tag','Tag'),(r'shark','Shark'),(r'gaming','Arcade'),(r'boxing','Boxing'),(r'bunny','Rabbit'),(r'greek key','Key'),(r'portrait','Portrait'),(r'skull','Skull'),(r'guadalupe','Devotion') ] if re.search(rx,low)), '')
 weight_match=re.search(r'(\d+(?:\.\d+)?\s*ctw?|\d+(?:\.\d+)?\s*carat)',title,re.I)
 weight=re.sub(r'\s+','',weight_match.group(1)).lower() if weight_match else ''
 if 'bridal' in low:kind='Bridal Set'
 if cat=='earrings':kind='Studs' if 'stud' in low else ('Hoops' if 'hoop' in low else 'Drop Earrings')
 if cat=='tennis' and not design:kind='Tennis Bracelet'
 if cat=='chains' and 'tennis' in low:kind='Tennis Chain' if 'chain' in low else 'Tennis Necklace'
 colour=next((val for rx,val in [(r'fancy.*blue|\bblue\b','Blue'),(r'fancy.*pink|\bpink\b','Pink'),(r'fancy.*yellow|\byellow diamond','Yellow'),(r'\bred\b','Red'),(r'\bblack\b','Black'),(r'\bruby\b','Ruby'),(r'\bsapphire\b','Sapphire'),(r'\bcognac\b','Cognac')] if re.search(rx,low)), '')
 if cat=='custom':name='Torres Atelier Commission '+str(n+1).zfill(2)
 else:
  place=places[n%len(places)]
  bits=[place,colour,shape if shape.lower() not in design.lower() else '',design,kind]
  name=' '.join(x for x in bits if x)
  if weight:name+=' — '+weight
 if name in seen_names:name+=' No. '+str(n+1)
 seen_names.add(name)
 for keys,label in [(['total carat','total diamond weight'],'Total diamond weight'),(['centre stone','center stone','centre diamond','center diamond'],'Centre stone'),(['accent diamonds'],'Accent diamonds'),(['side stones'],'Side stones'),(['stone count'],'Stone count'),(['shape','cut'],'Diamond shape / cut'),(['setting'],'Setting'),(['color grade','colour grade','color','colour'],'Colour'),(['clarity grade','clarity'],'Clarity'),(['certification'],'Grading documentation'),(['finish'],'Finish'),(['clasp'],'Clasp'),(['length'],'Length'),(['width'],'Width')]:
  value=next((parsed[k] for k in keys if k in parsed),None)
  if value:facts.append([label,value])
 if not facts:
  if weight:facts.append(['Advertised diamond weight',weight])
  if shape:facts.append(['Diamond shape',shape])
 if 'lab' in low:facts.append(['Diamond origin','Laboratory-grown'])
 metals=[]
 material=parsed.get('metal options','') or title
 for rx,label in [(r'\bsilver\b','Silver'),(r'\b10k\b','10K Gold'),(r'\b14k\b|10k.18k','14K Gold'),(r'\b18k\b','18K Gold'),(r'\bplatinum\b','Platinum')]:
  if re.search(rx,material,re.I):metals.append(label)
 if not metals:metals=['Confirm available metal']
 # Brand warranties, competitor comparisons, reviews and copy are intentionally not reused.
 shapephrase=(shape.lower()+'-cut ') if shape else ''
 if kind=='Bridal Set':description='A coordinated ring and band design featuring '+shapephrase+'diamonds. Explore the profile, setting and overall proportions, then discuss the metal and sizing that suit your plans.'
 elif cat in ['rings','engagement']:description='A '+shapephrase+'diamond ring with '+(design.lower()+' detailing' if design else 'a distinctive setting')+'. Compare its silhouette and side profile, and explore your preferred metal and ring size.'
 elif cat=='tennis':description='A '+(shape.lower()+'-cut ' if shape else '')+'diamond bracelet with '+(design.lower()+' detailing' if design else 'a continuous line of stones')+'. Compare total diamond weight, wrist fit and the clasp before choosing your configuration.'
 elif cat=='earrings':description='A pair of '+shapephrase+'diamond '+kind.lower()+'. Explore the setting and on-ear proportions. Where a total carat weight is listed for the pair, it describes both earrings together.'
 elif cat=='chains':description='A diamond '+kind.lower()+' with '+(design.lower()+' detailing' if design else 'a considered line of stones')+'. Compare the silhouette, dimensions and available metals, and confirm the chain length and what is included with the piece.'
 else:description='An individual design from the supplier’s advertised custom catalogue, renamed for the Torres demo. Ask about availability and specifications before considering a similar commission.'
 short=' · '.join(x for x in [weight+' advertised' if weight else '',shape+' cut' if shape else '',design] if x)
 if not short:short=kind+' · Specifications to be confirmed'
 # Prefer the product detail page price over older collection-card snapshots.
 pm=re.search(r'L\d+:\s*Sale price\$([\d,]+(?:\.\d+)?)',raw)
 if not pm:pm=re.search(r'\$([\d,]+(?:\.\d+)?)',r.get('price',''))
 price=float(pm.group(1).replace(',','')) if pm else None
 categories=[cat]
 if cat=='engagement':categories.append('rings')
 if cat=='rings' and re.search(r'halo|solitaire|three.stone|toi et moi',low):categories.append('engagement')
 available=not re.search(r'L\d+:.*\[Button: Sold out\]',raw)
 imgs=[]
 for url in r['photos']:
  url=url.rstrip(':,.;')
  if 'packaging' in url.lower():continue
  # Multiple render widths of one file do not constitute additional views.
  base=url.split('?')[0]
  if not any(x.split('?')[0]==base for x in imgs):imgs.append(url)
 products.append({'id':slug(name),'name':name,'category':cat,'categories':categories,'shortSpec':short,'description':description,'price':price,'available':available,'photos':imgs,'facts':facts,'metals':metals,'searchText':' '.join([shape,design,colour,kind,*metals]),'sourceUrl':r['url'],'sourceName':title,'sourceHandle':handle,'capturedDate':'2026-10-18'})
(ROOT/'assets/full-catalog.json').write_text(json.dumps(products,ensure_ascii=False,indent=2))
(ROOT/'inventory-data.js').write_text('window.TORRES_CATALOG='+json.dumps(products,ensure_ascii=False,separators=(',',':'))+';\n')
with (ROOT/'assets/catalog-review.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Keep?','Torres name','Category','Demo reference price CAD','Availability in source','Supplier listing','Supplier product URL','Photo URLs','Notes'])
 for p in products:w.writerow(['',p['name'],p['category'],p['price'],'Available' if p['available'] else 'Unavailable',p['sourceName'],p['sourceUrl'],' | '.join(p['photos']),''])
report={'imported_records':len(records),'unique_products_with_photos':len(products),'unresolved':failed,'deduplicated_records':len(records)-len(failed)-len(products),'photos':sum(len(x['photos']) for x in products),'by_category':{k:sum(x['category']==k for x in products) for k in ['engagement','rings','tennis','earrings','chains','custom']}}
(IMPORT/'audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
