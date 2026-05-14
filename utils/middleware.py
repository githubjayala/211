import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class TracingMiddleware(BaseHTTPMiddleware):
    # WHAT: intercepts every request before it hits your routes
    # WHY:  ensures every request has a trace ID regardless of
    #       whether the caller provided one or not

    async def dispatch(self, request: Request, call_next):

        # WHAT: read incoming trace ID or mint a new one
        # WHY:  if gateway already assigned one, preserve it
        #       so the same ID flows through all services
        #       if no ID exists (first entry point), create one
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))

        # WHAT: attach trace ID to request state
        # WHY:  route handlers and loggers can read it via
        #       request.state.trace_id without touching headers
        request.state.trace_id = trace_id

        # process the request
        response = await call_next(request)

        # WHAT: echo trace ID back in response headers
        # WHY:  client can log it for their own debugging
        #       and it confirms the ID that was used
        response.headers["X-Trace-ID"] = trace_id

        return response
