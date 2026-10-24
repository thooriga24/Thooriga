"""Evaluate completed human judgments; no fixture scores or synthetic relevance labels."""
import argparse
import csv
import json
import math
from collections import defaultdict
from statistics import mean

def evaluate(rows, k):
    grouped=defaultdict(list)
    for row in rows:
        row['human_relevance']=int(row['human_relevance'])
        if row['human_relevance'] not in (0,1,2): raise ValueError('Human relevance must be 0, 1 or 2')
        for method in ('baseline','gemma'):
            row[method+'_rank']=int(row[method+'_rank'])
            if row[method+'_rank']<1: raise ValueError('Ranks start at 1')
        grouped[row['brief_id']].append(row)
    report={}
    for brief, candidates in grouped.items():
        if len(candidates)<k: raise ValueError(f'{brief}: fewer than k judged photos')
        report[brief]={}
        ideal=sorted((x['human_relevance'] for x in candidates),reverse=True)[:k]
        def dcg(values): return sum((2**v-1)/math.log2(i+2) for i,v in enumerate(values))
        for method in ('baseline','gemma'):
            ranks=[r[method+'_rank'] for r in candidates]
            if len(set(ranks))!=len(ranks): raise ValueError('Rank ties must be resolved before evaluation')
            top=sorted(candidates,key=lambda x:x[method+'_rank'])[:k]
            report[brief][method]={'precision_at_k':sum(x['human_relevance']==2 for x in top)/k,'ndcg_at_k':dcg([x['human_relevance'] for x in top])/dcg(ideal) if dcg(ideal) else 0}
    macro={method:{metric:mean(r[method][metric] for r in report.values()) for metric in ('precision_at_k','ndcg_at_k')} for method in ('baseline','gemma')}
    return {'k':k,'judgments':len(rows),'per_brief':report,'macro':macro}

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('csv'); parser.add_argument('--k',type=int,default=3); args=parser.parse_args()
    if args.k<1: parser.error('k must be positive')
    with open(args.csv,newline='',encoding='utf-8') as file: rows=list(csv.DictReader(file))
    if not rows: parser.error('Supply actual completed judgments; template has no results')
    print(json.dumps(evaluate(rows,args.k),indent=2))
