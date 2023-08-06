from semver import max_satisfying

print(max_satisfying(["1.0.0"], b"1.0.0"))
# semver.InvalidTypeIncluded: must be str, but b'1.0.0'
