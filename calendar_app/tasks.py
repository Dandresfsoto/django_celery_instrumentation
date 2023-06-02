import random
import time

import requests
from celery import Task
from klym_telemetry.utils import instrument, klym_telemetry
from opentelemetry import trace
from opentelemetry.trace import SpanContext, TraceFlags, NonRecordingSpan

from calendar_app.models import Event
from core.celery import app


@instrument()
class AsyncEvent(Task):
    name = "event_calendar_task"

    def wait_a_time(self):
        time.sleep(random.randint(5, 10))

    def request_to_api_addresses(self):
        response = requests.get(url="https://random-data-api.com/api/v2/addresses")
        addresses = response.json()
        return addresses

    @staticmethod
    def update_validation(event_id, addresses):
        event_instance = Event.objects.get(id=event_id)
        event_instance.addresses = addresses
        event_instance.is_valid = random.choices([True, False])[0]
        event_instance.save()

    def run(self, event_id, span_id=None, trace_id=None):
        klym_telemetry.up(name="WORKER_RUN_COUNTER", description="A counter of enrichment Event")
        context = None
        if span_id and trace_id:
            parent_span_context = SpanContext(
                span_id=span_id, trace_id=trace_id, is_remote=True, trace_flags=TraceFlags(0x01)
            )
            context = trace.set_span_in_context(NonRecordingSpan(parent_span_context))
        with klym_telemetry.new_curr_span(self.name, context=context):
            self.wait_a_time()
            addresses = self.request_to_api_addresses()
            self.update_validation(event_id=event_id, addresses=addresses)
            klym_telemetry.add_event_curr_span('Validation finished')
            return {"addresses": addresses}


app.tasks.register(AsyncEvent())
