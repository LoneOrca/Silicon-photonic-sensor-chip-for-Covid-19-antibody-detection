import siepic.all as siepic
import ipkiss3.all as i3
from ipkiss.technology import get_technology
from picazzo3.wg.spirals import FixedLengthSpiralRounded
import scipy.constants as con
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from ipkiss3.io.touchstone import import_touchstone_smatrix, export_touchstone_smatrix



TECH = get_technology()

class COV_19_proj_1(i3.Circuit):
    Spacing_y = i3.PositiveNumberProperty(default=250)
    Spacing_x = i3.PositiveNumberProperty(default=10.9)


    def _default_insts(self):
        floorplan_4 = siepic.FloorPlan(size=[2250, 3800])
        ebeamterminatorte1550_1 = siepic.EbeamTerminatorTE1550()
        ebeamy1550_2 = siepic.EbeamY1550()
        waveguide_crossing = siepic.EbeamCrossing()
        spiral = FixedLengthSpiralRounded(name=self.name + "_SPIRAL",
                                          total_length=4000,
                                          n_o_loops=4,
                                          trace_template=siepic.StripWaveguideTemplate())
        layout = spiral.Layout(
            incoupling_length=10.0,
            bend_radius=10.0,
            spacing=6,
            stub_direction="H",  # either H or V
            growth_direction="V",  # either H or V
        )

        return {
            "Chip_Floor": floorplan_4,
            "Output_Ec_Cal": ebeamterminatorte1550_1,
            "MZI_1_EC": ebeamterminatorte1550_1,
            "MZI_2_EC": ebeamterminatorte1550_1,
            "MZI_3_EC": ebeamterminatorte1550_1,
            "Dummy_1": ebeamterminatorte1550_1,
            "Dummy_2": ebeamterminatorte1550_1,
            "Dummy_3": ebeamterminatorte1550_1,
            "Input_EC": ebeamterminatorte1550_1,
            "Dummy_Cal": ebeamy1550_2,
            "YB_1": ebeamy1550_2,
            "YB_2": ebeamy1550_2,
            "YB_3": ebeamy1550_2,
            "YB_2_MZI1": ebeamy1550_2,
            "YB_2_MZI2": ebeamy1550_2,
            "YB_3_MZI3": ebeamy1550_2,
            "CB_MZ_1": ebeamy1550_2,
            "CB_MZ_2": ebeamy1550_2,
            "CB_MZ_3": ebeamy1550_2,
            "WG_Cross_1": waveguide_crossing,
            "WG_Cross_2": waveguide_crossing,
            "WG_Cross_3": waveguide_crossing,
            "WG_Cross_4": waveguide_crossing,
            "WG_Cross_5": waveguide_crossing,
            "Spiral_1": spiral,
            "Spiral_2": spiral,
            "Spiral_3": spiral,
            "Spiral_4": spiral,
            "Spiral_5": spiral,
            "Spiral_6": spiral,


        }
    def _default_specs(self):

         return [

             i3.Place("Chip_Floor",(0,0),angle=0),
             i3.Place("Dummy_3",(40,2*self.Spacing_y),angle=0),
             i3.Place("Dummy_2",(40,3*self.Spacing_y),angle=0),
             i3.Place("Dummy_1", (40,4*self.Spacing_y), angle=0),
             i3.Place("MZI_3_EC", (40,5*self.Spacing_y), angle=0),
             i3.Place("MZI_2_EC", (40,7.6*self.Spacing_y), angle=0),
             i3.Place("MZI_1_EC", (40,8*self.Spacing_y), angle=0),
             i3.Place("Output_Ec_Cal", (40,10*self.Spacing_y),angle=0),
             i3.Place("Input_EC", (40,12*self.Spacing_y), angle=0),
             i3.Place("YB_1", (403,3275),angle=0),
             i3.Place("YB_2", (741.2,3338.9),angle=0),
             i3.Place("YB_3", (510, 3214),angle=0),
             i3.Place("YB_2_MZI1", (1397,3248),angle=270),
             i3.Place("YB_2_MZI2", (1448, 2039), angle=270),
             i3.Place("YB_3_MZI3", (1444.1,704.2), angle=270),
             i3.Place("CB_MZ_1", (1447, 2759), angle=90),
             i3.Place("CB_MZ_2", (1442, 1548), angle=90),
             i3.Place("CB_MZ_3", (1451.3, 168.2), angle=90),
             i3.Place("WG_Cross_1", (702, 2401), angle=0),
             i3.Place("WG_Cross_2", (799, 2399), angle=0),
             i3.Place("WG_Cross_3", (799.4,1449.4), angle=0),
             i3.Place("WG_Cross_4", (502,1123.4), angle=0),
             i3.Place("WG_Cross_5", (801,899), angle=90),
             i3.Place("Spiral_1", (1315, 3135), angle=270),
             i3.Place("Spiral_2", (1913, 3135), angle=270),
             i3.Place("Spiral_3", (1315, 1938), angle=270),
             i3.Place("Spiral_4", (1913, 1934), angle=270),
             i3.Place("Spiral_5", (1315, 487), angle=270),
             i3.Place("Spiral_6", (1916, 487), angle=270),
             i3.Place("Dummy_Cal", (184.2,749.7), angle=90),
             i3.ConnectManhattan("Input_EC:opt1","YB_1:opt1"),
             i3.ConnectManhattan("YB_1:opt2", "YB_2:opt1"),
             i3.ConnectManhattan("YB_1:opt3", "YB_3:opt1"),
             i3.ConnectManhattan("YB_2:opt2", "YB_2_MZI1:opt1",control_points=[i3.H(3400)]),
             i3.ConnectManhattan("YB_2_MZI1:opt3", "Spiral_1:in",control_points=[i3.H(3220)]),
             i3.ConnectManhattan("YB_2_MZI1:opt2", "Spiral_2:in",control_points=[i3.H(3220)]),
             i3.ConnectManhattan("Spiral_1:out", "CB_MZ_1:opt2"),
             i3.ConnectManhattan("Spiral_2:out", "CB_MZ_1:opt3"),
             i3.ConnectManhattan("CB_MZ_1:opt1", "WG_Cross_2:opt4"),
             i3.ConnectManhattan("WG_Cross_2:opt1", "WG_Cross_1:opt4"),
             i3.ConnectManhattan("WG_Cross_1:opt1", "MZI_1_EC:opt1"),
             i3.ConnectManhattan("YB_2:opt3", "WG_Cross_2:opt2"),
             i3.ConnectManhattan("YB_3:opt3", "Output_Ec_Cal:opt1"),
             i3.ConnectManhattan("YB_3:opt2", "WG_Cross_1:opt2"),
             i3.ConnectManhattan("YB_2_MZI2:opt3", "Spiral_3:in",control_points=[i3.H(2020)]),
             i3.ConnectManhattan("YB_2_MZI2:opt2", "Spiral_4:in",control_points=[i3.H(2020)]),
             i3.ConnectManhattan("WG_Cross_2:opt3", "YB_2_MZI2:opt1"),
             i3.ConnectManhattan("Spiral_3:out", "CB_MZ_2:opt2"),
             i3.ConnectManhattan("Spiral_4:out", "CB_MZ_2:opt3"),
             i3.ConnectManhattan("CB_MZ_2:opt1", "WG_Cross_3:opt4"),
             i3.ConnectManhattan("WG_Cross_1:opt3", "WG_Cross_3:opt2"),
             i3.ConnectManhattan("WG_Cross_3:opt3", "WG_Cross_4:opt2"),
             i3.ConnectManhattan("WG_Cross_4:opt3", "WG_Cross_5:opt2"),
             i3.ConnectManhattan("WG_Cross_5:opt3", "YB_3_MZI3:opt1"),
             i3.ConnectManhattan("YB_3_MZI3:opt3", "Spiral_5:in",control_points=[i3.H(690)]),
             i3.ConnectManhattan("YB_3_MZI3:opt2", "Spiral_6:in",control_points=[i3.H(690)]),
             i3.ConnectManhattan("WG_Cross_3:opt1", "MZI_2_EC:opt1"),
             i3.ConnectManhattan("Spiral_5:out", "CB_MZ_3:opt2"),
             i3.ConnectManhattan("Spiral_6:out", "CB_MZ_3:opt3"),
             i3.ConnectManhattan("CB_MZ_3:opt1", "WG_Cross_5:opt1"),
             i3.ConnectManhattan("WG_Cross_5:opt4", "WG_Cross_4:opt4"),
             i3.ConnectManhattan("WG_Cross_4:opt1", "MZI_3_EC:opt1"),
             i3.ConnectManhattan("Dummy_Cal:opt2", "Dummy_1:opt1"),
             i3.ConnectManhattan("Dummy_Cal:opt3", "Dummy_2:opt1"),
             i3.ConnectManhattan("Dummy_Cal:opt1", "Dummy_3:opt1"),



         ]

    def _default_exposed_ports(self):
        return {
            "Input_EC:fib1": "Input",
            "Output_Ec_Cal:fib1": "Output_Cal",
            "MZI_1_EC:fib1": "MZI1",
            "MZI_2_EC:fib1": "MZI2",
            "MZI_3_EC:fib1": "MZI3",
            "Dummy_1:fib1": "Dummy1",
            "Dummy_2:fib1": "Dummy2",
            "Dummy_3:fib1": "Dummy3",
        }


