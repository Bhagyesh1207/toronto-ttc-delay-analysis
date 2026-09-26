"""Download City of Toronto TTC data and build a reproducible SQLite analysis."""
import argparse
import hashlib
import sqlite3
from pathlib import Path
from urllib.request import urlopen

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
CHARTS = ROOT / 'charts'
CUTOFF = '2026-08-31'
URLS = {
 'delays': 'https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/0b6e5c52-e993-46d6-8d74-8602ee224457/download/ttc-subway-delay-data-since-2025.csv',
 'codes': 'https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/b2d8f5e0-0997-46b5-8abd-caa685a0290b/download/code-descriptions.csv',
}

def fetch(force=False):
 DATA.mkdir(exist_ok=True)
 for name, url in URLS.items():
  path = DATA / f'{name}.csv'
  if not path.exists() or force:
   with urlopen(url, timeout=45) as response:
    path.write_bytes(response.read())
  print(f'{name}: {path.stat().st_size:,} bytes, SHA-256 {hashlib.sha256(path.read_bytes()).hexdigest()}')

def build():
 raw = pd.read_csv(DATA / 'delays.csv', dtype={'Code':'string','Line':'string','Station':'string','Bound':'string'})
 codes = pd.read_csv(DATA / 'codes.csv', dtype={'CODE':'string','DESCRIPTION':'string'})
 raw = raw.loc[raw['Date'] <= CUTOFF].copy()
 # The municipal feed has multiple incident records that can look alike; do not deduplicate without an incident key.
 raw['incident_id'] = pd.to_numeric(raw['_id'], errors='coerce')
 raw['date'] = pd.to_datetime(raw['Date'], errors='coerce')
 raw['time'] = raw['Time'].astype(str).str.strip()
 raw['hour'] = pd.to_numeric(raw['time'].str.extract(r'^(\d{1,2}):')[0], errors='coerce')
 raw['code'] = raw['Code'].str.strip().str.upper()
 raw['line_raw'] = raw['Line'].str.strip().str.upper()
 raw['station'] = raw['Station'].str.strip().str.upper()
 raw['delay_min'] = pd.to_numeric(raw['Min Delay'], errors='coerce')
 raw['gap_min'] = pd.to_numeric(raw['Min Gap'], errors='coerce')
 raw['line'] = raw['line_raw'].map({'YU':'Line 1','BD':'Line 2','SHP':'Line 4'})
 raw['is_usable'] = (raw['date'].notna() & raw['hour'].between(0,23) & raw['delay_min'].ge(0) & raw['line'].notna())
 raw['exclude_reason'] = ''
 raw.loc[raw['date'].isna() | ~raw['hour'].between(0,23), 'exclude_reason'] = 'invalid date/time'
 raw.loc[~raw['delay_min'].ge(0), 'exclude_reason'] = 'invalid delay'
 raw.loc[raw['line'].isna() & raw['exclude_reason'].eq(''), 'exclude_reason'] = 'line not one of YU/BD/SHP'
 clean = raw.loc[raw['is_usable'], ['incident_id','date','hour','station','code','line','delay_min','gap_min']].copy()
 clean['date'] = clean['date'].dt.strftime('%Y-%m-%d')
 clean['is_positive_delay'] = (clean.delay_min > 0).astype(int)
 clean['is_peak'] = clean.hour.between(7,9) | clean.hour.between(16,18)
 clean['is_peak'] = clean['is_peak'].astype(int)
 codes['code'] = codes['CODE'].str.strip().str.upper()
 codes['description'] = codes['DESCRIPTION'].str.replace('â€“', '-', regex=False).str.replace('â€', '-', regex=False).str.strip()
 codes = codes[['code','description']].drop_duplicates('code')
 # Keep source IDs and all valid rows, including zero-minute records. A zero is not a missing value.
 db = DATA / 'ttc_analysis.sqlite'
 with sqlite3.connect(db) as conn:
  clean.to_sql('incidents',conn,if_exists='replace',index=False)
  codes.to_sql('delay_codes',conn,if_exists='replace',index=False)
  conn.executescript('CREATE INDEX idx_inc_date ON incidents(date); CREATE INDEX idx_inc_line ON incidents(line); CREATE INDEX idx_inc_code ON incidents(code);')
  sql=(ROOT/'sql'/'analysis.sql').read_text()
  sections=sql.split('-- QUERY: ')[1:]
  print(f'Rows: raw={len(raw):,}, retained={len(clean):,}, positive delays={int(clean.is_positive_delay.sum()):,}, excluded={len(raw)-len(clean):,}')
  print('Excluded reasons:',raw.loc[~raw.is_usable,'exclude_reason'].value_counts().to_dict())
  print('Unmapped codes in clean rows:',len(set(clean.code)-set(codes.code)))
  out=[]
  for section in sections:
   name,statement=section.split('\n',1)
   table=pd.read_sql_query(statement.strip(),conn)
   out.append(f'## {name}\n\n'+table.to_markdown(index=False))
  (DATA/'results.md').write_text('\n\n'.join(out)+'\n')
  monthly=pd.read_sql_query('SELECT substr(date,1,7) month, line, SUM(delay_min) minutes FROM incidents GROUP BY 1,2 ORDER BY 1,2',conn)
  CHARTS.mkdir(exist_ok=True)
  fig,ax=plt.subplots(figsize=(11,5.5));fig.patch.set_facecolor('#f7f8fa');ax.set_facecolor('#f7f8fa')
  for line,g in monthly.groupby('line'):
   ax.plot(pd.to_datetime(g.month),g.minutes,marker='o',markersize=3,label=line,linewidth=2)
  ax.set_title('Recorded subway delay minutes by month',loc='left',fontsize=17,fontweight='bold',pad=18)
  ax.set_ylabel('Minutes recorded');ax.set_xlabel('Month');ax.legend(frameon=False,ncol=3);ax.grid(axis='y',alpha=.2)
  ax.spines[['top','right']].set_visible(False);fig.autofmt_xdate();fig.tight_layout();fig.savefig(CHARTS/'monthly-delay-minutes.svg',dpi=160);plt.close(fig)
  hourly=pd.read_sql_query('SELECT hour, COUNT(*) incidents, SUM(is_positive_delay) positive_events FROM incidents GROUP BY hour ORDER BY hour',conn)
  fig,ax=plt.subplots(figsize=(10,5));fig.patch.set_facecolor('#f7f8fa');ax.set_facecolor('#f7f8fa')
  ax.bar(hourly.hour,hourly.positive_events,color='#187b99');ax.set_xticks(range(0,24,2));ax.set_ylabel('Positive-delay records');ax.set_xlabel('Recorded hour')
  ax.set_title('Positive-delay records by hour',loc='left',fontsize=17,fontweight='bold',pad=18)
  ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);fig.tight_layout();fig.savefig(CHARTS/'hourly-incidents.svg',dpi=160);plt.close(fig)
 print('Wrote',db,DATA/'results.md')

if __name__ == '__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--refresh',action='store_true',help='redownload resources');args=parser.parse_args()
 fetch(args.refresh);build()
