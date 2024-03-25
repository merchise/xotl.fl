import os
from hypothesis import settings, Verbosity

settings.register_profile("ci", max_examples=250, deadline=None)
settings.register_profile("dev", max_examples=10)
settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)
settings.register_profile("serious", max_examples=500, deadline=None)
settings.register_profile("killer", max_examples=1000, deadline=None)

settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "ci"))
