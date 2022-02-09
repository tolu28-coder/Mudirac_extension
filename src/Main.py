from IntensityCalculator import IntensityCalculator
from Misc import parse_mudirac_file

path = r"C:\Users\Tolu\Documents\Mudirac data\mudirac_output_file\Gold.out"
Gold = IntensityCalculator("linear", 12, path)
Gold.calculate_intensities()


