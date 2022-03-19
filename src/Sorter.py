class Sorter(object):

    def __init__(self):
        self.records = []


    def sort_by_energy(self):
        self.records = sorted(self.records, key=lambda record: record.energy, reverse=True)

    def sort_by_intensity(self):
        self.records = sorted(self.records, key=lambda record: record.intensity)

    def group_by_energy_and_sort_by_intensity(self, grouping):
        self.sort_by_energy()

    def add_record(self, energy, intensity, rel_intensity, transition):
        record = Record(energy, intensity, rel_intensity, transition)
        self.records.append(record) 

    def __str__(self):
        text = ""
        for record in self.records:
            if record.intensity < 0:
                continue
            text += str(record)
        return text


class Record(object):

    def __init__(self, energy, intensity, rel_intensity, transition):
        self.energy = energy
        self.intensity = intensity
        self.rel_intensity = rel_intensity
        self.transition = transition

    def __str__(self):
        text = "Energy: {}, Intensity: {}, Transition: {}\n".format(self.energy, self.intensity, self.transition)
        return text