if __name__ == "__main__":
    cell = COV_19_proj_1(name="COV_19_proj_1")
    cell_lo = cell.Layout()
    cell_lo.write_gdsii("COV_19_proj_1.gds")
    cell_lo.visualize(annotate=True)

center_wavelength = i3.Environment(wavelength=1.56)
lambda_0 = 1.55

# MZI Design Calculations

wg_tmpl = siepic.StripWaveguideTemplate()
wg_tmpl.Layout(core_width=0.5)
wg_tmpl_cm = wg_tmpl.CircuitModel()

neff = wg_tmpl_cm.get_n_eff(center_wavelength)
ng = wg_tmpl_cm.get_n_g(center_wavelength)
print("......................")
print("neff @ 1.56 {}".format(neff))
print("ng @ 1.56: {}".format(ng))
print("......................")

nm = con.nano
um = con.micron
Meg = con.mega
pi = con.pi

FSR = np.array([4 * nm, 8 * nm, 9 * nm], float)

Delta_L = np.divide((np.square(lambda_0 * um)), (ng * FSR))

print("......................")
print("Delta L for 3 MZIs Designed")
print(np.round(Delta_L * Meg, 0))
print("......................")

wavelength_sweep = um * np.linspace(1.54, 1.56, 1000)

ko = np.divide((2 * pi), wavelength_sweep)

