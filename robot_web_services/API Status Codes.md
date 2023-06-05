# API Status Codes

- (200) HTTP_OK => Standard response for successful HTTP requests.
- (201) CREATED => The request has been fulfilled, and a new resource is created
- (202) ACCEPTED => The request has been accepted for processing, but the processing has not been completed
- (204) NO_CONTENT => The request has been successfully processed, but is not returning any content
- (301) MOVED_PERMANENTLY => The requested page has moved to a new URL
- (304) NOT_MODIFIED => Indicates the requested page has not been modified since last requested
- (400) BAD_REQUEST => The request cannot be fulfilled due to bad syntax
- (401) UNAUTHORIZED => The request was a legal request, but the server is refusing to respond to it. For use when authentication is possible but has failed or not yet been provided
- (403) FORBIDDEN => The request was a legal request, but the server is refusing to respond to it
- (404) NOT_FOUND => The requested page could not be found but may be available again in the future
- (405) METHOD_NOT_ALLOWED => A request was made of a page using a request method not supported by that page
- (406) NOT_ACCEPTABLE => The server can only generate a response that is not accepted by the client
- (409) CONFLICT => The request could not be completed due to a conflict with the current state of the target resource
- (410) GONE => The requested page is no longer available
- (415) UNSUPPORTED_MEDIA => The server will not accept the request, because the media type is not supported
- (500) INTERNAL_SERVER_ERROR => A generic error message, given when no more specific message is suitable
- (501) NOT_IMPLEMENTED => The server either does not recognize the request method, or it lacks the ability to fulfill the request
- (503) SERVICE_UNAVAILABLE => The server is currently unavailable (overloaded or down)
