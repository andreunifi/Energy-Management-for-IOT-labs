#define TRACE_PERIOD 900
#define SIZE_PV 4 

#define I250  13.1992
#define I500  28.3300
#define I750  41.8511
#define I1000 54.8893

#define V250  3.0020
#define V500  3.0020
#define V750  3.1390
#define V1000 3.2860

static const double G[SIZE_PV] = {250, 500, 750, 100};
static const double I_MPP[SIZE_PV] = {I250, I500, I750, I1000};
static const double V_MPP[SIZE_PV] = {V250, V500, V750, V1000};
