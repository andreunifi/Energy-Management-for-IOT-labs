#include "battery_voc.h"


double battery_voc::getVoc(double soc)
{
    return A_Voc * pow(soc, 6) +
    B_Voc * pow(soc, 5) +
    C_Voc * pow(soc, 4) +
    D_Voc * pow(soc, 3) +
    E_Voc * pow(soc, 2) +
    F_Voc * soc +
    G_Voc;
}

double battery_voc::getR(double soc)
{
    return module_R*pow(soc, exp_R) + bias_R;
}


void battery_voc::set_attributes()
{
    v_oc.set_timestep(SIM_STEP, sc_core::SC_SEC);
    r_s.set_timestep(SIM_STEP, sc_core::SC_SEC);
    soc.set_timestep(SIM_STEP, sc_core::SC_SEC);
    r_s.set_delay(1);
    soc.set_delay(1);
}

void battery_voc::initialize() {}

void battery_voc::processing()
{
    double tmpcurrent; // Battery current, if negative, the battery is charged 
    
    // Read input current
    tmpcurrent = i.read(); // Battery current, if negative, the battery is charged 

    /* 
    Compute actual state-of-charge solving the integral:
    SOC_t = SOC_{t-1} - \int^{t}_{-inf} i(\tau) / C d\tau
    */
    
    tmpsoc -= (((tmpcurrent + prev_i_batt) * SIM_STEP) / (2 * 3600 * c_nom)); // 3600 * Cnom, mAh to mAs cause [sim step] = [s]
    prev_i_batt = tmpcurrent; // Update

    // Each instant the battery self-discharge a bit
    tmpsoc = (1.0 - SELFDISCH_FACTOR) * tmpsoc;

    // Output the battery SOC
    if(tmpsoc >= 1) // Not let the SOC overflow
    {
        soc.write(1);
        tmpsoc = 1;
    }
    else
    {
        soc.write(tmpsoc);
    }

    // SOC and battery Voc relationship
    v_oc.write(getVoc(tmpsoc)); // Place interpolated funct here

    // SOC and battery internal resistance relationship
    r_s.write(getR(tmpsoc)); // Place interpolated funct here

    // When the battery SOC decreases under 1%, the simulation stops.	
    if(tmpsoc <= 0.01)
    {
        cout << "SOC is less than or equal to 1%:" << " @" << sc_time_stamp() << endl;
        sc_stop();
    }
}