Beta = ng * ko
MZI_T_Calculated_0 = 10 * np.log10(np.abs(0.5 * (1 + np.cos(Beta * Delta_L[0]))))
MZI_T_Calculated_1 = 10 * np.log10(np.abs(0.5 * (1 + np.cos(Beta * Delta_L[1]))))
MZI_T_Calculated_2 = 10 * np.log10(np.abs(0.5 * (1 + np.cos(Beta * Delta_L[2]))))

peaks_y0, _ = find_peaks(MZI_T_Calculated_0)
peak_x0 = Meg * wavelength_sweep[peaks_y0[0]]
next_peak_x0 = Meg * wavelength_sweep[peaks_y0[1]]
FSR_0 = next_peak_x0 - peak_x0
peaks_y1, _ = find_peaks(MZI_T_Calculated_1)
peak_x1 = Meg * wavelength_sweep[peaks_y1[0]]
next_peak_x1 = Meg * wavelength_sweep[peaks_y1[1]]
FSR_1 = next_peak_x1 - peak_x1
peaks_y2, _ = find_peaks(MZI_T_Calculated_2)
peak_x2 = Meg * wavelength_sweep[peaks_y2[0]]
next_peak_x2 = Meg * wavelength_sweep[peaks_y2[1]]
FSR_2 = next_peak_x2 - peak_x1

