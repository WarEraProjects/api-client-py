try:
    for a, b in enumerate(zip(None, [1, 2], strict=True)):
        pass
except Exception as e:
    print(repr(e))
