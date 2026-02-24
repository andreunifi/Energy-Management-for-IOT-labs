#include <systemc-ams.h>

#include "config.h"

#define A_Voc 2.459294
#define B_Voc -3.8721552
#define C_Voc 2.548287
#define D_Voc 3.066423

#define module_R 0.000076
#define exp_R -1.867435
#define bias_R 0.000049

SCA_TDF_MODULE(battery_voc)
{
    sca_tdf::sca_in<double> i; // Battery current
    sca_tdf::sca_out<double> v_oc; // Voltage open-circuit
    sca_tdf::sca_out<double> r_s; // Series resistance
    sca_tdf::sca_out<double> soc; // State of Charge

    SCA_CTOR(battery_voc): v_oc("v_oc"),
                           r_s("r_s"),
                           soc("soc"),
                           tmpsoc(SOC_INIT),
                           prev_i_batt(0) {}

    void set_attributes();
    void initialize();
    void processing();
    double getVoc(double soc);
    double getR(double soc);
    private:
        double c_nom = 3350; //mAH, va portato in in mAs; // Battery nominal capacity, mAh
        double tmpsoc;
        double prev_i_batt;
};