fig, ax = plt.subplots(3, sharex="all", figsize=(8, 8))
for axs in ax:
    axs.grid(True)

ax[0].plot(wavelength_sweep * Meg, MZI_T_Calculated_0, color='red')
ax[0].plot(wavelength_sweep[peaks_y0] * Meg, MZI_T_Calculated_0[peaks_y0], "x", markersize=10, color='black')
ax[0].set_ylim([-30, 5])
ax[0].set_title('FSR ={:.2f} nm '.format(FSR_0 * 1000))

ax[1].plot(wavelength_sweep * Meg, MZI_T_Calculated_1, color='blue')
ax[1].plot(wavelength_sweep[peaks_y1] * Meg, MZI_T_Calculated_1[peaks_y1], "x", markersize=10, color='black')
ax[1].set_ylim([-30, 5])
ax[1].set_title('FSR ={:.2f} nm '.format(FSR_1 * 1000))

ax[2].plot(wavelength_sweep * Meg, MZI_T_Calculated_2, color='green')
ax[2].plot(wavelength_sweep[peaks_y2] * Meg, MZI_T_Calculated_2[peaks_y2], "x", markersize=10, color='black')
ax[2].set_ylim([-30, 5])
ax[2].set_title('FSR ={:.2f} nm '.format(FSR_2 * 1000))

ax[2].set_xlabel("wavelength (\u03BCm)", fontsize=16)
fig.text(1014, 105, 'Transmission (dB)', va='center', rotation='vertical', fontsize=16)
fig.suptitle('Calculated MZI Spectrum for each Design', fontsize=16)
plt.savefig('Calculated_MZI_Design_Spectrum.png', dpi=600)
plt.show()

# Generates the circuit model
circuit_Netlist = cell.Netlist()
print(circuit_Netlist)
circuit_model = cell.CircuitModel()

# Get the S-Parameter data for each component and compute the S-Matrix
wavelengths = np.linspace(1.54, 1.56, 1000)
S_total = circuit_model.get_smatrix(wavelengths=wavelengths)
plt.figure(figsize=(10, 6))

# Plotting transmission for different ports as an example
plt.plot(wavelengths, 20*np.log10(np.abs(S_total['MZI1', 'Input'])), label='MZI_1 Transmission',color='red')
plt.xlabel('Wavelength (μm)')
plt.ylabel('Transmission(dB)')
plt.title('S-Parameter Simulation Results')
plt.legend()
plt.grid(True)
plt.show()


wavelengths = np.linspace(1.54, 1.56, 1000)
S_total = circuit_model.get_smatrix(wavelengths=wavelengths)
plt.figure(figsize=(10, 6))

plt.plot(wavelengths, 20*np.log10(np.abs(S_total['MZI2', 'Input'])), label='MZI_2 Transmission', color='blue')

plt.xlabel('Wavelength (μm)')
plt.ylabel('Transmission(dB)')
plt.title('S-Parameter Simulation Results')
plt.legend()
plt.grid(True)
plt.show()




wavelengths = np.linspace(1.54, 1.56, 1000)
S_total = circuit_model.get_smatrix(wavelengths=wavelengths)
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, 20*np.log10(np.abs(S_total['MZI3', 'Input'])), label='MZI_3 Transmission',color='green')

plt.xlabel('Wavelength (μm)')
plt.ylabel('Transmission(dB)')
plt.title('S-Parameter Simulation Results')
plt.legend()
plt.grid(True)
plt.show()


