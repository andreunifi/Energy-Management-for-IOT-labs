#include <systemc-ams.h>

#include "config.h"

#define A_Voc -42.77304451
#define B_Voc 147.03333309
#define C_Voc -198.82836987
#define D_Voc 134.07477623
#define E_Voc -46.60518529
#define F_Voc 8.35505624
#define G_Voc 2.8747398

#define module_R 0.00761749 
#define exp_R -1.86746127
#define bias_R 0.00493609

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
