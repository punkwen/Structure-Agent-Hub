import sys
print("line_buffering", sys.stdout.line_buffering, "write_through", getattr(sys.stdout, "write_through", None), "isatty", sys.stdout.isatty(), "encoding", sys.stdout.encoding)
