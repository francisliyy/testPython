from flask import render_template, make_response, send_file, request
from flask_appbuilder import BaseView, expose, has_access
from app import appbuilder
from .forms import TOBForm
from io import BytesIO
import pandas as pd
import numpy as np
import logging

log = logging.getLogger(__name__)

class TestView(BaseView):

    @expose('/testEchart/')
    @has_access
    def testEchart(self):
        # do something with param1
        # and return to previous page or index
        param1 = 'hello'
        log.info('================inside')
        return self.render_template('testechart.html',param1=param1)

appbuilder.add_view(TestView(),"testEchart", href='/testview/testEchart/', category='Echart')

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404


    
