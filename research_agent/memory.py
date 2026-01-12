class ResearchMemory:
    def __init__(self):
        self.notes = []
        self.sources = []

    def add(self, claim, source):
        self.notes.append(claim)
        self.sources.append(source)

    def summary(self):
        out = []
        for note, src in zip(self.notes, self.sources):
            out.append(f"- {note}\n  Source: {src}")
        return "\n".join(out)
