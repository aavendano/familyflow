from vibeblocks.core.outcome import Outcome
import dataclasses

print([f.name for f in dataclasses.fields(Outcome)])
