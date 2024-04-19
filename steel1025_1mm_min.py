import numpy as np
import matplotlib.pyplot as plt

def calculate_engineering_stress_strain(force, displacement, area, gauge_length):
    engineering_stress = force / area
    engineering_strain = displacement / gauge_length
    return engineering_stress, engineering_strain

def calculate_true_stress_strain(force, displacement, area, gauge_length):
    engineering_stress, engineering_strain = calculate_engineering_stress_strain(force, displacement, area, gauge_length)
    true_stress = engineering_stress * (1 + engineering_strain)
    true_strain = np.log(1 + engineering_strain)    
    return true_stress, true_strain


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def calculate_toughness(force, displacement, area, gauge_length):
    stress = force / area
    strain = displacement / gauge_length
    toughness = np.trapz(stress, strain)
    return toughness

file_path = "C:/Users/borga/OneDrive/Desktop/malzeme lablar/lab2/steel1025_1mm_min.TRA"
data = np.loadtxt(file_path, delimiter=",") 

force = data[:, 0]
displacement = data[:, 1]

area = 50.26548  
gauge_length = 30

engineering_stress, engineering_strain = calculate_engineering_stress_strain(force, displacement, area, gauge_length)

true_stress, true_strain = calculate_true_stress_strain(force, displacement, area, gauge_length)

yield_strength_eng = np.max(engineering_stress[:find_nearest(engineering_strain, 0.002)])
ultimate_strength_eng = np.max(engineering_stress)
fracture_strength_eng = np.max(true_stress)

yield_strength_true = np.max(true_stress[:find_nearest(true_strain, 0.002)])
ultimate_strength_true = np.max(true_stress)
fracture_strength_true = np.max(true_stress)

plt.figure(figsize=(10, 5), dpi=80)
plt.plot(engineering_strain, engineering_stress, marker='o', linestyle='-', label='Engineering Stress-Strain', markersize=0.3)
plt.plot(true_strain, true_stress, marker='s', linestyle='-', label='True Stress-Strain', markersize=0.3)
plt.xlabel('Strain (mm/mm)')
plt.ylabel('Stress (MPa)')
plt.title('steel1025_1mm_min')
plt.grid(True)

yield_strength_eng = 550
fracture_strength_eng = 573
fracture_strength_true = 622
modulus_of_elasticity = yield_strength_eng/0.0024
elongation_after_fracture = (np.max(engineering_strain)-(fracture_strength_eng/modulus_of_elasticity))
final_area = area * (1 - np.max(engineering_strain))
reduction_in_area = (area - final_area)/area
toughness = calculate_toughness(force, displacement, area, gauge_length)

print("yield_strength_eng=", yield_strength_eng)
print("ultimate_strength_eng=", int(ultimate_strength_eng))
print("ultimate_strength_true=", int(ultimate_strength_true))
print("fracture_strength_eng=", fracture_strength_eng)
print("fracture_strength_true=", fracture_strength_true)
print("modulus_of_elasticity=", int(modulus_of_elasticity/100)/10)
print("elongation_after_fracture= %", int(elongation_after_fracture*10000)/100)
print("reduction_in_area= %", int(reduction_in_area*10000)/100)
print("toughness=", int(toughness*100)/100)

plt.scatter(0.0024, yield_strength_eng, color='red', label='Yield Strength 550Mpa', zorder=5)
plt.scatter(0.0445, ultimate_strength_eng, color='green', label='Ultimate Tensile Strength (Engineering) 603MPa', zorder=5)
plt.scatter(np.max(engineering_strain), fracture_strength_eng, color='blue', label='Fracture Strength (Engineering) 573MPa', zorder=5)


plt.scatter(0.059, ultimate_strength_true, color='purple', label='Ultimate Tensile Strength (True) 635MPa', zorder=5)
plt.scatter(np.max(true_strain), fracture_strength_true, color='cyan', label='Fracture Strength (True) 622MPa', zorder=5)

plt.legend()
plt.show()
