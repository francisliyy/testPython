from flask import render_template, make_response, send_file, request
from flask_appbuilder import BaseView, expose, has_access
from app import appbuilder
from .forms import TOBForm
from io import BytesIO
import pandas as pd
import numpy as np
import logging



log = logging.getLogger(__name__)

class MyView(BaseView):

    default_view = 'method1'
    #pd.set_option('display.float_format', lambda x: '%.2f' % x)

    @expose('/method1/')
    @has_access
    def method1(self):
            # do something with param1
            # and return to previous page or index
        return 'Hello'

    @expose('/method2/<string:param1>')
    @has_access
    def method2(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        return param1

    @staticmethod
    def color_negative_red(val):
        """
        Takes a scalar and returns a string with
        the css property `'color: red'` for negative
        strings, black otherwise.
        """
        color = 'red' if val < -5 else 'black'
        return 'color: %s' % color

    @staticmethod
    def comparisons(lastyear, thisyear, lastsim, thissim):

        # define path the different year
        lastyear_path = 'app/data/' + lastyear
        thisyear_path = 'app/data/' + thisyear

        #lastyear 
        lastyear_cr_policy = lastyear_path + '/cr/CRILM_MidHighRise_AggPolicyLosses.txt'
        lastyear_cr_risk = lastyear_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
        lastyear_lr = lastyear_path + '/pr_lr/valid_data.csv'
        lastyear_residential = lastyear_path + '/pr_residential/valid_data.csv'
        lastyear_mobile = lastyear_path + '/pr_mobile/valid_data.csv'
        lastyear_rental = lastyear_path + '/pr_rental/valid_data.csv'
        lastyear_condo = lastyear_path + '/pr_condo/valid_data.csv'

        lastyear_cr_df_policy = pd.read_csv(lastyear_cr_policy)
        lastyear_cr_df_risk = pd.read_csv(lastyear_cr_risk,usecols=['LMs', 'LMapp', 'LMc', 'LMale', 'RiskTotalLoss','Deduc'])        
        lastyear_lr_df = pd.read_csv(lastyear_lr,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss','Deduc'])
        lastyear_residential_df = pd.read_csv(lastyear_residential,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss','Deduc'])
        lastyear_mobile_df = pd.read_csv(lastyear_mobile,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss','Deduc'])
        lastyear_rental_df = pd.read_csv(lastyear_rental,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss','Deduc'])
        lastyear_condo_df = pd.read_csv(lastyear_condo,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss','Deduc'])
        
        lastyear_commercial_units = lastyear_cr_df_policy.Policy.count() + lastyear_lr_df.Units.sum()
        lastyear_residential_units = lastyear_residential_df.Units.sum()
        lastyear_mobile_units = lastyear_mobile_df.Units.sum()
        lastyear_rental_units = lastyear_rental_df.Units.sum()
        lastyear_condo_units = lastyear_condo_df.Units.sum()
        lastyear_total_units = lastyear_commercial_units + lastyear_residential_units + lastyear_mobile_units + lastyear_rental_units + lastyear_condo_units
        
        lastyear_lr_df_exps = (lastyear_lr_df['LMs']+lastyear_lr_df['LMapp']+lastyear_lr_df['LMc']+lastyear_lr_df['LMale'])*lastyear_lr_df['Units']
        lastyear_commercial_exps = lastyear_cr_df_risk.LMs.sum() + lastyear_cr_df_risk.LMapp.sum() + lastyear_cr_df_risk.LMc.sum() + lastyear_cr_df_risk.LMale.sum() + lastyear_lr_df_exps.sum()
        lastyear_residential_df_exps = (lastyear_residential_df['LMs']+lastyear_residential_df['LMapp']+lastyear_residential_df['LMc']+lastyear_residential_df['LMale'])*lastyear_residential_df['Units']
        lastyear_residential_exps = lastyear_residential_df_exps.sum()
        lastyear_mobile_df_exps = (lastyear_mobile_df['LMs']+lastyear_mobile_df['LMapp']+lastyear_mobile_df['LMc']+lastyear_mobile_df['LMale'])*lastyear_mobile_df['Units']
        lastyear_mobile_exps = lastyear_mobile_df_exps.sum()
        lastyear_rental_df_exps = (lastyear_rental_df['LMs']+lastyear_rental_df['LMapp']+lastyear_rental_df['LMc']+lastyear_rental_df['LMale'])*lastyear_rental_df['Units']
        lastyear_rental_exps = lastyear_rental_df_exps.sum()
        lastyear_condo_df_exps = (lastyear_condo_df['LMs']+lastyear_condo_df['LMapp']+lastyear_condo_df['LMc']+lastyear_condo_df['LMale'])*lastyear_condo_df['Units']
        lastyear_condo_exps = lastyear_condo_df_exps.sum()
        lastyear_total_exps = lastyear_commercial_exps + lastyear_residential_exps + lastyear_mobile_exps + lastyear_rental_exps + lastyear_condo_exps

        lastyear_commercial_aal = lastyear_cr_df_risk.RiskTotalLoss.sum() / lastsim + lastyear_lr_df.TotalLoss.sum()
        lastyear_residential_aal = lastyear_residential_df.TotalLoss.sum()
        lastyear_mobile_aal = lastyear_mobile_df.TotalLoss.sum()
        lastyear_rental_aal = lastyear_rental_df.TotalLoss.sum()
        lastyear_condo_aal = lastyear_condo_df.TotalLoss.sum()
        lastyear_total_aal = lastyear_commercial_aal + lastyear_residential_aal + lastyear_mobile_aal + lastyear_rental_aal + lastyear_condo_aal

        lastyear_commercial_deduc = lastyear_cr_df_risk.Deduc.sum()  + lastyear_lr_df.Deduc.sum()
        lastyear_residential_deduc = lastyear_residential_df.Deduc.sum()
        lastyear_mobile_deduc = lastyear_mobile_df.Deduc.sum()
        lastyear_rental_deduc = lastyear_rental_df.Deduc.sum()
        lastyear_condo_deduc = lastyear_condo_df.Deduc.sum()
        lastyear_total_deduc = lastyear_commercial_deduc + lastyear_residential_deduc + lastyear_mobile_deduc + lastyear_rental_deduc + lastyear_condo_deduc


        lastyear_comparison_d = {lastyear: [1,2,3,4,5,6],
                                 'TOB' : ['Commercial','Residential','Mobile Homes','Tenants','Condos','TOTAL'],
                                 'Total Unit Count' : [lastyear_commercial_units,lastyear_residential_units,lastyear_mobile_units,lastyear_rental_units,lastyear_condo_units,lastyear_total_units],
                                 'Unit Inc (%)' : [0,0,0,0,0,0],
                                 'Exp' : [lastyear_commercial_exps,lastyear_residential_exps,lastyear_mobile_exps,lastyear_rental_exps,lastyear_condo_exps,lastyear_total_exps],
                                 'Exp Inc (%)' : [0,0,0,0,0,0],
                                 'AAL' : [lastyear_commercial_aal,lastyear_residential_aal,lastyear_mobile_aal,lastyear_rental_aal,lastyear_condo_aal,lastyear_total_aal],
                                 'AAL Inc (%)' : [0,0,0,0,0,0],
                                 'Deduc' : [lastyear_commercial_deduc,lastyear_residential_deduc,lastyear_mobile_deduc,lastyear_rental_deduc,lastyear_condo_deduc,lastyear_total_deduc],
                                 'Deduc Inc (%)' : [0,0,0,0,0,0]}
        lastyear_comparison_df = pd.DataFrame(data=lastyear_comparison_d)
        lastyear_comparison_df['Loss Costs/$1,000'] = lastyear_comparison_df['AAL']/lastyear_comparison_df['Exp']*1000
        lastyear_comparison_df['Loss Costs Inc(%)'] = [0,0,0,0,0,0]
        #lastyear_comparison_df.style.format({'Unit Inc (%)':'{:.2%}','Exp Inc (%)':'{:.2%}','AAL Inc (%)':'{:.2%}'})

        #thisyear 
        thisyear_cr_policy = thisyear_path + '/cr/CRILM_MidHighRise_AggPolicyLosses.txt'
        thisyear_cr_risk = thisyear_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
        thisyear_lr = thisyear_path + '/pr_lr/valid_data.csv'
        thisyear_residential = thisyear_path + '/pr_residential/valid_data.csv'
        thisyear_mobile = thisyear_path + '/pr_mobile/valid_data.csv'
        thisyear_rental = thisyear_path + '/pr_rental/valid_data.csv'
        thisyear_condo = thisyear_path + '/pr_condo/valid_data.csv'

        thisyear_cr_df_policy = pd.read_csv(thisyear_cr_policy)
        thisyear_cr_df_risk = pd.read_csv(thisyear_cr_risk,usecols=['LMs', 'LMapp', 'LMc', 'LMale', 'RiskTotalLoss','Deduc'])
        thisyear_lr_df = pd.read_csv(thisyear_lr,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss','Deduc'])
        thisyear_residential_df = pd.read_csv(thisyear_residential,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss','Deduc'])
        thisyear_mobile_df = pd.read_csv(thisyear_mobile,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss','Deduc'])
        thisyear_rental_df = pd.read_csv(thisyear_rental,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss','Deduc'])
        thisyear_condo_df = pd.read_csv(thisyear_condo,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss','Deduc'])
        
        thisyear_commercial_units = thisyear_cr_df_policy.Policy.count() + thisyear_lr_df.Units.sum()
        thisyear_residential_units = thisyear_residential_df.Units.sum()
        thisyear_mobile_units = thisyear_mobile_df.Units.sum()
        thisyear_rental_units = thisyear_rental_df.Units.sum()
        thisyear_condo_units = thisyear_condo_df.Units.sum()
        thisyear_total_units = thisyear_commercial_units + thisyear_residential_units + thisyear_mobile_units + thisyear_rental_units + thisyear_condo_units
        thisyear_commercial_units_ratio = (thisyear_commercial_units - lastyear_commercial_units) * 100.00 / lastyear_commercial_units
        thisyear_residential_units_ratio = (thisyear_residential_units - lastyear_residential_units) * 100.00 / lastyear_residential_units
        thisyear_mobile_units_ratio = (thisyear_mobile_units - lastyear_mobile_units) * 100.00 / lastyear_mobile_units
        thisyear_rental_units_ratio = (thisyear_rental_units - lastyear_rental_units) * 100.00 / lastyear_rental_units
        thisyear_condo_units_ratio = (thisyear_condo_units - lastyear_condo_units) * 100.00 / lastyear_condo_units
        thisyear_total_units_ratio = (thisyear_total_units - lastyear_total_units) * 100.00 / lastyear_total_units
        
        thisyear_lr_df_exps = (thisyear_lr_df['LMs']+thisyear_lr_df['LMapp']+thisyear_lr_df['LMc']+thisyear_lr_df['LMale'])*thisyear_lr_df['Units']
        thisyear_commercial_exps = thisyear_cr_df_risk.LMs.sum() + thisyear_cr_df_risk.LMapp.sum() + thisyear_cr_df_risk.LMc.sum() + thisyear_cr_df_risk.LMale.sum() + thisyear_lr_df_exps.sum()
        thisyear_residential_df_exps = (thisyear_residential_df['LMs']+thisyear_residential_df['LMapp']+thisyear_residential_df['LMc']+thisyear_residential_df['LMale'])*thisyear_residential_df['Units']
        thisyear_residential_exps = thisyear_residential_df_exps.sum()
        thisyear_mobile_df_exps = (thisyear_mobile_df['LMs']+thisyear_mobile_df['LMapp']+thisyear_mobile_df['LMc']+thisyear_mobile_df['LMale'])*thisyear_mobile_df['Units']
        thisyear_mobile_exps = thisyear_mobile_df_exps.sum()
        thisyear_rental_df_exps = (thisyear_rental_df['LMs']+thisyear_rental_df['LMapp']+thisyear_rental_df['LMc']+thisyear_rental_df['LMale'])*thisyear_rental_df['Units']
        thisyear_rental_exps = thisyear_rental_df_exps.sum()
        thisyear_condo_df_exps = (thisyear_condo_df['LMs']+thisyear_condo_df['LMapp']+thisyear_condo_df['LMc']+thisyear_condo_df['LMale'])*thisyear_condo_df['Units']
        thisyear_condo_exps = thisyear_condo_df_exps.sum()
        thisyear_total_exps = thisyear_commercial_exps + thisyear_residential_exps + thisyear_mobile_exps + thisyear_rental_exps + thisyear_condo_exps
        thisyear_commercial_exps_ratio = (thisyear_commercial_exps - lastyear_commercial_exps) * 100.00  / lastyear_commercial_exps
        thisyear_residential_exps_ratio = (thisyear_residential_exps - lastyear_residential_exps) * 100.00  / lastyear_residential_exps
        thisyear_mobile_exps_ratio = (thisyear_mobile_exps - lastyear_mobile_exps) * 100.00  / lastyear_mobile_exps
        thisyear_rental_exps_ratio = (thisyear_rental_exps - lastyear_rental_exps) * 100.00  / lastyear_rental_exps
        thisyear_condo_exps_ratio = (thisyear_condo_exps - lastyear_condo_exps) * 100.00  / lastyear_condo_exps
        thisyear_total_exps_ratio = (thisyear_total_exps - lastyear_total_exps) * 100.00  / lastyear_total_exps
 
        thisyear_commercial_aal = thisyear_cr_df_risk.RiskTotalLoss.sum() / thissim + thisyear_lr_df.TotalLoss.sum()
        thisyear_residential_aal = thisyear_residential_df.TotalLoss.sum()
        thisyear_mobile_aal = thisyear_mobile_df.TotalLoss.sum()
        thisyear_rental_aal = thisyear_rental_df.TotalLoss.sum()
        thisyear_condo_aal = thisyear_condo_df.TotalLoss.sum()
        thisyear_total_aal = thisyear_commercial_aal + thisyear_residential_aal + thisyear_mobile_aal + thisyear_rental_aal + thisyear_condo_aal
        thisyear_commercial_aal_ratio = (thisyear_commercial_aal - lastyear_commercial_aal) * 100.00  / lastyear_commercial_aal
        thisyear_residential_aal_ratio = (thisyear_residential_aal - lastyear_residential_aal) * 100.00  / lastyear_residential_aal
        thisyear_mobile_aal_ratio = (thisyear_mobile_aal - lastyear_mobile_aal) * 100.00  / lastyear_mobile_aal
        thisyear_rental_aal_ratio = (thisyear_rental_aal - lastyear_rental_aal) * 100.00  / lastyear_rental_aal
        thisyear_condo_aal_ratio = (thisyear_condo_aal - lastyear_condo_aal) * 100.00  / lastyear_condo_aal
        thisyear_total_aal_ratio = (thisyear_total_aal - lastyear_total_aal) * 100.00  / lastyear_total_aal


        thisyear_commercial_deduc = thisyear_cr_df_risk.Deduc.sum() + thisyear_lr_df.Deduc.sum()
        thisyear_residential_deduc = thisyear_residential_df.Deduc.sum()
        thisyear_mobile_deduc = thisyear_mobile_df.Deduc.sum()
        thisyear_rental_deduc = thisyear_rental_df.Deduc.sum()
        thisyear_condo_deduc = thisyear_condo_df.Deduc.sum()
        thisyear_total_deduc = thisyear_commercial_deduc + thisyear_residential_deduc + thisyear_mobile_deduc + thisyear_rental_deduc + thisyear_condo_deduc
        thisyear_commercial_deduc_ratio = (thisyear_commercial_deduc - lastyear_commercial_deduc) * 100.00  / lastyear_commercial_deduc
        thisyear_residential_deduc_ratio = (thisyear_residential_deduc - lastyear_residential_deduc) * 100.00  / lastyear_residential_deduc
        thisyear_mobile_deduc_ratio = (thisyear_mobile_deduc - lastyear_mobile_deduc) * 100.00  / lastyear_mobile_deduc
        thisyear_rental_deduc_ratio = (thisyear_rental_deduc - lastyear_rental_deduc) * 100.00  / lastyear_rental_deduc
        thisyear_condo_deduc_ratio = (thisyear_condo_deduc - lastyear_condo_deduc) * 100.00  / lastyear_condo_deduc
        thisyear_total_deduc_ratio = (thisyear_total_deduc - lastyear_total_deduc) * 100.00  / lastyear_total_deduc

        thisyear_comparison_d = {thisyear: [1,2,3,4,5,6],
                                 'TOB' : ['Commercial','Residential','Mobile Homes','Tenants','Condos','TOTAL'],
                                 'Total Unit Count' : [thisyear_commercial_units,thisyear_residential_units,thisyear_mobile_units,thisyear_rental_units,thisyear_condo_units,thisyear_total_units],
                                 'Unit Inc (%)' : [thisyear_commercial_units_ratio,thisyear_residential_units_ratio ,thisyear_mobile_units_ratio ,thisyear_rental_units_ratio ,thisyear_condo_units_ratio ,thisyear_total_units_ratio],
                                 'Exp' : [thisyear_commercial_exps,thisyear_residential_exps,thisyear_mobile_exps,thisyear_rental_exps,thisyear_condo_exps,thisyear_total_exps],
                                 'Exp Inc (%)' : [thisyear_commercial_exps_ratio,thisyear_residential_exps_ratio,thisyear_mobile_exps_ratio,thisyear_rental_exps_ratio,thisyear_condo_exps_ratio,thisyear_total_exps_ratio],
                                 'AAL' : [thisyear_commercial_aal,thisyear_residential_aal,thisyear_mobile_aal,thisyear_rental_aal,thisyear_condo_aal,thisyear_total_aal],
                                 'AAL Inc (%)' : [thisyear_commercial_aal_ratio,thisyear_residential_aal_ratio,thisyear_mobile_aal_ratio,thisyear_rental_aal_ratio,thisyear_condo_aal_ratio,thisyear_total_aal_ratio],
                                 'Deduc' : [thisyear_commercial_deduc,thisyear_residential_deduc,thisyear_mobile_deduc,thisyear_rental_deduc,thisyear_condo_deduc,thisyear_total_deduc],
                                 'Deduc Inc (%)' : [thisyear_commercial_deduc_ratio,thisyear_residential_deduc_ratio,thisyear_mobile_deduc_ratio,thisyear_rental_deduc_ratio,thisyear_condo_deduc_ratio,thisyear_total_aal_ratio]}        
        thisyear_comparison_df = pd.DataFrame(data=thisyear_comparison_d)
        thisyear_comparison_df['Loss Costs/$1,000'] = thisyear_comparison_df['AAL']/thisyear_comparison_df['Exp']*1000
        thisyear_comparison_df['Loss Costs Inc(%)'] = (thisyear_comparison_df['Loss Costs/$1,000'] - lastyear_comparison_df['Loss Costs/$1,000']) / lastyear_comparison_df['Loss Costs/$1,000'] * 100.00

        return [lastyear_comparison_df,thisyear_comparison_df]   
        #thisyear_comparison_df.style.format({'Unit Inc (%)':'{:.2%}','Exp Inc (%)':'{:.2%}','AAL Inc (%)':'{:.2%}'})    


    @staticmethod
    def retemarking(thisyear, thissim):

        sheetlist = [1,2,3]

        # define path
        thisyear_path = 'app/data/' + thisyear

        #total
        thisyear_cr_risk = thisyear_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
        thisyear_lr = thisyear_path + '/pr_lr/valid_data.csv'
        thisyear_residential = thisyear_path + '/pr_residential/valid_data.csv'
        thisyear_mobile = thisyear_path + '/pr_mobile/valid_data.csv'
        thisyear_rental = thisyear_path + '/pr_rental/valid_data.csv'
        thisyear_condo = thisyear_path + '/pr_condo/valid_data.csv'

        thisyear_cr_df_risk = pd.read_csv(thisyear_cr_risk,usecols=['LMs', 'LMapp', 'LMc', 'LMale', 'RiskTotalLoss'])        
        thisyear_lr_df = pd.read_csv(thisyear_lr,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        thisyear_residential_df = pd.read_csv(thisyear_residential,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        thisyear_mobile_df = pd.read_csv(thisyear_mobile,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        thisyear_rental_df = pd.read_csv(thisyear_rental,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        thisyear_condo_df = pd.read_csv(thisyear_condo,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])

        thisyear_commercial_aal = thisyear_cr_df_risk.RiskTotalLoss.sum() / thissim + thisyear_lr_df.TotalLoss.sum()
        thisyear_residential_aal = thisyear_residential_df.TotalLoss.sum()
        thisyear_mobile_aal = thisyear_mobile_df.TotalLoss.sum()
        thisyear_rental_aal = thisyear_rental_df.TotalLoss.sum()
        thisyear_condo_aal = thisyear_condo_df.TotalLoss.sum()
        thisyear_total_aal = thisyear_commercial_aal + thisyear_residential_aal + thisyear_mobile_aal + thisyear_rental_aal + thisyear_condo_aal

        thisyear_total_d = {'TOB Code': [1,2,3,4,6,7,],
                                 'TOB Name' : ['Commercial','Residential','Mobile Homes','Tenants','Condos','TOTAL'],
                                 'AAL' : [thisyear_commercial_aal,thisyear_residential_aal,thisyear_mobile_aal,thisyear_rental_aal,thisyear_condo_aal,thisyear_total_aal]}
        thisyear_total_df = pd.DataFrame(data=thisyear_total_d)
        sheetlist[0] = thisyear_total_df

        #deductible
        thisyear_cr_de = thisyear_path + '/cr/CRILM_MidHighRise_StormLosses.txt'
        thisyear_lr_de = thisyear_path + '/pr_lr/Storm_Losses.csv'
        thisyear_residential_de = thisyear_path + '/pr_residential/Storm_Losses.csv'
        thisyear_mobile_de = thisyear_path + '/pr_mobile/Storm_Losses.csv'
        thisyear_rental_de = thisyear_path + '/pr_rental/Storm_Losses.csv'
        thisyear_condo_de = thisyear_path + '/pr_condo/Storm_Losses.csv'

        thisyear_cr_df_de = pd.read_csv(thisyear_cr_de, header = None, names = ['A','Year','CRL'])        
        thisyear_lr_df_de = pd.read_csv(thisyear_lr_de, header = None, names = ['A','Year','LRL'])        
        thisyear_commercial_df_de = pd.read_csv(thisyear_lr_de, header = None, names = ['A','Year','LRL'])
        thisyear_residential_df_de = pd.read_csv(thisyear_residential_de, header = None, names = ['A','Year','Residential Loss'])
        thisyear_mobile_df_de = pd.read_csv(thisyear_mobile_de, header = None, names = ['A','Year','Mobile Home Loss'])
        thisyear_rental_df_de = pd.read_csv(thisyear_rental_de, header = None, names = ['A','Year','Tenants Loss'])
        thisyear_condo_df_de = pd.read_csv(thisyear_condo_de, header = None, names = ['A','Year','Condo Units Loss'])

        thisyear_cr_df_de_1 = thisyear_cr_df_de.sort_values(by='Year').reset_index(drop=True)
        thisyear_lr_df_de['Commercial Loss'] = thisyear_cr_df_de_1.CRL + thisyear_lr_df_de.LRL
        result_de = pd.concat([thisyear_lr_df_de[['Year','Commercial Loss']], thisyear_residential_df_de[['Residential Loss']]], axis=1)
        result_de = pd.concat([result_de, thisyear_mobile_df_de[['Mobile Home Loss']]], axis=1)
        result_de = pd.concat([result_de, thisyear_rental_df_de[['Tenants Loss']]], axis=1)
        result_de = pd.concat([result_de, thisyear_condo_df_de[['Condo Units Loss']]], axis=1)
        result_de['Total Loss'] = result_de['Commercial Loss'] + result_de['Residential Loss'] + result_de['Mobile Home Loss'] + result_de['Tenants Loss'] + result_de['Condo Units Loss']
        sheetlist[1] = result_de
        #deductible total
        deductible_total_d = {'Year':['Total'],'Total Loss':[result_de['Total Loss'].sum()],'Commercial Loss':[result_de['Commercial Loss'].sum()]
        ,'Residential Loss':[result_de['Residential Loss'].sum()],'Mobile Home Loss':[result_de['Mobile Home Loss'].sum()]
        ,'Tenants Loss':[result_de['Tenants Loss'].sum()],'Condo Units Loss':[result_de['Condo Units Loss'].sum()]}
        deductible_total_df = pd.DataFrame(data=deductible_total_d)
        sheetlist[2] = deductible_total_df

        return sheetlist
    
    @expose('/showComparisons/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def showComparisons(self, lastyear, thisyear, lastsim, thissim):

        # number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)
        loss_costs_format = lambda x: '{:,.3f}'.format(x)

        tables = MyView.comparisons(lastyear, thisyear, lastsim, thissim)
        lastyear_comparison_df = tables[0]
        thisyear_comparison_df = tables[1]

        return self.render_template('export.html',lyear=lastyear,tyear=thisyear,lsim=lastsim,tsim=thissim,analytype='exportComparisons',title='CatFund Comparisons',ratemarking='exportRateMarking',
                               tables=[lastyear_comparison_df.to_html(classes='table table-bordered',index=False,formatters={'Total Unit Count':int_num_format,'Exp':flt_num_format,'AAL':flt_num_format,'Loss Costs/$1,000':loss_costs_format,'Loss Costs Inc(%)':flt_percent_format,'Deduc':flt_num_format,'Deduc Inc (%)':flt_percent_format},columns=[lastyear,'TOB','Total Unit Count','Unit Inc (%)','Exp','Exp Inc (%)','AAL','AAL Inc (%)','Deduc','Deduc Inc (%)','Loss Costs/$1,000','Loss Costs Inc(%)']),
                                       thisyear_comparison_df.to_html(classes='table table-bordered',index=False,formatters={'Total Unit Count':int_num_format,'Unit Inc (%)':flt_percent_format,'Exp':flt_num_format,'Exp Inc (%)':flt_percent_format,'AAL':flt_num_format,'AAL Inc (%)':flt_percent_format,'Loss Costs/$1,000':loss_costs_format,'Loss Costs Inc(%)':flt_percent_format,'Deduc':flt_num_format,'Deduc Inc (%)':flt_percent_format},columns=[thisyear,'TOB','Total Unit Count','Unit Inc (%)','Exp','Exp Inc (%)','AAL','AAL Inc (%)','Deduc','Deduc Inc (%)','Loss Costs/$1,000','Loss Costs Inc(%)'])])

    @expose('/exportComparisons/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def exportComparisons(self, lastyear, thisyear, lastsim, thissim):

        tables = MyView.comparisons(lastyear, thisyear, lastsim, thissim)
        lastyear_comparison_df = tables[0]
        thisyear_comparison_df = tables[1]

        df = pd.concat([lastyear_comparison_df[['TOB','Total Unit Count','Unit Inc (%)','Exp','Exp Inc (%)','AAL','AAL Inc (%)','Deduc','Deduc Inc (%)','Loss Costs/$1,000','Loss Costs Inc(%)']],thisyear_comparison_df[['TOB','Total Unit Count','Unit Inc (%)','Exp','Exp Inc (%)','AAL','AAL Inc (%)','Deduc','Deduc Inc (%)','Loss Costs/$1,000','Loss Costs Inc(%)']]])
        index = 0
        first_col = [lastyear,lastyear,lastyear,lastyear,lastyear,lastyear,thisyear,thisyear,thisyear,thisyear,thisyear,thisyear]
        df.insert(loc=index,column='year',value=first_col)

        resp = make_response(df.to_csv(index=False,float_format="%.2f"))
        resp.headers["Content-Disposition"] = "attachment; filename=Comparison.csv"
        resp.headers["Content-Type"] = "text/csv"

        return resp

    @expose('/exportRateMarking/<string:thisyear>/<int:thissim>')
    @has_access
    def exportRateMarking(self, thisyear, thissim):

        tables = MyView.retemarking(thisyear,thissim)
        total_df = tables[0][['TOB Code','TOB Name','AAL']]
        deductible_df = tables[1][['Year','Total Loss','Commercial Loss','Residential Loss','Mobile Home Loss','Tenants Loss','Condo Units Loss']]
        deductible_df.index.name = 'Event ID'
        deductible_df.index = np.arange(1,len(deductible_df)+1)
        deductible_total_df = tables[2][['Year','Total Loss','Commercial Loss','Residential Loss','Mobile Home Loss','Tenants Loss','Condo Units Loss']]

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        total_df.to_excel(writer, sheet_name='Control Totals',index=False,float_format="%.2f")
        deductible_df.to_excel(writer, sheet_name='Actual deductible - With Demand',index=True,float_format="%.2f",columns=["Year","Total Loss","Commercial Loss","Residential Loss","Mobile Home Loss","Tenants Loss","Condo Units Loss"])
        deductible_total_df.to_excel(writer, sheet_name='Actual deductible - With Demand',index=False,float_format="%.2f",columns=["Year","Total Loss","Commercial Loss","Residential Loss","Mobile Home Loss","Tenants Loss","Condo Units Loss"],
             startrow=len(deductible_df)+1, startcol=1, header=False)
        worksheet1 = writer.sheets['Control Totals']
        worksheet2 = writer.sheets['Actual deductible - With Demand']
        
        workbook = writer.book
        money_fmt = workbook.add_format({'num_format': '$#,##0.00'})
        xlsformat = workbook.add_format()

        worksheet1.set_column('C:C', 12, money_fmt)
        worksheet2.set_column('C:H', 12, money_fmt)
        #the writer has done its job
        writer.close()

        #go back to the beginning of the stream
        output.seek(0)
        #df = pd.concat([lastyear_comparison_df[['TOB','Total Unit Count','Unit Inc (%)','Exp','Exp Inc (%)','AAL','AAL Inc (%)']],thisyear_comparison_df[['TOB','Total Unit Count','Unit Inc (%)','Exp','Exp Inc (%)','AAL','AAL Inc (%)']]])
        #index = 0
        #first_col = [lastyear,lastyear,lastyear,lastyear,lastyear,lastyear,thisyear,thisyear,thisyear,thisyear,thisyear,thisyear]
        #df.insert(loc=index,column='year',value=first_col)

        #resp = make_response(writer)
        #resp.headers["Content-Disposition"] = "attachment; filename=ratemarking.xlsx"
        #resp.headers["Content-Type"] = "text/csv"

        return send_file(output, attachment_filename="retemarking.xlsx", as_attachment=True)
    

    @staticmethod
    def yearbuild(yeartup,tob):

        yearlist = [1,2,3]

        i = 0

        for year in yeartup:
            # define path the different year
            year_path = 'app/data/' + year

            year_lr = year_path + '/'+tob+'/valid_data.csv'
            year_lr_df = pd.read_csv(year_lr,usecols=['YearBuilt','Units', 'LMs', 'LMapp', 'LMc', 'LMale','TotalLoss'])
            year_lr_df_lt_1970 = year_lr_df[year_lr_df['YearBuilt'] < 1970]
            year_lr_df_lte_1983 = year_lr_df[(year_lr_df['YearBuilt'] >= 1970) & (year_lr_df['YearBuilt'] <= 1983)]
            year_lr_df_lte_1993 = year_lr_df[(year_lr_df['YearBuilt'] >= 1984) & (year_lr_df['YearBuilt'] <= 1993)]
            year_lr_df_gte_1994 = year_lr_df[year_lr_df['YearBuilt'] >= 1994]

            lr_exps_lt_1970 = ((year_lr_df_lt_1970.LMs + year_lr_df_lt_1970.LMapp + year_lr_df_lt_1970.LMc + year_lr_df_lt_1970.LMale) * year_lr_df_lt_1970.Units).sum()
            lr_exps_lte_1983 = ((year_lr_df_lte_1983.LMs + year_lr_df_lte_1983.LMapp + year_lr_df_lte_1983.LMc + year_lr_df_lte_1983.LMale) * year_lr_df_lte_1983.Units).sum()
            lr_exps_lte_1993 = ((year_lr_df_lte_1993.LMs + year_lr_df_lte_1993.LMapp + year_lr_df_lte_1993.LMc + year_lr_df_lte_1993.LMale) * year_lr_df_lte_1993.Units).sum()
            lr_exps_gte_1994 = ((year_lr_df_gte_1994.LMs + year_lr_df_gte_1994.LMapp + year_lr_df_gte_1994.LMc + year_lr_df_gte_1994.LMale) * year_lr_df_gte_1994.Units).sum()
            lr_exps_total = lr_exps_lt_1970 + (0 if np.isnan(lr_exps_lte_1983) else lr_exps_lte_1983) + lr_exps_lte_1993 + lr_exps_gte_1994

            lr_aal_lt_1970 = year_lr_df_lt_1970.TotalLoss.sum()
            lr_aal_lte_1983 = year_lr_df_lte_1983.TotalLoss.sum()
            lr_aal_lte_1993 = year_lr_df_lte_1993.TotalLoss.sum()
            lr_aal_gte_1994 = year_lr_df_gte_1994.TotalLoss.sum()
            lr_aal_total = year_lr_df.TotalLoss.sum()

            if tob == 'pr_lr': 
                year_cr_risk = year_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
                year_cr_df_risk = pd.read_csv(year_cr_risk,usecols=['YearBuilt','LMs', 'LMapp', 'LMc', 'LMale'])
                year_cr_df_risk_lt_1970 = year_cr_df_risk[year_cr_df_risk['YearBuilt'] < 1970]
                year_cr_df_risk_lte_1983 = year_cr_df_risk[(year_cr_df_risk['YearBuilt'] >= 1970) & (year_cr_df_risk['YearBuilt'] <= 1983)]
                year_cr_df_risk_lte_1993 = year_cr_df_risk[(year_cr_df_risk['YearBuilt'] >= 1984) & (year_cr_df_risk['YearBuilt'] <= 1993)]
                year_cr_df_risk_gte_1994 = year_cr_df_risk[year_cr_df_risk['YearBuilt'] >= 1994]

                cr_exps_lt_1970 = year_cr_df_risk_lt_1970.LMs.sum() + year_cr_df_risk_lt_1970.LMapp.sum() + year_cr_df_risk_lt_1970.LMc.sum() + year_cr_df_risk_lt_1970.LMale.sum()
                cr_exps_lte_1983 = year_cr_df_risk_lte_1983.LMs.sum() + year_cr_df_risk_lte_1983.LMapp.sum() + year_cr_df_risk_lte_1983.LMc.sum() + year_cr_df_risk_lte_1983.LMale.sum()
                cr_exps_lte_1993 = year_cr_df_risk_lte_1993.LMs.sum() + year_cr_df_risk_lte_1993.LMapp.sum() + year_cr_df_risk_lte_1993.LMc.sum() + year_cr_df_risk_lte_1993.LMale.sum()
                cr_exps_gte_1994 = year_cr_df_risk_gte_1994.LMs.sum() + year_cr_df_risk_gte_1994.LMapp.sum() + year_cr_df_risk_gte_1994.LMc.sum() + year_cr_df_risk_gte_1994.LMale.sum()
                cr_exps_total = cr_exps_lt_1970 + cr_exps_lte_1983 + cr_exps_lte_1993 + cr_exps_gte_1994
                
                change_exps_lt_1970 = (cr_exps_lt_1970 + lr_exps_lt_1970) / (cr_exps_total + lr_exps_total) * 100
                change_exps_lte_1983 = (cr_exps_lte_1983 + lr_exps_lte_1983) / (cr_exps_total + lr_exps_total) * 100
                change_exps_lte_1993 = (cr_exps_lte_1993 + lr_exps_lte_1993) / (cr_exps_total + lr_exps_total) * 100
                change_exps_gte_1994 = (cr_exps_gte_1994 + lr_exps_gte_1994) / (cr_exps_total + lr_exps_total) * 100

                year_exps_d = { year: [1,2,3,4,5],
                                'Year Build':['<1970','1970~1983','1984~1993','>=1994','Total'],
                                'CR Exposure':[cr_exps_lt_1970,cr_exps_lte_1983,cr_exps_lte_1993,cr_exps_gte_1994,cr_exps_total],
                                'LR Exposure':[lr_exps_lt_1970,lr_exps_lte_1983,lr_exps_lte_1993,lr_exps_gte_1994,lr_exps_total],
                                'Total Change':[change_exps_lt_1970,change_exps_lte_1983,change_exps_lte_1993,change_exps_gte_1994,100]}

            
            else:
                
                change_exps_lt_1970 = (lr_exps_lt_1970) / (lr_exps_total) * 100
                change_exps_lte_1983 = (lr_exps_lte_1983) / (lr_exps_total) * 100
                change_exps_lte_1993 = (lr_exps_lte_1993) / (lr_exps_total) * 100
                change_exps_gte_1994 = (lr_exps_gte_1994) / (lr_exps_total) * 100

                year_exps_d = { year: [1,2,3,4,5],
                                'Year Build':['<1970','1970~1983','1984~1993','>=1994','Total'],
                                'Exposure':[lr_exps_lt_1970,lr_exps_lte_1983,lr_exps_lte_1993,lr_exps_gte_1994,lr_exps_total],
                                'Total Change':[change_exps_lt_1970,change_exps_lte_1983,change_exps_lte_1993,change_exps_gte_1994,100],
                                'AAL':[lr_aal_lt_1970,lr_aal_lte_1983,lr_aal_lte_1993,lr_aal_gte_1994,lr_aal_total]}
 
            year_exps_df = pd.DataFrame(data=year_exps_d,index=[0,1,2,3,4])
            if tob != 'pr_lr': 
                year_exps_df['Loss Costs/$1,000'] = year_exps_df['AAL']/year_exps_df['Exposure']*1000
           
            yearlist[i] = year_exps_df.fillna(0)
            i = i + 1

        percent_cr_exps_lt_1970 = (yearlist[1].iat[0,1] - yearlist[0].iat[0,1]) / yearlist[0].iat[0,1] * 100
        percent_cr_exps_lte_1983 = (yearlist[1].iat[1,1] - yearlist[0].iat[1,1]) / yearlist[0].iat[1,1] * 100
        percent_cr_exps_lte_1993 = (yearlist[1].iat[2,1] - yearlist[0].iat[2,1]) / yearlist[0].iat[2,1] * 100
        percent_cr_exps_gte_1994 = (yearlist[1].iat[3,1] - yearlist[0].iat[3,1]) / yearlist[0].iat[3,1] * 100
        percent_cr_exps_total = (yearlist[1].iat[4,1] - yearlist[0].iat[4,1]) / yearlist[0].iat[4,1] * 100

        if tob == 'pr_lr':

            percent_lr_exps_lt_1970 = (yearlist[1].iat[0,2] - yearlist[0].iat[0,2]) / yearlist[0].iat[0,2] * 100
            percent_lr_exps_lte_1983 = (yearlist[1].iat[1,2] - yearlist[0].iat[1,2]) / yearlist[0].iat[1,2] * 100
            percent_lr_exps_lte_1993 = (yearlist[1].iat[2,2] - yearlist[0].iat[2,2]) / yearlist[0].iat[2,2] * 100
            percent_lr_exps_gte_1994 = (yearlist[1].iat[3,2] - yearlist[0].iat[3,2]) / yearlist[0].iat[3,2] * 100
            percent_lr_exps_total = (yearlist[1].iat[4,2] - yearlist[0].iat[4,2]) / yearlist[0].iat[4,2] * 100

            percent_change_d = {'CR Percentage Change':[percent_cr_exps_lt_1970,percent_cr_exps_lte_1983,percent_cr_exps_lte_1993,percent_cr_exps_gte_1994,percent_cr_exps_total],
                            'LR Percentage Change':[percent_lr_exps_lt_1970,percent_lr_exps_lte_1983,percent_lr_exps_lte_1993,percent_lr_exps_gte_1994,percent_lr_exps_total]} 
        else:
            percent_cr_exps_lt_1970 = (yearlist[1].iat[0,2] - yearlist[0].iat[0,2]) / yearlist[0].iat[0,2] * 100
            percent_cr_exps_lte_1983 = (yearlist[1].iat[1,2] - yearlist[0].iat[1,2]) / yearlist[0].iat[1,2] * 100
            percent_cr_exps_lte_1993 = (yearlist[1].iat[2,2] - yearlist[0].iat[2,2]) / yearlist[0].iat[2,2] * 100
            percent_cr_exps_gte_1994 = (yearlist[1].iat[3,2] - yearlist[0].iat[3,2]) / yearlist[0].iat[3,2] * 100
            percent_cr_exps_total = (yearlist[1].iat[4,2] - yearlist[0].iat[4,2]) / yearlist[0].iat[4,2] * 100
            percent_change_d = {'Percentage Change':[percent_cr_exps_lt_1970,percent_cr_exps_lte_1983,percent_cr_exps_lte_1993,percent_cr_exps_gte_1994,percent_cr_exps_total]} 

        yearlist[2] = pd.DataFrame(data=percent_change_d,index=[0,1,2,3,4]) 
        if tob != 'pr_lr': 
            yearlist[2]['AAL Inc(%)'] = (yearlist[1]['AAL']-yearlist[0]['AAL'])/yearlist[0]['AAL']*100
            yearlist[2]['Loss Costs Inc(%)'] = (yearlist[1]['Loss Costs/$1,000']-yearlist[0]['Loss Costs/$1,000'])/yearlist[0]['Loss Costs/$1,000']*100           
        yearlist[2] = yearlist[2].fillna(0)
        return yearlist

    @expose('/showYearbuild/<string:lastyear>/<string:thisyear>')
    @has_access
    def showYearbuild(self, lastyear, thisyear):

        tobSelectValue = request.args.get('type_of_building') if request.args.get('type_of_building') else 'pr_lr' 
        tobform = TOBForm(type_of_building=tobSelectValue)

        # number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)
        loss_costs_format = lambda x: '{:,.3f}'.format(x)

        yeartup = (lastyear, thisyear)
        yearlist = MyView.yearbuild(yeartup,tobSelectValue)

        lastyear_exps_df = yearlist[0]
        thisyear_exps_df = yearlist[1]
        percent_exps_df = yearlist[2]
        result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)

        if tobSelectValue == 'pr_lr' :
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='Yearbuild',title='Yearbuilt',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format},columns=[lastyear,'Year Build','CR Exposure','LR Exposure','Total Change']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format,'CR Percentage Change':flt_percent_format,'LR Percentage Change':flt_percent_format},columns=[thisyear,'Year Build','CR Exposure','LR Exposure','Total Change','CR Percentage Change','LR Percentage Change'])])
        else:
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='Yearbuild',title='Yearbuilt',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'Exposure':flt_num_format,'Total Change':flt_percent_format,'AAL':flt_num_format,'Loss Costs/$1,000':loss_costs_format},columns=[lastyear,'Year Build','Exposure','Total Change','AAL','Loss Costs/$1,000']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'Exposure':flt_num_format,'Total Change':flt_percent_format,'Percentage Change':flt_percent_format,'AAL':flt_num_format,'AAL Inc(%)':flt_percent_format,'Loss Costs/$1,000':loss_costs_format,'Loss Costs Inc(%)':flt_percent_format},columns=[thisyear,'Year Build','Exposure','Total Change','Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)'])])

    @expose('/exportYearbuild/<string:tobSelectValue>/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def exportYearbuild(self, tobSelectValue ,lastyear, thisyear, lastsim, thissim):

        yeartup = (lastyear, thisyear)
        yearlist = MyView.yearbuild(yeartup,tobSelectValue)

        lastyear_exps_df = yearlist[0]
        thisyear_exps_df = yearlist[1]
        percent_exps_df = yearlist[2]

        if tobSelectValue == 'pr_lr' :
            result_df = pd.concat([lastyear_exps_df[[lastyear,'Year Build','CR Exposure','LR Exposure','Total Change']],thisyear_exps_df[[thisyear,'Year Build','CR Exposure','LR Exposure','Total Change']], percent_exps_df[['CR Percentage Change','LR Percentage Change']]], axis=1)
           
        else:
            result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)
            result_df = pd.concat([lastyear_exps_df[[lastyear,'Year Build','Exposure','Total Change','AAL','Loss Costs/$1,000']],result_df[[thisyear,'Year Build','Exposure','Total Change','Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)']]], axis=1)

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        #lastyear_exps_df.to_excel(writer, sheet_name=tobSelectValue,index=False,float_format="%.2f")
        result_df.to_excel(writer, sheet_name=tobSelectValue,index=False,float_format="%.2f")
        worksheet1 = writer.sheets[tobSelectValue]
        
        workbook = writer.book
        money_fmt = workbook.add_format({'num_format': '$#,##0.00'})
        percent_format = workbook.add_format({'num_format': '0.00%'})

        if tobSelectValue == 'pr_lr' :
            worksheet1.set_column('C:C', 20, money_fmt)
            worksheet1.set_column('D:D', 20, money_fmt)
            worksheet1.set_column('I:I', 20, money_fmt)
            worksheet1.set_column('H:H', 20, money_fmt)
        else:
            worksheet1.set_column('C:C', 20, money_fmt)
            worksheet1.set_column('E:E', 20, money_fmt)
            worksheet1.set_column('I:I', 20, money_fmt)
            worksheet1.set_column('L:L', 20, money_fmt)
        #the writer has done its job
        writer.close()

        #go back to the beginning of the stream
        output.seek(0)

        return send_file(output, attachment_filename="yearbuild.xlsx", as_attachment=True)

    @staticmethod
    def regionAna(yeartup,tob):

        regionlist = [1,2,3]

        i = 0

        for year in yeartup:
            # define path the different year
            year_path = 'app/data/' + year

            year_lr = year_path + '/'+tob+'/valid_data.csv'
            year_lr_df = pd.read_csv(year_lr,usecols=['Region','Units', 'LMs', 'LMapp', 'LMc', 'LMale','TotalLoss'])

            year_lr_df_Central = year_lr_df[year_lr_df['Region'] == 'Central']
            year_lr_df_Keys = year_lr_df[year_lr_df['Region'] == 'Keys']
            year_lr_df_North = year_lr_df[year_lr_df['Region'] == 'North']
            year_lr_df_South = year_lr_df[year_lr_df['Region'] == 'South']

            lr_exps_Central = ((year_lr_df_Central.LMs + year_lr_df_Central.LMapp + year_lr_df_Central.LMc + year_lr_df_Central.LMale) * year_lr_df_Central.Units).sum()
            lr_exps_Keys = ((year_lr_df_Keys.LMs + year_lr_df_Keys.LMapp + year_lr_df_Keys.LMc + year_lr_df_Keys.LMale) * year_lr_df_Keys.Units).sum()
            lr_exps_North = ((year_lr_df_North.LMs + year_lr_df_North.LMapp + year_lr_df_North.LMc + year_lr_df_North.LMale) * year_lr_df_North.Units).sum()
            lr_exps_South = ((year_lr_df_South.LMs + year_lr_df_South.LMapp + year_lr_df_South.LMc + year_lr_df_South.LMale) * year_lr_df_South.Units).sum()
            lr_exps_total = lr_exps_Central + lr_exps_Keys + lr_exps_North + lr_exps_South

            lr_aal_Central = year_lr_df_Central.TotalLoss.sum()
            lr_aal_Keys = year_lr_df_Keys.TotalLoss.sum()
            lr_aal_North = year_lr_df_North.TotalLoss.sum()
            lr_aal_South = year_lr_df_South.TotalLoss.sum()
            lr_aal_total = year_lr_df.TotalLoss.sum()

            if tob == 'pr_lr':
                year_cr_risk = year_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
                year_cr_df_risk = pd.read_csv(year_cr_risk,usecols=['Region','LMs', 'LMapp', 'LMc', 'LMale'])
                year_cr_df_risk_Central = year_cr_df_risk[year_cr_df_risk['Region'] == 'Central']
                year_cr_df_risk_Keys = year_cr_df_risk[year_cr_df_risk['Region'] == 'Keys']
                year_cr_df_risk_North = year_cr_df_risk[year_cr_df_risk['Region'] == 'North']
                year_cr_df_risk_South = year_cr_df_risk[year_cr_df_risk['Region'] == 'South']

                cr_exps_Central = year_cr_df_risk_Central.LMs.sum() + year_cr_df_risk_Central.LMapp.sum() + year_cr_df_risk_Central.LMc.sum() + year_cr_df_risk_Central.LMale.sum()
                cr_exps_Keys = year_cr_df_risk_Keys.LMs.sum() + year_cr_df_risk_Keys.LMapp.sum() + year_cr_df_risk_Keys.LMc.sum() + year_cr_df_risk_Keys.LMale.sum()
                cr_exps_North = year_cr_df_risk_North.LMs.sum() + year_cr_df_risk_North.LMapp.sum() + year_cr_df_risk_North.LMc.sum() + year_cr_df_risk_North.LMale.sum()
                cr_exps_South = year_cr_df_risk_South.LMs.sum() + year_cr_df_risk_South.LMapp.sum() + year_cr_df_risk_South.LMc.sum() + year_cr_df_risk_South.LMale.sum()
                cr_exps_total = cr_exps_Central + cr_exps_Keys + cr_exps_North + cr_exps_South
            
                change_exps_Central = (cr_exps_Central + lr_exps_Central) / (cr_exps_total + lr_exps_total) * 100
                change_exps_Keys = (cr_exps_Keys + lr_exps_Keys) / (cr_exps_total + lr_exps_total) * 100
                change_exps_North = (cr_exps_North + lr_exps_North) / (cr_exps_total + lr_exps_total) * 100
                change_exps_South = (cr_exps_South + lr_exps_South) / (cr_exps_total + lr_exps_total) * 100

                region_exps_d = {year: [1,2,3,4,5],
                                'Region':['Central','Keys','North','South','Total'],
                                'CR Exposure':[cr_exps_Central,cr_exps_Keys,cr_exps_North,cr_exps_South,cr_exps_total],
                                'LR Exposure':[lr_exps_Central,lr_exps_Keys,lr_exps_North,lr_exps_South,lr_exps_total],
                                'Total Change':[change_exps_Central,change_exps_Keys,change_exps_North,change_exps_South,100]}
            else:
                change_exps_Central = (lr_exps_Central) / (lr_exps_total) * 100
                change_exps_Keys = (lr_exps_Keys) / (lr_exps_total) * 100
                change_exps_North = (lr_exps_North) / (lr_exps_total) * 100
                change_exps_South = (lr_exps_South) / (lr_exps_total) * 100

                region_exps_d = {year: [1,2,3,4,5],
                                'Region':['Central','Keys','North','South','Total'],
                                'Exposure':[lr_exps_Central,lr_exps_Keys,lr_exps_North,lr_exps_South,lr_exps_total],
                                'Total Change':[change_exps_Central,change_exps_Keys,change_exps_North,change_exps_South,100],
                                'AAL':[lr_aal_Central,lr_aal_Keys,lr_aal_North,lr_aal_South,lr_aal_total]}

            region_exps_df = pd.DataFrame(data=region_exps_d,index=[0,1,2,3,4]) 
            if tob != 'pr_lr': 
                region_exps_df['Loss Costs/$1,000'] = region_exps_df['AAL']/region_exps_df['Exposure']*1000

            regionlist[i] = region_exps_df.fillna(0)
            i = i + 1

        percent_cr_exps_Central = (regionlist[1].iat[0,1] - regionlist[0].iat[0,1]) / regionlist[0].iat[0,1] * 100
        percent_cr_exps_Keys = (regionlist[1].iat[1,1] - regionlist[0].iat[1,1]) / regionlist[0].iat[1,1] * 100
        percent_cr_exps_North = (regionlist[1].iat[2,1] - regionlist[0].iat[2,1]) / regionlist[0].iat[2,1] * 100
        percent_cr_exps_South = (regionlist[1].iat[3,1] - regionlist[0].iat[3,1]) / regionlist[0].iat[3,1] * 100
        percent_cr_exps_total = (regionlist[1].iat[4,1] - regionlist[0].iat[4,1]) / regionlist[0].iat[4,1] * 100

        if tob == 'pr_lr':

            percent_lr_exps_Central = (regionlist[1].iat[0,2] - regionlist[0].iat[0,2]) / regionlist[0].iat[0,2] * 100
            percent_lr_exps_Keys = (regionlist[1].iat[1,2] - regionlist[0].iat[1,2]) / regionlist[0].iat[1,2] * 100
            percent_lr_exps_North = (regionlist[1].iat[2,2] - regionlist[0].iat[2,2]) / regionlist[0].iat[2,2] * 100
            percent_lr_exps_South = (regionlist[1].iat[3,2] - regionlist[0].iat[3,2]) / regionlist[0].iat[3,2] * 100
            percent_lr_exps_total = (regionlist[1].iat[4,2] - regionlist[0].iat[4,2]) / regionlist[0].iat[4,2] * 100

            percent_total_exps_Central = (regionlist[1].iat[0,1] + regionlist[1].iat[0,2]  - regionlist[0].iat[0,1] - regionlist[0].iat[0,2]) / (regionlist[0].iat[0,2] + regionlist[0].iat[0,1]) * 100
            percent_total_exps_Keys = (regionlist[1].iat[1,1] + regionlist[1].iat[1,2] - regionlist[0].iat[1,1] - regionlist[0].iat[1,2]) / (regionlist[0].iat[1,2] + regionlist[0].iat[1,1]) * 100
            percent_total_exps_North = (regionlist[1].iat[2,1] + regionlist[1].iat[2,2] - regionlist[0].iat[2,1] - regionlist[0].iat[2,2]) / (regionlist[0].iat[2,2] + regionlist[0].iat[2,1]) * 100
            percent_total_exps_South = (regionlist[1].iat[3,1] + regionlist[1].iat[3,2] - regionlist[0].iat[3,1] - regionlist[0].iat[3,2]) / (regionlist[0].iat[3,2] + regionlist[0].iat[3,1]) * 100
            percent_total_exps_total = (regionlist[1].iat[4,1] + regionlist[1].iat[4,2] - regionlist[0].iat[4,1] - regionlist[0].iat[4,2]) / (regionlist[0].iat[4,2] + regionlist[0].iat[4,1]) * 100

            percent_change_d = {'CR Percentage Change':[percent_cr_exps_Central,percent_cr_exps_Keys,percent_cr_exps_North,percent_cr_exps_South,percent_cr_exps_total],
                                'LR Percentage Change':[percent_lr_exps_Central,percent_lr_exps_Keys,percent_lr_exps_North,percent_lr_exps_South,percent_lr_exps_total],
                                'Total Percentage Change':[percent_total_exps_Central,percent_total_exps_Keys,percent_total_exps_North,percent_total_exps_South,percent_total_exps_total]} 
        else:
            percent_cr_exps_Central = (regionlist[1].iat[0,2] - regionlist[0].iat[0,2]) / regionlist[0].iat[0,2] * 100
            percent_cr_exps_Keys = (regionlist[1].iat[1,2] - regionlist[0].iat[1,2]) / regionlist[0].iat[1,2] * 100
            percent_cr_exps_North = (regionlist[1].iat[2,2] - regionlist[0].iat[2,2]) / regionlist[0].iat[2,2] * 100
            percent_cr_exps_South = (regionlist[1].iat[3,2] - regionlist[0].iat[3,2]) / regionlist[0].iat[3,2] * 100
            percent_cr_exps_total = (regionlist[1].iat[4,2] - regionlist[0].iat[4,2]) / regionlist[0].iat[4,2] * 100
            percent_change_d = {'Percentage Change':[percent_cr_exps_Central,percent_cr_exps_Keys,percent_cr_exps_North,percent_cr_exps_South,percent_cr_exps_total]} 


        regionlist[2] = pd.DataFrame(data=percent_change_d,index=[0,1,2,3,4])
        if tob != 'pr_lr': 
            regionlist[2]['AAL Inc(%)'] = (regionlist[1]['AAL']-regionlist[0]['AAL'])/regionlist[0]['AAL']*100
            regionlist[2]['Loss Costs Inc(%)'] = (regionlist[1]['Loss Costs/$1,000']-regionlist[0]['Loss Costs/$1,000'])/regionlist[0]['Loss Costs/$1,000']*100           
        regionlist[2] = regionlist[2].fillna(0) 

        return  regionlist

    @expose('/showRegion/<string:lastyear>/<string:thisyear>')
    @has_access
    def showRegion(self, lastyear, thisyear):

        tobSelectValue = request.args.get('type_of_building') if request.args.get('type_of_building') else 'pr_lr' 
        tobform = TOBForm(type_of_building=tobSelectValue)

        # number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)
        loss_costs_format = lambda x: '{:,.3f}'.format(x)

        yeartup = (lastyear, thisyear)
        regionlist = MyView.regionAna(yeartup,tobSelectValue)

        lastyear_exps_df = regionlist[0]
        thisyear_exps_df = regionlist[1]
        percent_exps_df = regionlist[2]
        result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)

        if tobSelectValue == 'pr_lr':
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='Region',title='Region',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format},columns=[lastyear,'Region','CR Exposure','LR Exposure','Total Change']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format,'CR Percentage Change':flt_percent_format,'LR Percentage Change':flt_percent_format,'Total Percentage Change':flt_percent_format},columns=[thisyear,'Region','CR Exposure','LR Exposure','Total Change','CR Percentage Change','LR Percentage Change','Total Percentage Change'])])
        else:
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='Region',title='Region',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'Exposure':flt_num_format,'Total Change':flt_percent_format,'AAL':flt_num_format,'Loss Costs/$1,000':loss_costs_format},columns=[lastyear,'Region','Exposure','Total Change','AAL','Loss Costs/$1,000']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'Exposure':flt_num_format,'Total Change':flt_percent_format,'Percentage Change':flt_percent_format,'Total Percentage Change':flt_percent_format,'AAL':flt_num_format,'AAL Inc(%)':flt_percent_format,'Loss Costs/$1,000':loss_costs_format,'Loss Costs Inc(%)':flt_percent_format},columns=[thisyear,'Region','Exposure','Total Change','Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)'])])




    @expose('/exportRegion/<string:tobSelectValue>/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def exportRegion(self, tobSelectValue, lastyear, thisyear, lastsim, thissim):

        yeartup = (lastyear, thisyear)
        yearlist = MyView.regionAna(yeartup,tobSelectValue)

        lastyear_exps_df = yearlist[0]
        thisyear_exps_df = yearlist[1]
        percent_exps_df = yearlist[2]

        if tobSelectValue == 'pr_lr' :
            result_df = pd.concat([lastyear_exps_df[[lastyear,'Region','CR Exposure','LR Exposure','Total Change']],thisyear_exps_df[[thisyear,'Region','CR Exposure','LR Exposure','Total Change']], percent_exps_df[['CR Percentage Change','LR Percentage Change']]], axis=1)
           
        else:
            result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)
            result_df = pd.concat([lastyear_exps_df[[lastyear,'Region','Exposure','Total Change','AAL','Loss Costs/$1,000']],result_df[[thisyear,'Region','Exposure','Total Change','Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)']]], axis=1)

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        #lastyear_exps_df.to_excel(writer, sheet_name=tobSelectValue,index=False,float_format="%.2f")
        result_df.to_excel(writer, sheet_name=tobSelectValue,index=False,float_format="%.2f")
        worksheet1 = writer.sheets[tobSelectValue]
        
        workbook = writer.book
        money_fmt = workbook.add_format({'num_format': '$#,##0.00'})
        percent_format = workbook.add_format({'num_format': '0.00%'})

        if tobSelectValue == 'pr_lr' :
            worksheet1.set_column('C:C', 20, money_fmt)
            worksheet1.set_column('D:D', 20, money_fmt)
            worksheet1.set_column('I:I', 20, money_fmt)
            worksheet1.set_column('H:H', 20, money_fmt)
        else:
            worksheet1.set_column('C:C', 20, money_fmt)
            worksheet1.set_column('E:E', 20, money_fmt)
            worksheet1.set_column('I:I', 20, money_fmt)
            worksheet1.set_column('L:L', 20, money_fmt)
        #the writer has done its job
        writer.close()

        #go back to the beginning of the stream
        output.seek(0)

        return send_file(output, attachment_filename="region.xlsx", as_attachment=True)

    @staticmethod
    def constructionAna(yeartup,tob):

        constructionlist = [1,2,3]

        i = 0

        for year in yeartup:
            # define path the different year
            year_path = 'app/data/' + year

            #defin year dataframe 
            #year_cr_risk = year_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
            year_lr = year_path + '/' + tob + '/valid_data.csv'

            #year_cr_df_risk = pd.read_csv(year_cr_risk,usecols=['Region','LMs', 'LMapp', 'LMc', 'LMale'])
            year_lr_df = pd.read_csv(year_lr,usecols=['ConstType','Units', 'LMs', 'LMapp', 'LMc', 'LMale','TotalLoss'])  

            year_lr_df_Frame = year_lr_df[year_lr_df['ConstType'] == 'Frame']
            year_lr_df_Masonry = year_lr_df[year_lr_df['ConstType'] == 'Masonry']
            year_lr_df_Other = year_lr_df[year_lr_df['ConstType'] == 'Other']

            #cr_exps_Central = year_cr_df_risk_Central.LMs.sum() + year_cr_df_risk_Central.LMapp.sum() + year_cr_df_risk_Central.LMc.sum() + year_cr_df_risk_Central.LMale.sum()
            lr_exps_Frame = ((year_lr_df_Frame.LMs + year_lr_df_Frame.LMapp + year_lr_df_Frame.LMc + year_lr_df_Frame.LMale) * year_lr_df_Frame.Units).sum()
            #cr_exps_Keys = year_cr_df_risk_Keys.LMs.sum() + year_cr_df_risk_Keys.LMapp.sum() + year_cr_df_risk_Keys.LMc.sum() + year_cr_df_risk_Keys.LMale.sum()
            lr_exps_Masonry = ((year_lr_df_Masonry.LMs + year_lr_df_Masonry.LMapp + year_lr_df_Masonry.LMc + year_lr_df_Masonry.LMale) * year_lr_df_Masonry.Units).sum()
            #cr_exps_North = year_cr_df_risk_North.LMs.sum() + year_cr_df_risk_North.LMapp.sum() + year_cr_df_risk_North.LMc.sum() + year_cr_df_risk_North.LMale.sum()
            lr_exps_Other = ((year_lr_df_Other.LMs + year_lr_df_Other.LMapp + year_lr_df_Other.LMc + year_lr_df_Other.LMale) * year_lr_df_Other.Units).sum()
            #cr_exps_total = cr_exps_Central + cr_exps_Keys + cr_exps_North + cr_exps_South
            lr_exps_total = lr_exps_Frame + lr_exps_Masonry + lr_exps_Other

            lr_aal_Frame = year_lr_df_Frame.TotalLoss.sum()
            lr_aal_Masonry = year_lr_df_Masonry.TotalLoss.sum()
            lr_aal_Other = year_lr_df_Other.TotalLoss.sum()
            lr_aal_total = year_lr_df.TotalLoss.sum()

            change_exps_Frame = (0 + lr_exps_Frame) / (0 + lr_exps_total) * 100
            change_exps_Masonry = (0 + lr_exps_Masonry) / (0 + lr_exps_total) * 100
            change_exps_Other = (0 + lr_exps_Other) / (0 + lr_exps_total) * 100

            if tob == 'pr_lr':
                construction_exps_d = {year: [1,2,3,4],
                                'Construction Type':['Frame','Masonry','Other','Total'],
                                'CR Exposure':[0,0,0,0],
                                'LR Exposure':[lr_exps_Frame,lr_exps_Masonry,lr_exps_Other,lr_exps_total],
                                'Total Change':[change_exps_Frame,change_exps_Masonry,change_exps_Other,100]}
            else:
                construction_exps_d = {year: [1,2,3,4],
                                'Construction Type':['Frame','Masonry','Other','Total'],
                                'Exposure':[lr_exps_Frame,lr_exps_Masonry,lr_exps_Other,lr_exps_total],
                                'Total Change':[change_exps_Frame,change_exps_Masonry,change_exps_Other,100],
                                'AAL':[lr_aal_Frame,lr_aal_Masonry,change_exps_Other,lr_aal_total]}

            construction_exps_df = pd.DataFrame(data=construction_exps_d,index=[0,1,2,3]) 
            if tob != 'pr_lr': 
                construction_exps_df['Loss Costs/$1,000'] = construction_exps_df['AAL']/construction_exps_df['Exposure']*1000

            constructionlist[i] = construction_exps_df.fillna(0)
            i = i + 1
      
        if tob == 'pr_lr':
            percent_lr_exps_Frame = (constructionlist[1].iat[0,3] - constructionlist[0].iat[0,3]) / constructionlist[0].iat[0,3] * 100
            percent_lr_exps_Masonry = (constructionlist[1].iat[1,3] - constructionlist[0].iat[1,3]) / constructionlist[0].iat[1,3] * 100
            percent_lr_exps_Other = (constructionlist[1].iat[2,3] - constructionlist[0].iat[2,3]) / constructionlist[0].iat[2,3] * 100
            percent_lr_exps_total = (constructionlist[1].iat[3,3] - constructionlist[0].iat[3,3]) / constructionlist[0].iat[3,3] * 100

            percent_change_d = {'CR Percentage Change':[0,0,0,0],
                                'LR Percentage Change':[percent_lr_exps_Frame,percent_lr_exps_Masonry,percent_lr_exps_Other,percent_lr_exps_total]} 
        else:
            percent_lr_exps_Frame = (constructionlist[1].iat[0,3] - constructionlist[0].iat[0,3]) / constructionlist[0].iat[0,3] * 100
            percent_lr_exps_Masonry = (constructionlist[1].iat[1,3] - constructionlist[0].iat[1,3]) / constructionlist[0].iat[1,3] * 100
            percent_lr_exps_Other = (constructionlist[1].iat[2,3] - constructionlist[0].iat[2,3]) / constructionlist[0].iat[2,3] * 100
            percent_lr_exps_total = (constructionlist[1].iat[3,3] - constructionlist[0].iat[3,3]) / constructionlist[0].iat[3,3] * 100

            percent_change_d = {'Percentage Change':[percent_lr_exps_Frame,percent_lr_exps_Masonry,percent_lr_exps_Other,percent_lr_exps_total]} 


        constructionlist[2] = pd.DataFrame(data=percent_change_d,index=[0,1,2,3]) 
        if tob != 'pr_lr': 
            constructionlist[2]['AAL Inc(%)'] = (constructionlist[1]['AAL']-constructionlist[0]['AAL'])/constructionlist[0]['AAL']*100
            constructionlist[2]['Loss Costs Inc(%)'] = (constructionlist[1]['Loss Costs/$1,000']-constructionlist[0]['Loss Costs/$1,000'])/constructionlist[0]['Loss Costs/$1,000']*100           
        constructionlist[2] = constructionlist[2].fillna(0)

        return  constructionlist

    @expose('/showConstruction/<string:lastyear>/<string:thisyear>')
    @has_access
    def showConstruction(self, lastyear, thisyear):

        tobSelectValue = request.args.get('type_of_building') if request.args.get('type_of_building') else 'pr_lr' 
        tobform = TOBForm(type_of_building=tobSelectValue)

        # number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)
        loss_costs_format = lambda x: '{:,.3f}'.format(x)

        yeartup = (lastyear, thisyear)
        constructionlist = MyView.constructionAna(yeartup,tobSelectValue)

        lastyear_exps_df = constructionlist[0]
        thisyear_exps_df = constructionlist[1]
        percent_exps_df = constructionlist[2]
        result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)

        if tobSelectValue == 'pr_lr':
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='Construction',title='Construction Type',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format},columns=[lastyear,'Construction Type','CR Exposure','LR Exposure','Total Change']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format,'CR Percentage Change':flt_percent_format,'LR Percentage Change':flt_percent_format,},columns=[thisyear,'Construction Type','CR Exposure','LR Exposure','Total Change','CR Percentage Change','LR Percentage Change'])])
        else:
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='Construction',title='Construction Type',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'Exposure':flt_num_format,'Total Change':flt_percent_format,'AAL':flt_num_format,'Loss Costs/$1,000':loss_costs_format},columns=[lastyear,'Construction Type','Exposure','Total Change','AAL','Loss Costs/$1,000']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'Exposure':flt_num_format,'Total Change':flt_percent_format,'Percentage Change':flt_percent_format,'AAL':flt_num_format,'AAL Inc(%)':flt_percent_format,'Loss Costs/$1,000':loss_costs_format,'Loss Costs Inc(%)':flt_percent_format},columns=[thisyear,'Construction Type','Exposure','Total Change','Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)'])])


    @expose('/exportConstruction/<string:tobSelectValue>/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def exportConstruction(self, tobSelectValue, lastyear, thisyear, lastsim, thissim):

        yeartup = (lastyear, thisyear)
        yearlist = MyView.constructionAna(yeartup,tobSelectValue)

        lastyear_exps_df = yearlist[0]
        thisyear_exps_df = yearlist[1]
        percent_exps_df = yearlist[2]

        if tobSelectValue == 'pr_lr' :
            result_df = pd.concat([lastyear_exps_df[[lastyear,'Construction Type','CR Exposure','LR Exposure','Total Change']],thisyear_exps_df[[thisyear,'Construction Type','CR Exposure','LR Exposure','Total Change']], percent_exps_df[['CR Percentage Change','LR Percentage Change']]], axis=1)
           
        else:
            result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)
            result_df = pd.concat([lastyear_exps_df[[lastyear,'Construction Type','Exposure','Total Change','AAL','Loss Costs/$1,000']],result_df[[thisyear,'Construction Type','Exposure','Total Change','Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)']]], axis=1)

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        #lastyear_exps_df.to_excel(writer, sheet_name=tobSelectValue,index=False,float_format="%.2f")
        result_df.to_excel(writer, sheet_name=tobSelectValue,index=False,float_format="%.2f")
        worksheet1 = writer.sheets[tobSelectValue]
        
        workbook = writer.book
        money_fmt = workbook.add_format({'num_format': '$#,##0.00'})
        percent_format = workbook.add_format({'num_format': '0.00%'})

        if tobSelectValue == 'pr_lr' :
            worksheet1.set_column('C:C', 20, money_fmt)
            worksheet1.set_column('D:D', 20, money_fmt)
            worksheet1.set_column('I:I', 20, money_fmt)
            worksheet1.set_column('H:H', 20, money_fmt)
        else:
            worksheet1.set_column('C:C', 20, money_fmt)
            worksheet1.set_column('E:E', 20, money_fmt)
            worksheet1.set_column('I:I', 20, money_fmt)
            worksheet1.set_column('L:L', 20, money_fmt)
        #the writer has done its job
        writer.close()

        #go back to the beginning of the stream
        output.seek(0)

        return send_file(output, attachment_filename="construction.xlsx", as_attachment=True)

    @staticmethod
    def countyAna(yeartup,tob):

        countylist = [1,2]

        i = 0

        for year in yeartup:
            # define path the different year
            year_path = 'app/data/' + year

            year_lr = year_path + '/'+tob+'/valid_data.csv'
            year_lr_df = pd.read_csv(year_lr,usecols=['County','Units', 'LMs', 'LMapp', 'LMc', 'LMale','TotalLoss'])
            year_lr_df['exp'] = (year_lr_df.LMs + year_lr_df.LMapp + year_lr_df.LMc + year_lr_df.LMale) * year_lr_df.Units
            year_lr_df_group = year_lr_df.groupby(['County']).agg(['sum'])
            year_lr_df_group['Exposure'] = year_lr_df_group[['exp']].sum(axis=1)      

            if tob == 'pr_lr':
                year_cr_risk = year_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
                year_cr_df_risk = pd.read_csv(year_cr_risk,usecols=['County','LMs', 'LMapp', 'LMc', 'LMale'])
                year_cr_df_risk_group = year_cr_df_risk.groupby(['County']).agg(['sum'])
                year_cr_df_risk_group['CR Exposure'] = year_cr_df_risk_group[['LMs','LMapp','LMc','LMale']].sum(axis=1)
                year_lr_df_group['LR Exposure'] = year_lr_df_group[['exp']].sum(axis=1)
                df_cr_lr = pd.concat([year_cr_df_risk_group[['CR Exposure']],year_lr_df_group[['LR Exposure']]],axis=1)
                df_cr_lr_fillna0 = df_cr_lr.fillna(0)
                cr_exps_total = df_cr_lr_fillna0['CR Exposure'].sum()                
                lr_exps_total = df_cr_lr_fillna0['LR Exposure'].sum()
                df_cr_lr_fillna0['Total Percentage'] = (df_cr_lr_fillna0['CR Exposure'] + df_cr_lr_fillna0['LR Exposure']) * 100 / (cr_exps_total + lr_exps_total) 
                df_cr_lr_fillna0_t = df_cr_lr_fillna0.T
                df_cr_lr_fillna0_t['Total'] = [cr_exps_total,lr_exps_total,100]
                
            else:
                year_lr_df_group['AAL'] = year_lr_df_group[['TotalLoss']].sum(axis=1) 
                year_lr_df_group['Loss Costs/$1,000'] = year_lr_df_group['AAL']/year_lr_df_group['Exposure']*1000
                df_cr_lr = pd.concat([year_lr_df_group[['Exposure']],year_lr_df_group[['AAL']],year_lr_df_group[['Loss Costs/$1,000']]],axis=1)
                df_cr_lr_fillna0 = df_cr_lr.fillna(0)
                lr_exps_total = df_cr_lr_fillna0['Exposure'].sum()
                lr_aal_total = df_cr_lr_fillna0['AAL'].sum()
                lr_losscost_total = lr_aal_total / lr_exps_total * 1000
                df_cr_lr_fillna0['Total Percentage'] = (df_cr_lr_fillna0['Exposure']) * 100 / (lr_exps_total)
                df_cr_lr_fillna0_t = df_cr_lr_fillna0.T
                df_cr_lr_fillna0_t['Total'] = [lr_exps_total,lr_aal_total,lr_losscost_total,100]

            df_cr_lr_fillna0 = df_cr_lr_fillna0_t.T
            df_cr_lr_fillna0.columns = [col[0] for col in df_cr_lr_fillna0.columns]

            #df_cr_lr_fillna0.loc[:,year] = pd.date_range(1, periods=len(df_cr_lr_fillna0))

            df_cr_lr_fillna0.index.name = 'County'
            countylist[i] = df_cr_lr_fillna0

            i = i + 1

        if tob == 'pr_lr':
            countylist[1]['CR Percentage Change'] = (countylist[1]['CR Exposure'] - countylist[0]['CR Exposure']) * 100 / countylist[0]['CR Exposure']
            countylist[1]['LR Percentage Change'] = (countylist[1]['LR Exposure'] - countylist[0]['LR Exposure']) * 100 / countylist[0]['LR Exposure']
            countylist[1]['Total Percentage Change'] = (countylist[1]['CR Exposure'] + countylist[1]['LR Exposure'] - countylist[0]['CR Exposure'] - countylist[0]['LR Exposure']) * 100 / (countylist[0]['CR Exposure'] + countylist[0]['LR Exposure'])      
        else:
            countylist[1]['Total Percentage Change'] = (countylist[1]['Exposure'] - countylist[0]['Exposure']) * 100 / countylist[0]['Exposure']
            countylist[1]['AAL Inc(%)'] = (countylist[1]['AAL'] - countylist[0]['AAL']) * 100 / countylist[0]['AAL']
            countylist[1]['Loss Costs Inc(%)'] = (countylist[1]['Loss Costs/$1,000'] - countylist[0]['Loss Costs/$1,000']) * 100 / countylist[0]['Loss Costs/$1,000']

        countylist[1] = countylist[1].fillna(0)
        countylist[1] = countylist[1].replace(np.inf, 0)

        return countylist

    @expose('/showCounty/<string:lastyear>/<string:thisyear>')
    @has_access
    def showCounty(self, lastyear, thisyear):

        tobSelectValue = request.args.get('type_of_building') if request.args.get('type_of_building') else 'pr_lr' 
        tobform = TOBForm(type_of_building=tobSelectValue)

        # number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)                
        loss_costs_format = lambda x: '{:,.3f}'.format(x)

        yeartup = (lastyear, thisyear)
        countylist = MyView.countyAna(yeartup,tobSelectValue)

        lastyear_exps_df = countylist[0]
        thisyear_exps_df = countylist[1]
        #lastyear_exps_df = pd.concat([countylist[0],countylist[1]],axis=1)

        if tobSelectValue == 'pr_lr':
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='County',title='County',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=True,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Percentage':flt_percent_format},columns=['CR Exposure','LR Exposure','Total Percentage'])
                                      ,thisyear_exps_df.to_html(classes='table table-bordered',index=True,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Percentage':flt_percent_format,'CR Percentage Change':flt_percent_format,'LR Percentage Change':flt_percent_format,'Total Percentage Change':flt_percent_format},columns=['CR Exposure','LR Exposure','Total Percentage','CR Percentage Change','LR Percentage Change','Total Percentage Change'])])
        else:
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='County',title='County',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=True,formatters={'Exposure':flt_num_format,'Total Percentage':flt_percent_format,'AAL':flt_num_format,'Loss Costs/$1,000':loss_costs_format},columns=['Exposure','Total Percentage','AAL','Loss Costs/$1,000'])
                                      ,thisyear_exps_df.to_html(classes='table table-bordered',index=True,formatters={'Exposure':flt_num_format,'Total Percentage':flt_percent_format,'Total Percentage Change':flt_percent_format,'AAL':flt_num_format,'AAL Inc(%)':flt_percent_format,'Loss Costs/$1,000':loss_costs_format,'Loss Costs Inc(%)':flt_percent_format},columns=['Exposure','Total Percentage','Total Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)'])])
    
    @expose('/showHeatChartCounty/<string:kpi>/<string:maptype>/<string:tobSelectValue>/<string:lastyear>/<string:thisyear>')
    @has_access
    def showHeatChartCounty(self, kpi, maptype, tobSelectValue, lastyear, thisyear):

        # number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)

        yeartup = (lastyear, thisyear)
        countylist = MyView.countyAna(yeartup,tobSelectValue)
        lastyear_exps_df = countylist[0]
        thisyear_exps_df = countylist[1]

        if kpi == 'exp' :
            maxValue = thisyear_exps_df['Total Percentage Change'].max()
            minValue = thisyear_exps_df['Total Percentage Change'].min()            
        elif kpi == 'aal' :
            maxValue = thisyear_exps_df['AAL Inc(%)'].max()
            minValue = thisyear_exps_df['AAL Inc(%)'].min()
        else:
            maxValue = thisyear_exps_df['Loss Costs Inc(%)'].max()
            minValue = thisyear_exps_df['Loss Costs Inc(%)'].min()
        
        #lastyear_exps_df = pd.concat([countylist[0],countylist[1]],axis=1)

        return self.render_template('heatChartForCounty.html',kpi=kpi,maptype=maptype,maxValue=maxValue,minValue=minValue,tob=tobSelectValue,lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,countyData=thisyear_exps_df.to_json())

    @expose('/exportCounty/<string:tobSelectValue>/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def exportCounty(self, tobSelectValue, lastyear, thisyear, lastsim, thissim):

        yeartup = (lastyear, thisyear)
        yearlist = MyView.countyAna(yeartup,tobSelectValue)

        lastyear_exps_df = yearlist[0]
        thisyear_exps_df = yearlist[1]

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        if tobSelectValue == 'pr_lr' :
            result_df = pd.concat([lastyear_exps_df[['CR Exposure','LR Exposure','Total Percentage']],thisyear_exps_df[['CR Exposure','LR Exposure','Total Percentage','CR Percentage Change','LR Percentage Change','Total Percentage Change']]], axis=0)
            result_df.to_excel(writer, sheet_name=tobSelectValue,index=True,float_format="%.2f",columns=['CR Exposure','LR Exposure','Total Percentage','CR Percentage Change','LR Percentage Change','Total Percentage Change'])
        else:
            result_df = pd.concat([lastyear_exps_df[['Exposure','Total Percentage','AAL','Loss Costs/$1,000']],thisyear_exps_df[['Exposure','Total Percentage','Total Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)']]], axis=0)
            result_df.to_excel(writer, sheet_name=tobSelectValue,index=True,float_format="%.2f",columns=['Exposure','Total Percentage','Total Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)'])
        
        worksheet1 = writer.sheets[tobSelectValue]
        
        workbook = writer.book
        money_fmt = workbook.add_format({'num_format': '$#,##0.00'})
        percent_format = workbook.add_format({'num_format': '0.00%'})

        if tobSelectValue == 'pr_lr' :
            worksheet1.set_column('C:C', 20, money_fmt)
            worksheet1.set_column('B:B', 20, money_fmt)
        else:
            worksheet1.set_column('B:B', 20, money_fmt)
            worksheet1.set_column('E:E', 20, money_fmt)
        #the writer has done its job
        writer.close()

        #go back to the beginning of the stream
        output.seek(0)

        return send_file(output, attachment_filename="county.xlsx", as_attachment=True)

    @staticmethod
    def zipAna(yeartup,tob):

        countylist = [1,2]

        i = 0

        for year in yeartup:
            # define path the different year
            year_path = 'app/data/' + year

            year_lr = year_path + '/'+tob+'/valid_data.csv'
            year_lr_df = pd.read_csv(year_lr,usecols=['Zipcode','Units', 'LMs', 'LMapp', 'LMc', 'LMale','TotalLoss'])
            year_lr_df['exp'] = (year_lr_df.LMs + year_lr_df.LMapp + year_lr_df.LMc + year_lr_df.LMale) * year_lr_df.Units
            year_lr_df_group = year_lr_df.groupby(['Zipcode']).agg(['sum'])
            year_lr_df_group['Exposure'] = year_lr_df_group[['exp']].sum(axis=1)
            year_lr_df_group.index = year_lr_df_group.index.astype(int)            

            if tob == 'pr_lr':
                year_cr_risk = year_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
                year_cr_df_risk = pd.read_csv(year_cr_risk,usecols=['ZipCode','LMs', 'LMapp', 'LMc', 'LMale'])
                year_cr_df_risk_group = year_cr_df_risk.groupby(['ZipCode']).agg(['sum'])
                year_cr_df_risk_group['CR Exposure'] = year_cr_df_risk_group[['LMs','LMapp','LMc','LMale']].sum(axis=1)
                year_lr_df_group['LR Exposure'] = year_lr_df_group[['exp']].sum(axis=1)
                df_cr_lr = pd.concat([year_cr_df_risk_group[['CR Exposure']],year_lr_df_group[['LR Exposure']]],axis=1)
                df_cr_lr_fillna0 = df_cr_lr.fillna(0)
                cr_exps_total = df_cr_lr_fillna0['CR Exposure'].sum()                
                lr_exps_total = df_cr_lr_fillna0['LR Exposure'].sum()
                df_cr_lr_fillna0['Total Percentage'] = (df_cr_lr_fillna0['CR Exposure'] + df_cr_lr_fillna0['LR Exposure']) * 100 / (cr_exps_total + lr_exps_total) 
                df_cr_lr_fillna0_t = df_cr_lr_fillna0.T
                df_cr_lr_fillna0_t['Total'] = [cr_exps_total,lr_exps_total,100]
                
            else:
                year_lr_df_group['AAL'] = year_lr_df_group[['TotalLoss']].sum(axis=1) 
                year_lr_df_group['Loss Costs/$1,000'] = year_lr_df_group['AAL']/year_lr_df_group['Exposure']*1000
                df_cr_lr = pd.concat([year_lr_df_group[['Exposure']],year_lr_df_group[['AAL']],year_lr_df_group[['Loss Costs/$1,000']]],axis=1)
                df_cr_lr_fillna0 = df_cr_lr.fillna(0)
                lr_exps_total = df_cr_lr_fillna0['Exposure'].sum()
                lr_aal_total = df_cr_lr_fillna0['AAL'].sum()
                lr_losscost_total = lr_aal_total / lr_exps_total * 1000
                df_cr_lr_fillna0['Total Percentage'] = (df_cr_lr_fillna0['Exposure']) * 100 / (lr_exps_total)
                df_cr_lr_fillna0_t = df_cr_lr_fillna0.T
                df_cr_lr_fillna0_t['Total'] = [lr_exps_total,lr_aal_total,lr_losscost_total,100]

            df_cr_lr_fillna0 = df_cr_lr_fillna0_t.T
            df_cr_lr_fillna0.columns = [col[0] for col in df_cr_lr_fillna0.columns]

            #df_cr_lr_fillna0.loc[:,year] = pd.date_range(1, periods=len(df_cr_lr_fillna0))

            df_cr_lr_fillna0.index.name = 'ZipCode'
            countylist[i] = df_cr_lr_fillna0

            i = i + 1

        if tob == 'pr_lr':
            countylist[1]['CR Percentage Change'] = (countylist[1]['CR Exposure'] - countylist[0]['CR Exposure']) * 100 / countylist[0]['CR Exposure']
            countylist[1]['LR Percentage Change'] = (countylist[1]['LR Exposure'] - countylist[0]['LR Exposure']) * 100 / countylist[0]['LR Exposure']
            countylist[1]['Total Percentage Change'] = (countylist[1]['CR Exposure'] + countylist[1]['LR Exposure'] - countylist[0]['CR Exposure'] - countylist[0]['LR Exposure']) * 100 / (countylist[0]['CR Exposure'] + countylist[0]['LR Exposure'])      
        else:
            countylist[1]['Total Percentage Change'] = (countylist[1]['Exposure'] - countylist[0]['Exposure']) * 100 / countylist[0]['Exposure']
            countylist[1]['AAL Inc(%)'] = (countylist[1]['AAL'] - countylist[0]['AAL']) * 100 / countylist[0]['AAL']
            countylist[1]['Loss Costs Inc(%)'] = (countylist[1]['Loss Costs/$1,000'] - countylist[0]['Loss Costs/$1,000']) * 100 / countylist[0]['Loss Costs/$1,000']

        
        countylist[1] = countylist[1].fillna(0)
        countylist[1] = countylist[1].replace(np.inf, 0)

        return countylist

    @expose('/showZipCode/<string:lastyear>/<string:thisyear>')
    @has_access
    def showZipCode(self, lastyear, thisyear):

        tobSelectValue = request.args.get('type_of_building') if request.args.get('type_of_building') else 'pr_lr' 
        tobform = TOBForm(type_of_building=tobSelectValue)

        # number format
        int_num_format = lambda x: '{:,.0f}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)
        loss_costs_format = lambda x: '{:,.3f}'.format(x)

        yeartup = (lastyear, thisyear)
        countylist = MyView.zipAna(yeartup,tobSelectValue)

        lastyear_exps_df = countylist[0]
        thisyear_exps_df = countylist[1]
        #lastyear_exps_df = pd.concat([countylist[0],countylist[1]],axis=1)

        if tobSelectValue == 'pr_lr':
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='ZipCode',title='ZipCode',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=True,formatters={'ZipCode':int_num_format,'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Percentage':flt_percent_format},columns=['CR Exposure','LR Exposure','Total Percentage'])
                                      ,thisyear_exps_df.to_html(classes='table table-bordered',index=True,formatters={'ZipCode':int_num_format,'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Percentage':flt_percent_format,'CR Percentage Change':flt_percent_format,'LR Percentage Change':flt_percent_format,'Total Percentage Change':flt_percent_format},columns=['CR Exposure','LR Exposure','Total Percentage','CR Percentage Change','LR Percentage Change','Total Percentage Change'])])
        else:
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='ZipCode',title='ZipCode',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=True,formatters={'ZipCode':int_num_format,'Exposure':flt_num_format,'Total Percentage':flt_percent_format,'AAL':flt_num_format,'Loss Costs/$1,000':loss_costs_format},columns=['Exposure','Total Percentage','AAL','Loss Costs/$1,000'])
                                      ,thisyear_exps_df.to_html(classes='table table-bordered',index=True,formatters={'ZipCode':int_num_format,'Exposure':flt_num_format,'Total Percentage':flt_percent_format,'Total Percentage Change':flt_percent_format,'AAL':flt_num_format,'AAL Inc(%)':flt_percent_format,'Loss Costs/$1,000':loss_costs_format,'Loss Costs Inc(%)':flt_percent_format},columns=['Exposure','Total Percentage','Total Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)'])])
    
    @expose('/showHeatChartZipCode/<string:kpi>/<string:maptype>/<string:tobSelectValue>/<string:lastyear>/<string:thisyear>')
    @has_access
    def showHeatChartZipCode(self, kpi, maptype, tobSelectValue, lastyear, thisyear):

        # number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)

        yeartup = (lastyear, thisyear)
        countylist = MyView.zipAna(yeartup,tobSelectValue)

        lastyear_exps_df = countylist[0]
        thisyear_exps_df = countylist[1]

        if kpi == 'exp' :
            maxValue = thisyear_exps_df['Total Percentage Change'].max()
            minValue = thisyear_exps_df['Total Percentage Change'].min()            
        elif kpi == 'aal' :
            maxValue = thisyear_exps_df['AAL Inc(%)'].max()
            minValue = thisyear_exps_df['AAL Inc(%)'].min()
        else:
            maxValue = thisyear_exps_df['Loss Costs Inc(%)'].max()
            minValue = thisyear_exps_df['Loss Costs Inc(%)'].min()
        #lastyear_exps_df = pd.concat([countylist[0],countylist[1]],axis=1)

        return self.render_template('heatChartForCounty.html',kpi=kpi,maptype=maptype,maxValue=maxValue,minValue=minValue,tob=tobSelectValue,lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,countyData=thisyear_exps_df.to_json())
    
    @expose('/exportZipCode/<string:tobSelectValue>/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def exportZipCode(self, tobSelectValue, lastyear, thisyear, lastsim, thissim):

        yeartup = (lastyear, thisyear)
        yearlist = MyView.zipAna(yeartup,tobSelectValue)

        lastyear_exps_df = yearlist[0]
        thisyear_exps_df = yearlist[1]

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        if tobSelectValue == 'pr_lr' :
            result_df = pd.concat([lastyear_exps_df[['CR Exposure','LR Exposure','Total Percentage']],thisyear_exps_df[['CR Exposure','LR Exposure','Total Percentage','CR Percentage Change','LR Percentage Change','Total Percentage Change']]], axis=0)
            result_df.to_excel(writer, sheet_name=tobSelectValue,index=True,float_format="%.2f",columns=['CR Exposure','LR Exposure','Total Percentage','CR Percentage Change','LR Percentage Change','Total Percentage Change'])
        else:
            result_df = pd.concat([lastyear_exps_df[['Exposure','Total Percentage','AAL','Loss Costs/$1,000']],thisyear_exps_df[['Exposure','Total Percentage','Total Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)']]], axis=0)
            result_df.to_excel(writer, sheet_name=tobSelectValue,index=True,float_format="%.2f",columns=['Exposure','Total Percentage','Total Percentage Change','AAL','AAL Inc(%)','Loss Costs/$1,000','Loss Costs Inc(%)'])
        
        worksheet1 = writer.sheets[tobSelectValue]
        
        workbook = writer.book
        money_fmt = workbook.add_format({'num_format': '$#,##0.00'})
        percent_format = workbook.add_format({'num_format': '0.00%'})

        if tobSelectValue == 'pr_lr' :
            worksheet1.set_column('B:B', 20, money_fmt)
            worksheet1.set_column('C:C', 20, money_fmt)
        else:
            worksheet1.set_column('B:B', 20, money_fmt)
            worksheet1.set_column('E:E', 20, money_fmt)
        #the writer has done its job
        writer.close()

        #go back to the beginning of the stream
        output.seek(0)

        return send_file(output, attachment_filename="zipcode.xlsx", as_attachment=True)

    @staticmethod
    def deducAna(yeartup,tob):

        yearlist = [1,2,3]

        i = 0

        for year in yeartup:
            # define path the different year
            year_path = 'app/data/' + year

            year_lr = year_path + '/'+tob+'/valid_data.csv'
            year_lr_df = pd.read_csv(year_lr,usecols=['Deduc','Units', 'LMs', 'LMapp', 'LMc', 'LMale','TotalLoss'])
            year_lr_df_eq_0 = year_lr_df[year_lr_df['Deduc'] == 0]
            year_lr_df_lt_500 = year_lr_df[(year_lr_df['Deduc'] > 0) & (year_lr_df['Deduc'] < 500)]
            year_lr_df_lt_1000 = year_lr_df[(year_lr_df['Deduc'] >= 500) & (year_lr_df['Deduc'] < 1000)]
            year_lr_df_lt_1500 = year_lr_df[(year_lr_df['Deduc'] >= 1000) & (year_lr_df['Deduc'] < 1500)]
            year_lr_df_lt_2000 = year_lr_df[(year_lr_df['Deduc'] >= 1500) & (year_lr_df['Deduc'] < 2000)]
            year_lr_df_gte_2000 = year_lr_df[year_lr_df['Deduc'] >= 2000]

            lr_exps_eq_0 = ((year_lr_df_eq_0.LMs + year_lr_df_eq_0.LMapp + year_lr_df_eq_0.LMc + year_lr_df_eq_0.LMale) * year_lr_df_eq_0.Units).sum()
            lr_exps_lt_500 = ((year_lr_df_lt_500.LMs + year_lr_df_lt_500.LMapp + year_lr_df_lt_500.LMc + year_lr_df_lt_500.LMale) * year_lr_df_lt_500.Units).sum()
            lr_exps_lt_1000 = ((year_lr_df_lt_1000.LMs + year_lr_df_lt_1000.LMapp + year_lr_df_lt_1000.LMc + year_lr_df_lt_1000.LMale) * year_lr_df_lt_1000.Units).sum()
            lr_exps_lt_1500 = ((year_lr_df_lt_1500.LMs + year_lr_df_lt_1500.LMapp + year_lr_df_lt_1500.LMc + year_lr_df_lt_1500.LMale) * year_lr_df_lt_1500.Units).sum()
            lr_exps_lt_2000 = ((year_lr_df_lt_2000.LMs + year_lr_df_lt_2000.LMapp + year_lr_df_lt_2000.LMc + year_lr_df_lt_2000.LMale) * year_lr_df_lt_2000.Units).sum()
            lr_exps_gte_2000 = ((year_lr_df_gte_2000.LMs + year_lr_df_gte_2000.LMapp + year_lr_df_gte_2000.LMc + year_lr_df_gte_2000.LMale) * year_lr_df_gte_2000.Units).sum()
            lr_exps_total = lr_exps_eq_0 + lr_exps_lt_500 + lr_exps_lt_1000 + lr_exps_lt_1500 + lr_exps_lt_2000 + lr_exps_gte_2000

            lr_policy_eq_0 = year_lr_df_eq_0.Deduc.count()
            lr_policy_lt_500 = year_lr_df_lt_500.Deduc.count()
            lr_policy_lt_1000 = year_lr_df_lt_1000.Deduc.count()
            lr_policy_lt_1500 = year_lr_df_lt_1500.Deduc.count()
            lr_policy_lt_2000 = year_lr_df_lt_2000.Deduc.count()
            lr_policy_gte_2000 = year_lr_df_gte_2000.Deduc.count()
            lr_policy_total = year_lr_df.Deduc.count()

            if tob == 'pr_lr': 
                year_cr_risk = year_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
                year_cr_df_risk = pd.read_csv(year_cr_risk,usecols=['Deduc','LMs', 'LMapp', 'LMc', 'LMale'])
                year_cr_df_eq_0 = year_cr_df_risk[year_cr_df_risk['Deduc'] == 0]
                year_cr_df_lt_500 = year_cr_df_risk[(year_cr_df_risk['Deduc'] > 0) & (year_cr_df_risk['Deduc'] < 500)]
                year_cr_df_lt_1000 = year_cr_df_risk[(year_cr_df_risk['Deduc'] >= 500) & (year_cr_df_risk['Deduc'] < 1000)]
                year_cr_df_lt_1500 = year_cr_df_risk[(year_cr_df_risk['Deduc'] >= 1000) & (year_cr_df_risk['Deduc'] < 1500)]
                year_cr_df_lt_2000 = year_cr_df_risk[(year_cr_df_risk['Deduc'] >= 1500) & (year_cr_df_risk['Deduc'] < 2000)]
                year_cr_df_gte_2000 = year_cr_df_risk[year_cr_df_risk['Deduc'] >= 2000]

                cr_exps_eq_0 = ((year_cr_df_eq_0.LMs + year_cr_df_eq_0.LMapp + year_cr_df_eq_0.LMc + year_cr_df_eq_0.LMale) ).sum()
                cr_exps_eq_0 = 0 if pd.isna(cr_exps_eq_0) else cr_exps_eq_0
                cr_exps_lt_500 = ((year_cr_df_lt_500.LMs + year_cr_df_lt_500.LMapp + year_cr_df_lt_500.LMc + year_cr_df_lt_500.LMale) ).sum()
                cr_exps_lt_1000 = ((year_cr_df_lt_1000.LMs + year_cr_df_lt_1000.LMapp + year_cr_df_lt_1000.LMc + year_cr_df_lt_1000.LMale) ).sum()
                cr_exps_lt_1500 = ((year_cr_df_lt_1500.LMs + year_cr_df_lt_1500.LMapp + year_cr_df_lt_1500.LMc + year_cr_df_lt_1500.LMale) ).sum()
                cr_exps_lt_2000 = ((year_cr_df_lt_2000.LMs + year_cr_df_lt_2000.LMapp + year_cr_df_lt_2000.LMc + year_cr_df_lt_2000.LMale) ).sum()
                cr_exps_gte_2000 = ((year_cr_df_gte_2000.LMs + year_cr_df_gte_2000.LMapp + year_cr_df_gte_2000.LMc + year_cr_df_gte_2000.LMale) ).sum()
                cr_exps_total = cr_exps_eq_0 + cr_exps_lt_500 + cr_exps_lt_1000 + cr_exps_lt_1500 + cr_exps_lt_2000 + cr_exps_gte_2000

                change_exps_eq_0 = (cr_exps_eq_0 + lr_exps_eq_0) / (cr_exps_total + lr_exps_total) * 100
                change_exps_lt_500 = (cr_exps_lt_500 + lr_exps_lt_500) / (cr_exps_total + lr_exps_total) * 100
                change_exps_lt_1000 = (cr_exps_lt_1000 + lr_exps_lt_1000) / (cr_exps_total + lr_exps_total) * 100
                change_exps_lt_1500 = (cr_exps_lt_1500 + lr_exps_lt_1500) / (cr_exps_total + lr_exps_total) * 100
                change_exps_lt_2000 = (cr_exps_lt_2000 + lr_exps_lt_2000) / (cr_exps_total + lr_exps_total) * 100
                change_exps_gte_2000 = (cr_exps_gte_2000 + lr_exps_gte_2000) / (cr_exps_total + lr_exps_total) * 100

                year_exps_d = { year: [1,2,3,4,5,6,7],
                                'Deductible':['=$0','($0~$500)','[$500~$1000)','[$1000~$1500)','[$1500~$2000)','>=$2000','Total'],
                                'CR Exposure':[cr_exps_eq_0,cr_exps_lt_500,cr_exps_lt_1000,cr_exps_lt_1500,cr_exps_lt_2000,cr_exps_gte_2000,cr_exps_total],
                                'LR Exposure':[lr_exps_eq_0,lr_exps_lt_500,lr_exps_lt_1000,lr_exps_lt_1500,lr_exps_lt_2000,lr_exps_gte_2000,lr_exps_total],
                                'Total Change':[change_exps_eq_0,change_exps_lt_500,change_exps_lt_1000,change_exps_lt_1500,change_exps_lt_2000,change_exps_gte_2000,100]}

            
            else:
                
                change_exps_eq_0 = lr_exps_eq_0 / lr_exps_total * 100
                change_exps_lt_500 = lr_exps_lt_500 / lr_exps_total * 100
                change_exps_lt_1000 = lr_exps_lt_1000 / lr_exps_total * 100
                change_exps_lt_1500 = lr_exps_lt_1500 / lr_exps_total * 100
                change_exps_lt_2000 = lr_exps_lt_2000 / lr_exps_total * 100
                change_exps_gte_2000 = lr_exps_gte_2000 / lr_exps_total * 100

                change_policy_eq_0 = lr_policy_eq_0 / lr_policy_total * 100
                change_policy_lt_500 = lr_policy_lt_500 / lr_policy_total * 100
                change_policy_lt_1000 = lr_policy_lt_1000 / lr_policy_total * 100
                change_policy_lt_1500 = lr_policy_lt_1500 / lr_policy_total * 100
                change_policy_lt_2000 = lr_policy_lt_2000 / lr_policy_total * 100
                change_policy_gte_2000 = lr_policy_gte_2000 / lr_policy_total * 100

                year_exps_d = { year: [1,2,3,4,5,6,7],
                                'Deductible':['=$0','($0~$500)','[$500~$1000)','[$1000~$1500)','[$1500~$2000)','>=$2000','Total'],
                                'Exposure':[lr_exps_eq_0,lr_exps_lt_500,lr_exps_lt_1000,lr_exps_lt_1500,lr_exps_lt_2000,lr_exps_gte_2000,lr_exps_total],
                                'Exp Total Change':[change_exps_eq_0,change_exps_lt_500,change_exps_lt_1000,change_exps_lt_1500,change_exps_lt_2000,change_exps_gte_2000,100],
                                'Policy Count':[lr_policy_eq_0,lr_policy_lt_500,lr_policy_lt_1000,lr_policy_lt_1500,lr_policy_lt_2000,lr_policy_gte_2000,lr_policy_total],
                                'Policy Total Change':[change_policy_eq_0,change_policy_lt_500,change_policy_lt_1000,change_policy_lt_1500,change_policy_lt_2000,change_policy_gte_2000,100]}
 
            year_exps_df = pd.DataFrame(data=year_exps_d,index=[0,1,2,3,4,5,6])
            #if tob != 'pr_lr': 
            #    year_exps_df['Loss Costs/$1,000'] = year_exps_df['AAL']/year_exps_df['Exposure']*1000
           
            yearlist[i] = year_exps_df.fillna(0)
            i = i + 1

        if tob == 'pr_lr':

            percent_cr_exps_eq_0 = (yearlist[1].iat[0,1] - yearlist[0].iat[0,1]) / yearlist[0].iat[0,1] * 100
            percent_cr_exps_lt_500 = (yearlist[1].iat[1,1] - yearlist[0].iat[1,1]) / yearlist[0].iat[1,1] * 100
            percent_cr_exps_lt_1000 = (yearlist[1].iat[2,1] - yearlist[0].iat[2,1]) / yearlist[0].iat[2,1] * 100
            percent_cr_exps_lt_1500 = (yearlist[1].iat[3,1] - yearlist[0].iat[3,1]) / yearlist[0].iat[3,1] * 100
            percent_cr_exps_lt_2000 = (yearlist[1].iat[4,1] - yearlist[0].iat[4,1]) / yearlist[0].iat[4,1] * 100
            percent_cr_exps_gte_2000 = (yearlist[1].iat[5,1] - yearlist[0].iat[5,1]) / yearlist[0].iat[5,1] * 100
            percent_cr_exps_total = (yearlist[1].iat[6,1] - yearlist[0].iat[6,1]) / yearlist[0].iat[6,1] * 100

            percent_lr_exps_eq_0 = (yearlist[1].iat[0,3] - yearlist[0].iat[0,3]) / yearlist[0].iat[0,3] * 100
            percent_lr_exps_lt_500 = (yearlist[1].iat[1,3] - yearlist[0].iat[1,3]) / yearlist[0].iat[1,3] * 100
            percent_lr_exps_lt_1000 = (yearlist[1].iat[2,3] - yearlist[0].iat[2,3]) / yearlist[0].iat[2,3] * 100
            percent_lr_exps_lt_1500 = (yearlist[1].iat[3,3] - yearlist[0].iat[3,3]) / yearlist[0].iat[3,3] * 100
            percent_lr_exps_lt_2000 = (yearlist[1].iat[4,3] - yearlist[0].iat[4,3]) / yearlist[0].iat[4,3] * 100
            percent_lr_exps_gte_2000 = (yearlist[1].iat[5,3] - yearlist[0].iat[5,3]) / yearlist[0].iat[5,3] * 100
            percent_lr_exps_total = (yearlist[1].iat[6,3] - yearlist[0].iat[6,3]) / yearlist[0].iat[6,3] * 100

            percent_change_d = {'CR Percentage Change':[percent_cr_exps_eq_0,percent_cr_exps_lt_500,percent_cr_exps_lt_1000,percent_cr_exps_lt_1500,percent_cr_exps_lt_2000,percent_cr_exps_gte_2000,percent_cr_exps_total],
                            'LR Percentage Change':[percent_lr_exps_eq_0,percent_lr_exps_lt_500,percent_lr_exps_lt_1000,percent_lr_exps_lt_1500,percent_lr_exps_lt_2000,percent_lr_exps_gte_2000,percent_lr_exps_total]} 
        else:
            percent_cr_exps_eq_0 = (yearlist[1].iat[0,2] - yearlist[0].iat[0,2]) / yearlist[0].iat[0,2] * 100
            percent_cr_exps_lt_500 = (yearlist[1].iat[1,2] - yearlist[0].iat[1,2]) / yearlist[0].iat[1,2] * 100
            percent_cr_exps_lt_1000 = (yearlist[1].iat[2,2] - yearlist[0].iat[2,2]) / yearlist[0].iat[2,2] * 100
            percent_cr_exps_lt_1500 = (yearlist[1].iat[3,2] - yearlist[0].iat[3,2]) / yearlist[0].iat[3,2] * 100
            percent_cr_exps_lt_2000 = (yearlist[1].iat[4,2] - yearlist[0].iat[4,2]) / yearlist[0].iat[4,2] * 100
            percent_cr_exps_gte_2000 = (yearlist[1].iat[5,2] - yearlist[0].iat[5,2]) / yearlist[0].iat[5,2] * 100
            percent_cr_exps_total = (yearlist[1].iat[6,2] - yearlist[0].iat[6,2]) / yearlist[0].iat[6,2] * 100

            percent_cr_exps_eq_0 = (yearlist[1].iat[0,3] - yearlist[0].iat[0,3]) / yearlist[0].iat[0,3] * 100
            percent_cr_exps_lt_500 = (yearlist[1].iat[1,3] - yearlist[0].iat[1,3]) / yearlist[0].iat[1,3] * 100
            percent_cr_exps_lt_1000 = (yearlist[1].iat[2,3] - yearlist[0].iat[2,3]) / yearlist[0].iat[2,3] * 100
            percent_cr_exps_lt_1500 = (yearlist[1].iat[3,3] - yearlist[0].iat[3,3]) / yearlist[0].iat[3,3] * 100
            percent_cr_exps_lt_2000 = (yearlist[1].iat[4,3] - yearlist[0].iat[4,3]) / yearlist[0].iat[4,3] * 100
            percent_cr_exps_gte_2000 = (yearlist[1].iat[5,3] - yearlist[0].iat[5,3]) / yearlist[0].iat[5,3] * 100
            percent_cr_exps_total = (yearlist[1].iat[6,3] - yearlist[0].iat[6,3]) / yearlist[0].iat[6,3] * 100
            percent_change_d = {'Exp Percentage Change':[percent_cr_exps_eq_0,percent_cr_exps_lt_500,percent_cr_exps_lt_1000,percent_cr_exps_lt_1500,percent_cr_exps_lt_2000,percent_cr_exps_gte_2000,percent_cr_exps_total]} 

        yearlist[2] = pd.DataFrame(data=percent_change_d,index=[0,1,2,3,4,5,6])
        yearlist[2]['Policy Percentage Change'] = (yearlist[1]['Policy Count'] - yearlist[0]['Policy Count'])/yearlist[0]['Policy Count']*100 
        #if tob != 'pr_lr': 
        #    yearlist[2]['AAL Inc(%)'] = (yearlist[1]['AAL']-yearlist[0]['AAL'])/yearlist[0]['AAL']*100
        #    yearlist[2]['Loss Costs Inc(%)'] = (yearlist[1]['Loss Costs/$1,000']-yearlist[0]['Loss Costs/$1,000'])/yearlist[0]['Loss Costs/$1,000']*100           
        yearlist[2] = yearlist[2].fillna(0)
        return yearlist

    @expose('/showDeduc/<string:lastyear>/<string:thisyear>')
    @has_access
    def showDeduc(self, lastyear, thisyear):

        tobSelectValue = request.args.get('type_of_building') if request.args.get('type_of_building') else 'pr_lr' 
        tobform = TOBForm(type_of_building=tobSelectValue)

        # number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)
        loss_costs_format = lambda x: '{:,.3f}'.format(x)

        yeartup = (lastyear, thisyear)
        yearlist = MyView.deducAna(yeartup,tobSelectValue)

        lastyear_exps_df = yearlist[0]
        thisyear_exps_df = yearlist[1]
        percent_exps_df = yearlist[2]
        result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)

        if tobSelectValue == 'pr_lr' :
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='Deduc',title='Deductible',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format},columns=[lastyear,'Deductible','CR Exposure','LR Exposure','Total Change']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format,'CR Percentage Change':flt_percent_format,'LR Percentage Change':flt_percent_format},columns=[thisyear,'Deductible','CR Exposure','LR Exposure','Total Change','CR Percentage Change','LR Percentage Change'])])
        else:
            return self.render_template('distribution.html',lyear=lastyear,tyear=thisyear,lsim=2017,tsim=2018,analytype='Deduc',title='Deductible',form=tobform,tobSelectValue=tobSelectValue,
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'Exposure':flt_num_format,'Exp Total Change':flt_percent_format,'Policy Count':int_num_format,'Policy Total Change':flt_percent_format},columns=[lastyear,'Deductible','Exposure','Exp Total Change','Policy Count','Policy Total Change']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'Exposure':flt_num_format,'Exp Total Change':flt_percent_format,'Exp Percentage Change':flt_percent_format,'Policy Count':int_num_format,'Policy Total Change':flt_percent_format,'Policy Percentage Change':flt_percent_format},columns=[thisyear,'Deductible','Exposure','Exp Total Change','Exp Percentage Change','Policy Count','Policy Total Change','Policy Percentage Change'])])

    @expose('/exportDeduc/<string:tobSelectValue>/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def exportDeduc(self, tobSelectValue ,lastyear, thisyear, lastsim, thissim):

        yeartup = (lastyear, thisyear)
        yearlist = MyView.deducAna(yeartup,tobSelectValue)

        lastyear_exps_df = yearlist[0]
        thisyear_exps_df = yearlist[1]
        percent_exps_df = yearlist[2]

        if tobSelectValue == 'pr_lr' :
            result_df = pd.concat([lastyear_exps_df[[lastyear,'Deductible','CR Exposure','LR Exposure','Total Change']],thisyear_exps_df[[thisyear,'Deductible','CR Exposure','LR Exposure','Total Change']], percent_exps_df[['CR Percentage Change','LR Percentage Change']]], axis=1)
        else:
            result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)
            result_df = pd.concat([lastyear_exps_df[[lastyear,'Deductible','Exposure','Exp Total Change','Policy Count','Policy Total Change']],result_df[[thisyear,'Deductible','Exposure','Exp Total Change','Exp Percentage Change','Policy Count','Policy Total Change','Policy Percentage Change']]], axis=1)

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        #lastyear_exps_df.to_excel(writer, sheet_name=tobSelectValue,index=False,float_format="%.2f")
        result_df.to_excel(writer, sheet_name=tobSelectValue,index=False,float_format="%.2f")
        worksheet1 = writer.sheets[tobSelectValue]
        
        workbook = writer.book
        money_fmt = workbook.add_format({'num_format': '$#,##0.00'})
        percent_format = workbook.add_format({'num_format': '0.00%'})

        if tobSelectValue == 'pr_lr' :
            worksheet1.set_column('C:C', 20, money_fmt)
            worksheet1.set_column('D:D', 20, money_fmt)
            worksheet1.set_column('I:I', 20, money_fmt)
            worksheet1.set_column('H:H', 20, money_fmt)
        else:
            worksheet1.set_column('C:C', 20, money_fmt)
            worksheet1.set_column('E:E', 20, money_fmt)
            worksheet1.set_column('I:I', 20, money_fmt)
            worksheet1.set_column('L:L', 20, money_fmt)
        #the writer has done its job
        writer.close()

        #go back to the beginning of the stream
        output.seek(0)

        return send_file(output, attachment_filename="deductible.xlsx", as_attachment=True)

#appbuilder.add_view(MyView(), "Method1", category='My View')
#appbuilder.add_view(MyView(), "Method2", href='/myview/method2/jonh', category='My View')
# Use add link instead there is no need to create MyView twice.
#appbuilder.add_link("Method2", href='/myview/method2/jonh', category='My View')
appbuilder.add_view(MyView(),"comparisons", href='/myview/showComparisons/2017/2018/57000/58000', category='My View')
appbuilder.add_link("yearbuild", href='/myview/showYearbuild/2017/2018', category='My View')
appbuilder.add_link("region", href='/myview/showRegion/2017/2018', category='My View')
appbuilder.add_link("county", href='/myview/showCounty/2017/2018', category='My View')
appbuilder.add_link("zipcode", href='/myview/showZipCode/2017/2018', category='My View')
appbuilder.add_link("construction", href='/myview/showConstruction/2017/2018', category='My View')
appbuilder.add_link("deductible", href='/myview/showDeduc/2017/2018', category='My View')

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404
