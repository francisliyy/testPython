from flask import render_template, make_response
from flask_appbuilder import BaseView, expose, has_access
from app import appbuilder
import pandas as pd
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
        lastyear_cr_df_risk = pd.read_csv(lastyear_cr_risk,usecols=['LMs', 'LMapp', 'LMc', 'LMale', 'RiskTotalLoss'])        
        lastyear_lr_df = pd.read_csv(lastyear_lr,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        lastyear_residential_df = pd.read_csv(lastyear_residential,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        lastyear_mobile_df = pd.read_csv(lastyear_mobile,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        lastyear_rental_df = pd.read_csv(lastyear_rental,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        lastyear_condo_df = pd.read_csv(lastyear_condo,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        
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




        lastyear_comparison_d = {lastyear: [1,2,3,4,5,6],
                                 'TOB' : ['Commercial','Residential','Mobile Homes','Tenants','Condos','TOTAL'],
                                 'Total Unit Count' : [lastyear_commercial_units,lastyear_residential_units,lastyear_mobile_units,lastyear_rental_units,lastyear_condo_units,lastyear_total_units],
                                 'Unit Inc (%)' : [0,0,0,0,0,0],
                                 'Exp' : [lastyear_commercial_exps,lastyear_residential_exps,lastyear_mobile_exps,lastyear_rental_exps,lastyear_condo_exps,lastyear_total_exps],
                                 'Exp Inc (%)' : [0,0,0,0,0,0],
                                 'AAL' : [lastyear_commercial_aal,lastyear_residential_aal,lastyear_mobile_aal,lastyear_rental_aal,lastyear_condo_aal,lastyear_total_aal],
                                 'AAL Inc (%)' : [0,0,0,0,0,0]}
        lastyear_comparison_df = pd.DataFrame(data=lastyear_comparison_d)
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
        thisyear_cr_df_risk = pd.read_csv(thisyear_cr_risk,usecols=['LMs', 'LMapp', 'LMc', 'LMale', 'RiskTotalLoss'])
        thisyear_lr_df = pd.read_csv(thisyear_lr,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        thisyear_residential_df = pd.read_csv(thisyear_residential,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        thisyear_mobile_df = pd.read_csv(thisyear_mobile,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        thisyear_rental_df = pd.read_csv(thisyear_rental,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        thisyear_condo_df = pd.read_csv(thisyear_condo,usecols=['Units', 'LMs', 'LMapp', 'LMc', 'LMale', 'TotalLoss'])
        
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

        thisyear_comparison_d = {thisyear: [1,2,3,4,5,6],
                                 'TOB' : ['Commercial','Residential','Mobile Homes','Tenants','Condos','TOTAL'],
                                 'Total Unit Count' : [thisyear_commercial_units,thisyear_residential_units,thisyear_mobile_units,thisyear_rental_units,thisyear_condo_units,thisyear_total_units],
                                 'Unit Inc (%)' : [thisyear_commercial_units_ratio,thisyear_residential_units_ratio ,thisyear_mobile_units_ratio ,thisyear_rental_units_ratio ,thisyear_condo_units_ratio ,thisyear_total_units_ratio],
                                 'Exp' : [thisyear_commercial_exps,thisyear_residential_exps,thisyear_mobile_exps,thisyear_rental_exps,thisyear_condo_exps,thisyear_total_exps],
                                 'Exp Inc (%)' : [thisyear_commercial_exps_ratio,thisyear_residential_exps_ratio,thisyear_mobile_exps_ratio,thisyear_rental_exps_ratio,thisyear_condo_exps_ratio,thisyear_total_exps_ratio],
                                 'AAL' : [thisyear_commercial_aal,thisyear_residential_aal,thisyear_mobile_aal,thisyear_rental_aal,thisyear_condo_aal,thisyear_total_aal],
                                 'AAL Inc (%)' : [thisyear_commercial_aal_ratio,thisyear_residential_aal_ratio,thisyear_mobile_aal_ratio,thisyear_rental_aal_ratio,thisyear_condo_aal_ratio,thisyear_total_aal_ratio]}        
        thisyear_comparison_df = pd.DataFrame(data=thisyear_comparison_d)

        return [lastyear_comparison_df,thisyear_comparison_df]   
        #thisyear_comparison_df.style.format({'Unit Inc (%)':'{:.2%}','Exp Inc (%)':'{:.2%}','AAL Inc (%)':'{:.2%}'})    

    @expose('/showComparisons/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def showComparisons(self, lastyear, thisyear, lastsim, thissim):

    	# number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)

        tables = MyView.comparisons(lastyear, thisyear, lastsim, thissim)
        lastyear_comparison_df = tables[0]
        thisyear_comparison_df = tables[1]

        return self.render_template('export.html',lyear=lastyear,tyear=thisyear,lsim=lastsim,tsim=thissim,analytype='exportComparisons',title='CatFund Comparisons',
                               tables=[lastyear_comparison_df.to_html(classes='table table-bordered',index=False,formatters={'Total Unit Count':int_num_format,'Exp':flt_num_format,'AAL':flt_num_format},columns=[lastyear,'TOB','Total Unit Count','Unit Inc (%)','Exp','Exp Inc (%)','AAL','AAL Inc (%)']),
                                       thisyear_comparison_df.to_html(classes='table table-bordered',index=False,formatters={'Total Unit Count':int_num_format,'Unit Inc (%)':flt_percent_format,'Exp':flt_num_format,'Exp Inc (%)':flt_percent_format,'AAL':flt_num_format,'AAL Inc (%)':flt_percent_format},columns=[thisyear,'TOB','Total Unit Count','Unit Inc (%)','Exp','Exp Inc (%)','AAL','AAL Inc (%)'])])

    @expose('/exportComparisons/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def exportComparisons(self, lastyear, thisyear, lastsim, thissim):

        tables = MyView.comparisons(lastyear, thisyear, lastsim, thissim)
        lastyear_comparison_df = tables[0]
        thisyear_comparison_df = tables[1]

        df = pd.concat([lastyear_comparison_df[['TOB','Total Unit Count','Unit Inc (%)','Exp','Exp Inc (%)','AAL','AAL Inc (%)']],thisyear_comparison_df[['TOB','Total Unit Count','Unit Inc (%)','Exp','Exp Inc (%)','AAL','AAL Inc (%)']]])
        index = 0
        first_col = [lastyear,lastyear,lastyear,lastyear,lastyear,lastyear,thisyear,thisyear,thisyear,thisyear,thisyear,thisyear]
        df.insert(loc=index,column='year',value=first_col)

        resp = make_response(df.to_csv(index=False))
        resp.headers["Content-Disposition"] = "attachment; filename=Comparison.csv"
        resp.headers["Content-Type"] = "text/csv"

        return resp

    @staticmethod
    def yearbuild(yeartup):

        yearlist = [1,2,3]

        i = 0

        for year in yeartup:
    	    # define path the different year
            year_path = 'app/data/' + year

            #defin year dataframe 
            year_cr_risk = year_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
            year_lr = year_path + '/pr_lr/valid_data.csv'

            year_cr_df_risk = pd.read_csv(year_cr_risk,usecols=['YearBuilt','LMs', 'LMapp', 'LMc', 'LMale'])
            year_lr_df = pd.read_csv(year_lr,usecols=['YearBuilt','Units', 'LMs', 'LMapp', 'LMc', 'LMale'])

            year_cr_df_risk_lt_1970 = year_cr_df_risk[year_cr_df_risk['YearBuilt'] < 1970]
            year_cr_df_risk_lte_1983 = year_cr_df_risk[(year_cr_df_risk['YearBuilt'] >= 1970) & (year_cr_df_risk['YearBuilt'] <= 1983)]
            year_cr_df_risk_lte_1993 = year_cr_df_risk[(year_cr_df_risk['YearBuilt'] >= 1984) & (year_cr_df_risk['YearBuilt'] <= 1993)]
            year_cr_df_risk_gte_1994 = year_cr_df_risk[year_cr_df_risk['YearBuilt'] >= 1994]

            year_lr_df_lt_1970 = year_lr_df[year_lr_df['YearBuilt'] < 1970]
            year_lr_df_lte_1983 = year_lr_df[(year_lr_df['YearBuilt'] >= 1970) & (year_lr_df['YearBuilt'] <= 1983)]
            year_lr_df_lte_1993 = year_lr_df[(year_lr_df['YearBuilt'] >= 1984) & (year_lr_df['YearBuilt'] <= 1993)]
            year_lr_df_gte_1994 = year_lr_df[year_lr_df['YearBuilt'] >= 1994]

            cr_exps_lt_1970 = year_cr_df_risk_lt_1970.LMs.sum() + year_cr_df_risk_lt_1970.LMapp.sum() + year_cr_df_risk_lt_1970.LMc.sum() + year_cr_df_risk_lt_1970.LMale.sum()
            lr_exps_lt_1970 = ((year_lr_df_lt_1970.LMs + year_lr_df_lt_1970.LMapp + year_lr_df_lt_1970.LMc + year_lr_df_lt_1970.LMale) * year_lr_df_lt_1970.Units).sum()
            cr_exps_lte_1983 = year_cr_df_risk_lte_1983.LMs.sum() + year_cr_df_risk_lte_1983.LMapp.sum() + year_cr_df_risk_lte_1983.LMc.sum() + year_cr_df_risk_lte_1983.LMale.sum()
            lr_exps_lte_1983 = ((year_lr_df_lte_1983.LMs + year_lr_df_lte_1983.LMapp + year_lr_df_lte_1983.LMc + year_lr_df_lte_1983.LMale) * year_lr_df_lte_1983.Units).sum()
            cr_exps_lte_1993 = year_cr_df_risk_lte_1993.LMs.sum() + year_cr_df_risk_lte_1993.LMapp.sum() + year_cr_df_risk_lte_1993.LMc.sum() + year_cr_df_risk_lte_1993.LMale.sum()
            lr_exps_lte_1993 = ((year_lr_df_lte_1993.LMs + year_lr_df_lte_1993.LMapp + year_lr_df_lte_1993.LMc + year_lr_df_lte_1993.LMale) * year_lr_df_lte_1993.Units).sum()
            cr_exps_gte_1994 = year_cr_df_risk_gte_1994.LMs.sum() + year_cr_df_risk_gte_1994.LMapp.sum() + year_cr_df_risk_gte_1994.LMc.sum() + year_cr_df_risk_gte_1994.LMale.sum()
            lr_exps_gte_1994 = ((year_lr_df_gte_1994.LMs + year_lr_df_gte_1994.LMapp + year_lr_df_gte_1994.LMc + year_lr_df_gte_1994.LMale) * year_lr_df_gte_1994.Units).sum()
            cr_exps_total = cr_exps_lt_1970 + cr_exps_lte_1983 + cr_exps_lte_1993 + cr_exps_gte_1994
            lr_exps_total = lr_exps_lt_1970 + lr_exps_lte_1983 + lr_exps_lte_1993 + lr_exps_gte_1994

            change_exps_lt_1970 = (cr_exps_lt_1970 + lr_exps_lt_1970) / (cr_exps_total + lr_exps_total) * 100
            change_exps_lte_1983 = (cr_exps_lte_1983 + lr_exps_lte_1983) / (cr_exps_total + lr_exps_total) * 100
            change_exps_lte_1993 = (cr_exps_lte_1993 + lr_exps_lte_1993) / (cr_exps_total + lr_exps_total) * 100
            change_exps_gte_1994 = (cr_exps_gte_1994 + lr_exps_gte_1994) / (cr_exps_total + lr_exps_total) * 100

            year_exps_d = { year: [1,2,3,4,5],
                            'Year Build':['<1970','1970~1983','1984~1993','>=1994','Total'],
                            'CR Exposure':[cr_exps_lt_1970,cr_exps_lte_1983,cr_exps_lte_1993,cr_exps_gte_1994,cr_exps_total],
                            'LR Exposure':[lr_exps_lt_1970,lr_exps_lte_1983,lr_exps_lte_1993,lr_exps_gte_1994,lr_exps_total],
                            'Total Change':[change_exps_lt_1970,change_exps_lte_1983,change_exps_lte_1993,change_exps_gte_1994,100]}

            year_exps_df = pd.DataFrame(data=year_exps_d,index=[0,1,2,3,4]) 
            yearlist[i] = year_exps_df
            i = i + 1

        percent_cr_exps_lt_1970 = (yearlist[1].iat[0,0] - yearlist[0].iat[0,0]) / yearlist[0].iat[0,0] * 100
        percent_cr_exps_lte_1983 = (yearlist[1].iat[1,0] - yearlist[0].iat[1,0]) / yearlist[0].iat[1,0] * 100
        percent_cr_exps_lte_1993 = (yearlist[1].iat[2,0] - yearlist[0].iat[2,0]) / yearlist[0].iat[2,0] * 100
        percent_cr_exps_gte_1994 = (yearlist[1].iat[3,0] - yearlist[0].iat[3,0]) / yearlist[0].iat[3,0] * 100
        percent_cr_exps_total = (yearlist[1].iat[4,0] - yearlist[0].iat[4,0]) / yearlist[0].iat[4,0] * 100

        percent_lr_exps_lt_1970 = (yearlist[1].iat[0,1] - yearlist[0].iat[0,1]) / yearlist[0].iat[0,1] * 100
        percent_lr_exps_lte_1983 = (yearlist[1].iat[1,1] - yearlist[0].iat[1,1]) / yearlist[0].iat[1,1] * 100
        percent_lr_exps_lte_1993 = (yearlist[1].iat[2,1] - yearlist[0].iat[2,1]) / yearlist[0].iat[2,1] * 100
        percent_lr_exps_gte_1994 = (yearlist[1].iat[3,1] - yearlist[0].iat[3,1]) / yearlist[0].iat[3,1] * 100
        percent_lr_exps_total = (yearlist[1].iat[4,1] - yearlist[0].iat[4,1]) / yearlist[0].iat[4,1] * 100

        percent_change_d = {'CR Percentage Change':[percent_cr_exps_lt_1970,percent_cr_exps_lte_1983,percent_cr_exps_lte_1993,percent_cr_exps_gte_1994,percent_cr_exps_total],
                            'LR Percentage Change':[percent_lr_exps_lt_1970,percent_lr_exps_lte_1983,percent_lr_exps_lte_1993,percent_lr_exps_gte_1994,percent_lr_exps_total]} 

        yearlist[2] = pd.DataFrame(data=percent_change_d,index=[0,1,2,3,4])                     

        return yearlist

    @expose('/showYearbuild/<string:lastyear>/<string:thisyear>')
    @has_access
    def showYearbuild(self, lastyear, thisyear):

    	# number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)

        yeartup = (lastyear, thisyear)
        yearlist = MyView.yearbuild(yeartup)

        lastyear_exps_df = yearlist[0]
        thisyear_exps_df = yearlist[1]
        percent_exps_df = yearlist[2]
        result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)

        return self.render_template('export.html',lyear=lastyear,tyear=thisyear,lsim=2016,tsim=2017,analytype='exportYearbuild',title='Yearbuilt',
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format},columns=[lastyear,'Year Build','CR Exposure','LR Exposure','Total Change']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format,'CR Percentage Change':flt_percent_format,'LR Percentage Change':flt_percent_format},columns=[thisyear,'Year Build','CR Exposure','LR Exposure','Total Change','CR Percentage Change','LR Percentage Change'])])

    @expose('/exportYearbuild/<string:lastyear>/<string:thisyear>/<int:lastsim>/<int:thissim>')
    @has_access
    def exportYearbuild(self, lastyear, thisyear, lastsim, thissim):

        yeartup = (lastyear, thisyear)
        yearlist = MyView.yearbuild(yeartup)

        lastyear_exps_df = yearlist[0]
        thisyear_exps_df = yearlist[1]
        percent_exps_df = yearlist[2]
        result_df = pd.concat([thisyear_exps_df, thisyear_exps_df], axis=1)
        result_df_1 = pd.concat([result_df, percent_exps_df], axis=1)

        resp = make_response(result_df_1.to_csv(index=False,))
        resp.headers["Content-Disposition"] = "attachment; filename=Yearbuilt.csv"
        resp.headers["Content-Type"] = "text/csv"

        return resp

    @staticmethod
    def regionAna(yeartup):

        regionlist = [1,2,3]

        i = 0

        for year in yeartup:
    	    # define path the different year
            year_path = 'app/data/' + year

            #defin year dataframe 
            year_cr_risk = year_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
            year_lr = year_path + '/pr_lr/valid_data.csv'

            year_cr_df_risk = pd.read_csv(year_cr_risk,usecols=['Region','LMs', 'LMapp', 'LMc', 'LMale'])
            year_lr_df = pd.read_csv(year_lr,usecols=['Region','Units', 'LMs', 'LMapp', 'LMc', 'LMale'])  
            
            year_cr_df_risk_Central = year_cr_df_risk[year_cr_df_risk['Region'] == 'Central']
            year_cr_df_risk_Keys = year_cr_df_risk[year_cr_df_risk['Region'] == 'Keys']
            year_cr_df_risk_North = year_cr_df_risk[year_cr_df_risk['Region'] == 'North']
            year_cr_df_risk_South = year_cr_df_risk[year_cr_df_risk['Region'] == 'South']

            year_lr_df_Central = year_lr_df[year_lr_df['Region'] == 'Central']
            year_lr_df_Keys = year_lr_df[year_lr_df['Region'] == 'Keys']
            year_lr_df_North = year_lr_df[year_lr_df['Region'] == 'North']
            year_lr_df_South = year_lr_df[year_lr_df['Region'] == 'South']

            cr_exps_Central = year_cr_df_risk_Central.LMs.sum() + year_cr_df_risk_Central.LMapp.sum() + year_cr_df_risk_Central.LMc.sum() + year_cr_df_risk_Central.LMale.sum()
            lr_exps_Central = ((year_lr_df_Central.LMs + year_lr_df_Central.LMapp + year_lr_df_Central.LMc + year_lr_df_Central.LMale) * year_lr_df_Central.Units).sum()
            cr_exps_Keys = year_cr_df_risk_Keys.LMs.sum() + year_cr_df_risk_Keys.LMapp.sum() + year_cr_df_risk_Keys.LMc.sum() + year_cr_df_risk_Keys.LMale.sum()
            lr_exps_Keys = ((year_lr_df_Keys.LMs + year_lr_df_Keys.LMapp + year_lr_df_Keys.LMc + year_lr_df_Keys.LMale) * year_lr_df_Keys.Units).sum()
            cr_exps_North = year_cr_df_risk_North.LMs.sum() + year_cr_df_risk_North.LMapp.sum() + year_cr_df_risk_North.LMc.sum() + year_cr_df_risk_North.LMale.sum()
            lr_exps_North = ((year_lr_df_North.LMs + year_lr_df_North.LMapp + year_lr_df_North.LMc + year_lr_df_North.LMale) * year_lr_df_North.Units).sum()
            cr_exps_South = year_cr_df_risk_South.LMs.sum() + year_cr_df_risk_South.LMapp.sum() + year_cr_df_risk_South.LMc.sum() + year_cr_df_risk_South.LMale.sum()
            lr_exps_South = ((year_lr_df_South.LMs + year_lr_df_South.LMapp + year_lr_df_South.LMc + year_lr_df_South.LMale) * year_lr_df_South.Units).sum()
            cr_exps_total = cr_exps_Central + cr_exps_Keys + cr_exps_North + cr_exps_South
            lr_exps_total = lr_exps_Central + lr_exps_Keys + lr_exps_North + lr_exps_South

            change_exps_Central = (cr_exps_Central + lr_exps_Central) / (cr_exps_total + lr_exps_total) * 100
            change_exps_Keys = (cr_exps_Keys + lr_exps_Keys) / (cr_exps_total + lr_exps_total) * 100
            change_exps_North = (cr_exps_North + lr_exps_North) / (cr_exps_total + lr_exps_total) * 100
            change_exps_South = (cr_exps_South + lr_exps_South) / (cr_exps_total + lr_exps_total) * 100

            region_exps_d = {year: [1,2,3,4,5],
                            'Region':['Central','Keys','North','South','Total'],
                            'CR Exposure':[cr_exps_Central,cr_exps_Keys,cr_exps_North,cr_exps_South,cr_exps_total],
                            'LR Exposure':[lr_exps_Central,lr_exps_Keys,lr_exps_North,lr_exps_South,lr_exps_total],
                            'Total Change':[change_exps_Central,change_exps_Keys,change_exps_North,change_exps_South,100]}

            region_exps_df = pd.DataFrame(data=region_exps_d,index=[0,1,2,3,4]) 
            regionlist[i] = region_exps_df
            i = i + 1

        percent_cr_exps_Central = (regionlist[1].iat[0,0] - regionlist[0].iat[0,0]) / regionlist[0].iat[0,0] * 100
        percent_cr_exps_Keys = (regionlist[1].iat[1,0] - regionlist[0].iat[1,0]) / regionlist[0].iat[1,0] * 100
        percent_cr_exps_North = (regionlist[1].iat[2,0] - regionlist[0].iat[2,0]) / regionlist[0].iat[2,0] * 100
        percent_cr_exps_South = (regionlist[1].iat[3,0] - regionlist[0].iat[3,0]) / regionlist[0].iat[3,0] * 100
        percent_cr_exps_total = (regionlist[1].iat[4,0] - regionlist[0].iat[4,0]) / regionlist[0].iat[4,0] * 100

        percent_lr_exps_Central = (regionlist[1].iat[0,1] - regionlist[0].iat[0,1]) / regionlist[0].iat[0,1] * 100
        percent_lr_exps_Keys = (regionlist[1].iat[1,1] - regionlist[0].iat[1,1]) / regionlist[0].iat[1,1] * 100
        percent_lr_exps_North = (regionlist[1].iat[2,1] - regionlist[0].iat[2,1]) / regionlist[0].iat[2,1] * 100
        percent_lr_exps_South = (regionlist[1].iat[3,1] - regionlist[0].iat[3,1]) / regionlist[0].iat[3,1] * 100
        percent_lr_exps_total = (regionlist[1].iat[4,1] - regionlist[0].iat[4,1]) / regionlist[0].iat[4,1] * 100

        percent_total_exps_Central = (regionlist[1].iat[0,1] + regionlist[1].iat[0,0]  - regionlist[0].iat[0,1] - regionlist[0].iat[0,0]) / (regionlist[0].iat[0,0] + regionlist[0].iat[0,1]) * 100
        percent_total_exps_Keys = (regionlist[1].iat[1,1] + regionlist[1].iat[1,0] - regionlist[0].iat[1,1] - regionlist[0].iat[1,0]) / (regionlist[0].iat[1,0] + regionlist[0].iat[1,1]) * 100
        percent_total_exps_North = (regionlist[1].iat[2,1] + regionlist[1].iat[2,0] - regionlist[0].iat[2,1] - regionlist[0].iat[2,0]) / (regionlist[0].iat[2,0] + regionlist[0].iat[2,1]) * 100
        percent_total_exps_South = (regionlist[1].iat[3,1] + regionlist[1].iat[3,0] - regionlist[0].iat[3,1] - regionlist[0].iat[3,0]) / (regionlist[0].iat[3,0] + regionlist[0].iat[3,1]) * 100
        percent_total_exps_total = (regionlist[1].iat[4,1] + regionlist[1].iat[4,0] - regionlist[0].iat[4,1] - regionlist[0].iat[4,0]) / (regionlist[0].iat[4,0] + regionlist[0].iat[4,1]) * 100

        percent_change_d = {'CR Percentage Change':[percent_cr_exps_Central,percent_cr_exps_Keys,percent_cr_exps_North,percent_cr_exps_South,percent_cr_exps_total],
                            'LR Percentage Change':[percent_lr_exps_Central,percent_lr_exps_Keys,percent_lr_exps_North,percent_lr_exps_South,percent_lr_exps_total],
                            'Total Percentage Change':[percent_total_exps_Central,percent_total_exps_Keys,percent_total_exps_North,percent_total_exps_South,percent_total_exps_total]} 

        regionlist[2] = pd.DataFrame(data=percent_change_d,index=[0,1,2,3,4]) 

        return  regionlist

    @expose('/showRegion/<string:lastyear>/<string:thisyear>')
    @has_access
    def showRegion(self, lastyear, thisyear):

    	# number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)

        yeartup = (lastyear, thisyear)
        regionlist = MyView.regionAna(yeartup)

        lastyear_exps_df = regionlist[0]
        thisyear_exps_df = regionlist[1]
        percent_exps_df = regionlist[2]
        result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)

        return self.render_template('export.html',lyear=lastyear,tyear=thisyear,lsim=2016,tsim=2017,analytype='exportYearbuild',title='Region',
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format},columns=[lastyear,'Region','CR Exposure','LR Exposure','Total Change']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format,'CR Percentage Change':flt_percent_format,'LR Percentage Change':flt_percent_format,'Total Percentage Change':flt_percent_format},columns=[thisyear,'Region','CR Exposure','LR Exposure','Total Change','CR Percentage Change','LR Percentage Change','Total Percentage Change'])])

    @staticmethod
    def constructionAna(yeartup):

        constructionlist = [1,2,3]

        i = 0

        for year in yeartup:
    	    # define path the different year
            year_path = 'app/data/' + year

            #defin year dataframe 
            #year_cr_risk = year_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
            year_lr = year_path + '/pr_lr/valid_data.csv'

            #year_cr_df_risk = pd.read_csv(year_cr_risk,usecols=['Region','LMs', 'LMapp', 'LMc', 'LMale'])
            year_lr_df = pd.read_csv(year_lr,usecols=['ConstType','Units', 'LMs', 'LMapp', 'LMc', 'LMale'])  
            
            #year_cr_df_risk_Central = year_cr_df_risk[year_cr_df_risk['Region'] == 'Central']
            #year_cr_df_risk_Keys = year_cr_df_risk[year_cr_df_risk['Region'] == 'Keys']
            #year_cr_df_risk_North = year_cr_df_risk[year_cr_df_risk['Region'] == 'North']
            #year_cr_df_risk_South = year_cr_df_risk[year_cr_df_risk['Region'] == 'South']

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

            change_exps_Frame = (0 + lr_exps_Frame) / (0 + lr_exps_total) * 100
            change_exps_Masonry = (0 + lr_exps_Masonry) / (0 + lr_exps_total) * 100
            change_exps_Other = (0 + lr_exps_Other) / (0 + lr_exps_total) * 100

            construction_exps_d = {year: [1,2,3,4],
                            'Construction Type':['Frame','Masonry','Other','Total'],
                            'CR Exposure':[0,0,0,0],
                            'LR Exposure':[lr_exps_Frame,lr_exps_Masonry,lr_exps_Other,lr_exps_total],
                            'Total Change':[change_exps_Frame,change_exps_Masonry,change_exps_Other,100]}

            construction_exps_df = pd.DataFrame(data=construction_exps_d,index=[0,1,2,3],columns=[year,"CR Exposure","LR Exposure","Construction Type","Total Change"]) 
            constructionlist[i] = construction_exps_df
            i = i + 1

        percent_cr_exps_Frame = 0
        percent_cr_exps_Masonry = 0
        percent_cr_exps_Other = 0
        percent_cr_exps_total = 0

        percent_lr_exps_Frame = (constructionlist[1].iat[0,1] - constructionlist[0].iat[0,1]) / constructionlist[0].iat[0,1] * 100
        percent_lr_exps_Masonry = (constructionlist[1].iat[1,1] - constructionlist[0].iat[1,1]) / constructionlist[0].iat[1,1] * 100
        percent_lr_exps_Other = (constructionlist[1].iat[2,1] - constructionlist[0].iat[2,1]) / constructionlist[0].iat[2,1] * 100
        percent_lr_exps_total = (constructionlist[1].iat[3,1] - constructionlist[0].iat[3,1]) / constructionlist[0].iat[3,1] * 100

        percent_change_d = {'CR Percentage Change':[0,0,0,0],
                            'LR Percentage Change':[percent_lr_exps_Frame,percent_lr_exps_Masonry,percent_lr_exps_Other,percent_lr_exps_total]} 

        constructionlist[2] = pd.DataFrame(data=percent_change_d,index=[0,1,2,3]) 

        return  constructionlist

    @expose('/showConstruction/<string:lastyear>/<string:thisyear>')
    @has_access
    def showConstruction(self, lastyear, thisyear):

    	# number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)

        yeartup = (lastyear, thisyear)
        constructionlist = MyView.constructionAna(yeartup)

        lastyear_exps_df = constructionlist[0]
        thisyear_exps_df = constructionlist[1]
        percent_exps_df = constructionlist[2]
        result_df = pd.concat([thisyear_exps_df, percent_exps_df], axis=1)

        return self.render_template('export.html',lyear=lastyear,tyear=thisyear,lsim=2016,tsim=2017,analytype='exportYearbuild',title='Construction Type',
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format},columns=[lastyear,'Construction Type','CR Exposure','LR Exposure','Total Change']),
                                       result_df.to_html(classes='table table-bordered',index=False,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format,'Total Change':flt_percent_format,'CR Percentage Change':flt_percent_format,'LR Percentage Change':flt_percent_format,},columns=[thisyear,'Construction Type','CR Exposure','LR Exposure','Total Change','CR Percentage Change','LR Percentage Change'])])
    

    @staticmethod
    def countyAna(yeartup):

        countylist = [1,2,3]

        i = 0

        for year in yeartup:
    	    # define path the different year
            year_path = 'app/data/' + year

            #defin year dataframe 
            year_cr_risk = year_path + '/cr/CRILM_MidHighRise_AggRiskLosses.txt'
            year_lr = year_path + '/pr_lr/valid_data.csv' 

            year_cr_df_risk = pd.read_csv(year_cr_risk,usecols=['County','LMs', 'LMapp', 'LMc', 'LMale'])
            year_lr_df = pd.read_csv(year_lr,usecols=['County','Units', 'LMs', 'LMapp', 'LMc', 'LMale'])
            year_cr_df_risk.set_index("County",inplace=True)
            year_lr_df.set_index("County",inplace=True)

            year_cr_df_risk_group = year_cr_df_risk.groupby(['County']).agg(['sum'])
            year_cr_df_risk_group['CR Exposure'] = year_cr_df_risk_group[['LMs','LMapp','LMc','LMale']].sum(axis=1)

            year_lr_df_group = year_lr_df.groupby(['County']).agg(['sum'])
            year_lr_df_group['LR Exposure'] = year_lr_df_group[['LMs','LMapp','LMc','LMale']].sum(axis=1)

            df_cr_lr = pd.concat([year_cr_df_risk_group[['CR Exposure']],year_lr_df_group[['LR Exposure']]],axis=1)
            df_cr_lr.fillna(0)

            countylist[i] = df_cr_lr
            i = i + 1

        return countylist

    @expose('/showCounty/<string:lastyear>/<string:thisyear>')
    @has_access
    def showCounty(self, lastyear, thisyear):

    	# number format
        int_num_format = lambda x: '{:,}'.format(x)
        flt_num_format = lambda x: '${:,.2f}'.format(x)
        flt_percent_format = lambda x: '{:,.2f}%'.format(x)

        yeartup = (lastyear, thisyear)
        countylist = MyView.countyAna(yeartup)

        lastyear_exps_df = countylist[0]

        return self.render_template('export.html',lyear=lastyear,tyear=thisyear,lsim=2016,tsim=2017,analytype='exportYearbuild',title='Construction Type',
                               tables=[lastyear_exps_df.to_html(classes='table table-bordered',index=True,formatters={'CR Exposure':flt_num_format,'LR Exposure':flt_num_format},columns=['CR Exposure','LR Exposure'])
                               ])
        

#appbuilder.add_view(MyView(), "Method1", category='My View')
#appbuilder.add_view(MyView(), "Method2", href='/myview/method2/jonh', category='My View')
# Use add link instead there is no need to create MyView twice.
#appbuilder.add_link("Method2", href='/myview/method2/jonh', category='My View')
appbuilder.add_view(MyView(),"comparisons", href='/myview/showComparisons/2016/2017/57000/58000', category='My View')
appbuilder.add_link("yearbuild", href='/myview/showYearbuild/2016/2017', category='My View')
appbuilder.add_link("region", href='/myview/showRegion/2016/2017', category='My View')
appbuilder.add_link("county", href='/myview/showCounty/2016/2017', category='My View')
appbuilder.add_link("construction", href='/myview/showConstruction/2016/2017', category='My View')