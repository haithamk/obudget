import sys
import csv
import re
from budget_lines.models import BudgetLine 
from django.core.management.base import BaseCommand
import json

class Command(BaseCommand):

    args = '<jsons-file> <jsons-file> ...'
    help = 'Transfers a sorted jsons budget data files into the DB'

    def handle(self, *args, **options):

        print 'Loading raw rows'
        k = 0
        for filename in args:
            print filename
            for l in file(filename).readlines():
                d = json.loads(l)
                bl = BudgetLine( budget_id=d['code'],
                                 year = d['year'],
                                 title = d['title'],
                                 net_amount_allocated = d.get('net_allocated'),
                                 net_amount_revised = d.get('net_revised'),
                                 net_amount_used = d.get('net_used'),
                                 gross_amount_allocated = d.get('gross_allocated'),
                                 gross_amount_revised = d.get('gross_revised'),
                                 gross_amount_used = d.get('gross_used'),
                                 budget_id_len = len(d['code'])
                                 )
                bl.save()
                if bl.budget_id_len == 2:        
                    continue
                
                for i in range(2,bl.budget_id_len,2):
                    parent_budget_id  = bl.budget_id[:-i]
                    try:
                        parent = BudgetLine.objects.get( year = bl.year, budget_id = parent_budget_id, budget_id_len = len(parent_budget_id) )
                        bl.containing_line = parent
                        bl.save()
                        break
                    except:
                        continue

                k+=1
                if k % 1000 == 0:
                    print k
        
