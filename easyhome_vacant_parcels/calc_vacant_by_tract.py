import pyogrio,glob,json,re,pandas as pd,geopandas as gpd
tr=gpd.GeoDataFrame.from_features(json.load(open('/tmp/claude-0/tracts.json'))['features'],crs=4326)
PUB=re.compile(r'\b(CITY OF|COUNTY|STATE OF|TEXAS DEPT|TXDOT|ISD|INDEPENDENT SCHOOL|SCHOOL DIST|HOA|HOMEOWNER|PROPERTY OWNERS|POA|HOME OWNERS|ASSOC|MUD|WCID|WATER|UTILIT|ELECTRIC|CPS|SAWS|UNITED STATES|U S A|USA|AIR FORCE|DEPT|DEPARTMENT|HOUSING AUTH|DISTRICT|CHURCH|CEMETERY|PUBLIC|AUTHORITY|SAN ANTONIO RIVER|UNION PACIFIC|RAILROAD)\b',re.I)
out=[]
for g in sorted(set(glob.glob('/tmp/claude-0/dl/*/fgdb/*.gdb'))):
    d=pyogrio.read_dataframe(g,columns=['OWNER_NAME','IMP_VALUE','LAND_VALUE'])
    d['pt']=d.geometry.representative_point() if False else d.geometry.centroid
    p=gpd.GeoDataFrame(d.drop(columns='geometry'),geometry='pt',crs=4326)
    j=gpd.sjoin(p,tr[['GEOID','geometry']],predicate='within',how='inner')
    j=j[j.LAND_VALUE>1000]
    own=j.OWNER_NAME.fillna('')
    j['vac']=(j.IMP_VALUE.fillna(0)==0)&(~own.str.contains(PUB))
    out.append(j.groupby('GEOID').vac.agg(['sum','count']))
    print(g.split('/')[-1][:40],len(j),int(j.vac.sum()),flush=True)
r=pd.concat(out).groupby(level=0).sum(); r.columns=['vacant','total']
r['pct']=100*r.vacant/r.total
r.to_csv('/tmp/claude-0/vacant.csv'); print(len(r),r.describe())
