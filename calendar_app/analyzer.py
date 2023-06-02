from klym_telemetry.utils import instrument, klym_telemetry
from opentelemetry import trace

from calendar_app.models import Event
from calendar_app.tasks import AsyncEvent


@instrument()
class EventAnalyzer:

    def __init__(self, event: Event):
        span = trace.get_current_span().get_span_context()
        self.run_async_event(event=event, span=span)

    def run_async_event(self, event, span):
        AsyncEvent().delay(event_id=event.id, span_id=span.span_id, trace_id=span.trace_id)
        klym_telemetry.add_event_curr_span('Validation started')
