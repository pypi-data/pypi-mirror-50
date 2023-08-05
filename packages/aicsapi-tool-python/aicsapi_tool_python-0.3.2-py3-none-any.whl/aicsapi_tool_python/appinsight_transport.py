from applicationinsights import TelemetryClient
from applicationinsights.flask.ext import AppInsights
from threading import Lock

class AppinsightLogger(object):
    '''
    Used for logging to Azure AppInsights
    
    To create an instance:
        appinsights = AppinsightLogger(<Flask app>, <your Azure AppInsights instrumentation key>)
    '''

    def __init__(self, app, appins_key):
        '''
        Creates AppInsightLogger instance

        Parameters
        ----------
        app : obj
            Flask instance
        appins_key : str
            Instrumentation key for Azure AppInsights subscription

        Returns
        -------
        obj
            AppInsightLogger instance
        '''

        # for customEvent logging
        self.tc = TelemetryClient( appins_key )
        self.tc.channel.sender.send_interval_in_milliseconds = 10 * 1000
        self.tc.channel.queue.max_queue_length = 10
        
        # automatically logs request, traces, and failures 
        self.appinsights = AppInsights(app)


        # lock to ensure correlation id is not altered by another request
        self.lock = Lock()

    def send_custEvent(self, cor_id, name, dim=None, measure=None):
        '''
        Logs to customEvent on Azure AppInsights, with correlation ID in context

        Parameters
        ----------
        cor_id : str
            correlation ID of the request
        name : str
            name of customEvent
        dim : dict
            customDimensions of customEvent
        measure : dict
            customMeasurements of customEvent
        '''
        
        self.lock.acquire()
        self.tc.context.operation.id = cor_id
        
        if dim and measure:
            self.tc.track_event(name, dim, measure)
        elif dim and not measure:
            self.tc.track_event(name, dim)
        elif not dim and measure:
            self.tc.track_event(name, None, measure)
        else:
            self.tc.track_event(name)

        self.lock.release()
