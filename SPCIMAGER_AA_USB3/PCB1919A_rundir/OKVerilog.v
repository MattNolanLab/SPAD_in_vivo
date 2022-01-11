// Auto generated Opal Kelly Verilog


module OK_Top (
input clk_1M, // 1MHz DAC Clock
input SYS_CLK1, // System Clock 1
input SYS_CLK2, // System Clock 2
input  [4:0]  okUH,
output [2:0]  okHU,
inout  [31:0] okUHU,
inout         okAA,
output        okClk, // 100.8MHz USB Clock
input   wire [1:0] button,
output  wire [7:0] led,

output         i2c_sda,
output         i2c_scl,
output  DAC_CLK,

output  DAC_DIN,

output  DAC_NCS,

output  DAC_SET,


// Endpoint connections:

input ADC_PU,
output [7:0] Mode,
input [7:0] FSMState,
output [6:0] SPCIMAGER_SPI_BINA_DELAYGEN_POS1,
output [6:0] SPCIMAGER_SPI_BINA_DELAYGEN_POS2,
output [3:0] SPCIMAGER_SPI_BINA_DELAYGEN_DAC,
output SPCIMAGER_SPI_BINA_DELAYGEN_LT_SEL,
output SPCIMAGER_SPI_BINA_DELAYGEN_OFFSET_SEL,
output [6:0] SPCIMAGER_SPI_BINB_DELAYGEN_POS1,
output [6:0] SPCIMAGER_SPI_BINB_DELAYGEN_POS2,
output [3:0] SPCIMAGER_SPI_BINB_DELAYGEN_DAC,
output SPCIMAGER_SPI_BINB_DELAYGEN_LT_SEL,
output SPCIMAGER_SPI_BINB_DELAYGEN_OFFSET_SEL,
output SPCIMAGER_SPI_BINA_OUT_ENABLE,
output SPCIMAGER_SPI_BINB_OUT_ENABLE,
output SPCIMAGER_SPI_BINA_INPUTSEL,
output SPCIMAGER_SPI_BINB_INPUTSEL,
output [7:0] ROI_FIRST_ROW,
output [7:0] ROI_LAST_ROW,
output [8:0] ROI_FIRST_COL,
output [8:0] ROI_LAST_COL,
output EXPOSURE_START_TRIGGER,
output RST_CTRL_SR,
output PROG_CTRL_SR,
input PROG_COMPLETE,
input [15:0] ADC_FIFO_OUT,
output ADC_FIFO_OUT_rd,
input ADC_FIFO_OUT_ready,
output ADC_FIFO_OUT_blockstrobe,
output ADC_FIFO_RST,
output SPCIMAGER_CHIP_RESET,
output [15:0] EXPOSURE_TIME_LSB,
output [15:0] EXPOSURE_TIME_MSB,
output [4:0] EXPOSURE_MODE,
input [15:0] EXPOSURE_TIME_LSB_RET,
input [15:0] EXPOSURE_TIME_MSB_RET,
input [15:0] FIFO_WR_COUNT,
input [15:0] FIFO_WR_LIMIT,
output DEBUG_PULSERESET,
output CDSBLK_DISABLE,
output CDSSIG_DISABLE,
output CDS_CROWBAR_DISABLE,
output [31:0] NO_OF_EXPOSURES,
output DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE,
input [15:0] FIRMWARE_REVISION,
output DIGITAL_READOUT_PIXEL_BIT,
output [7:0] ROLLING_RESET_CYCLES,
output [15:0] GLOBAL_RESET_CYCLES,
output [7:0] COLUMN_CYCLES_CROWBAR,
output [7:0] ADC_SIGNALS_START,
output [7:0] ADC_CROWBAR_SAMPLE_START,
output [7:0] CDS_BLK_AND_SIG_CYCLES,
output SPCIMAGER_AA_TRUE_FALSE,
input [31:0] SINGLE_BIT_FIFO_OUT,
output SINGLE_BIT_FIFO_OUT_rd,
input SINGLE_BIT_FIFO_OUT_ready,
output SINGLE_BIT_FIFO_OUT_blockstrobe,
output DIGITAL_TOF_AMBIENT_REJECTION_ENABLE,
output  DAC_RST


);


// Target interface bus:
wire [112:0] okHE;
wire [64:0] okEH;
reg reset0; // System RESETN
reg reset1; // System RESETN
reg reset2; // System RESETN
wire dac_set_in;
wire dac_rst_in;
wire dac_set_ret;
wire dac_rst_ret;
wire [11:0] VHV_DATA;
wire [11:0] VHV2_DATA;
wire [11:0] DAC1_A_DATA;
wire [11:0] DAC1_B_DATA;
wire [11:0] DAC2_A_DATA;
wire [11:0] DAC2_B_DATA;
wire [11:0] V1_SET_DATA;
wire [11:0] V2_SET_DATA;
wire [11:0] V3_SET_DATA;
wire [11:0] DAC4_B_DATA;
wire [11:0] VEB_SET_DATA;
wire [11:0] VDD_RAMP_SET_DATA;
wire [11:0] VDDE_SET_DATA;
wire [11:0] AVDD_SET_DATA;
wire [11:0] V3V3_SET_DATA;
wire [11:0] V1V2_SET_DATA;
wire [11:0] V3V6_SET_DATA;
wire [11:0] DAC_SPARE_DATA;

wire [11:0] VHV_ret;
wire [11:0] VHV2_ret;
wire [11:0] DAC1_A_ret;
wire [11:0] DAC1_B_ret;
wire [11:0] DAC2_A_ret;
wire [11:0] DAC2_B_ret;

wire [11:0] V1_SET_ret;
wire [11:0] V2_SET_ret;
wire [11:0] V3_SET_ret;
wire [11:0] DAC4_B_ret;
wire [11:0] VEB_SET_ret;
wire [11:0] VDD_RAMP_SET_ret;
wire [11:0] VDDE_SET_ret;
wire [11:0] AVDD_SET_ret;
wire [11:0] V3V3_SET_ret;
wire [11:0] V1V2_SET_ret;
wire [11:0] V3V6_SET_ret;
wire [11:0] DAC_SPARE_ret;

wire [11:0]   VHV;
wire [11:0]   VHV2;
wire [11:0]   VS;
wire [11:0]   VG;
wire [11:0]   VQ;
wire [11:0]   VREF;
wire [11:0]   V3V3;
wire [11:0]   V2V7;
wire [11:0]   IBIAS1;
wire [11:0]   IBIAS2;
wire [11:0]   V3V6;
wire [11:0]   VDDOPAMP;
wire [11:0]   VDDE;
wire [11:0]   V5_SET;
wire [11:0]   ADCPWR;
wire [11:0]   V1V2;
wire [11:0]   DAC5;
wire [11:0]   DAC6;
wire [1:0]   ProgResetDAC;
wire [1:0]   ProgResetDAC_Ret;
assign DAC_SET = dac_set_ret;
assign DAC_RST = dac_rst_ret;
assign i2c_sda = 1'bz;
assign i2c_scl = 1'bz;
wire [7:0] OK_LEDs;
assign led = ~OK_LEDs;
wire [65*9-1:0]  okEHx;

okWireOR # (.N(9)) wireOR (okEH, okEHx);

okHost okHI(
.okUH(okUH), .okHU(okHU), .okUHU(okUHU), .okAA(okAA),.okClk(okClk),.okHE(okHE), .okEH(okEH)
);

wire [31:0] epwire_00;
wire [31:0] epwire_01;
wire [31:0] epwire_02;
wire [31:0] epwire_03;
wire [31:0] epwire_04;
wire [31:0] epwire_05;
wire [31:0] epwire_06;
wire [31:0] epwire_07;
wire [31:0] epwire_08;
wire [31:0] epwire_09;
wire [31:0] epwire_0a;
wire [31:0] epwire_0b;
wire [31:0] epwire_0c;
wire [31:0] epwire_0d;
wire [31:0] epwire_0e;
wire [31:0] epwire_0f;
wire [31:0] epwire_10;
wire [31:0] epwire_11;
wire [31:0] epwire_12;
wire [31:0] epwire_40;
wire [31:0] epwire_20;
wire [31:0] epwire_13;
wire [31:0] epwire_14;
wire [31:0] epwire_15;
wire [31:0] epwire_16;
wire [31:0] epwire_17;
wire [31:0] epwire_18;
wire [31:0] epwire_44;
wire [31:0] epwire_41;
wire [31:0] epwire_42;
wire [31:0] epwire_60;
wire [31:0] epwire_A2;
wire [31:0] epwire_43;
wire [31:0] epwire_1A;
wire [31:0] epwire_1B;
wire [31:0] epwire_24;
wire [31:0] epwire_25;
wire [31:0] epwire_22;
wire [31:0] epwire_23;
wire [31:0] epwire_45;
wire [31:0] epwire_19;
wire [31:0] epwire_3f;
wire [31:0] epwire_1c;
wire [31:0] epwire_1d;
wire [31:0] epwire_1e;
wire [31:0] epwire_1f;
wire [31:0] epwire_A3;
assign OK_LEDs = epwire_00[7:0];
assign VHV = epwire_01[11:0];
assign VHV2 = epwire_02[11:0];
assign VS = epwire_03[11:0];
assign VG = epwire_04[11:0];
assign VQ = epwire_05[11:0];
assign VREF = epwire_06[11:0];
assign V3V3 = epwire_07[11:0];
assign V2V7 = epwire_08[11:0];
assign IBIAS1 = epwire_09[11:0];
assign IBIAS2 = epwire_0a[11:0];
assign V3V6 = epwire_0b[11:0];
assign VDDOPAMP = epwire_0c[11:0];
assign VDDE = epwire_0d[11:0];
assign V5_SET = epwire_0e[11:0];
assign ADCPWR = epwire_0f[11:0];
assign V1V2 = epwire_10[11:0];
assign DAC5 = epwire_11[11:0];
assign DAC6 = epwire_12[11:0];
assign ProgResetDAC = epwire_40[1:0];
assign epwire_20[3:2] = ProgResetDAC_Ret;
assign epwire_20[4:4] = ADC_PU;
assign Mode = epwire_00[15:8];
assign epwire_20[12:5] = FSMState;
assign SPCIMAGER_SPI_BINA_DELAYGEN_POS1 = epwire_13[6:0];
assign SPCIMAGER_SPI_BINA_DELAYGEN_POS2 = epwire_13[13:7];
assign SPCIMAGER_SPI_BINA_DELAYGEN_DAC = epwire_14[3:0];
assign SPCIMAGER_SPI_BINA_DELAYGEN_LT_SEL = epwire_13[14:14];
assign SPCIMAGER_SPI_BINA_DELAYGEN_OFFSET_SEL = epwire_13[15:15];
assign SPCIMAGER_SPI_BINB_DELAYGEN_POS1 = epwire_15[6:0];
assign SPCIMAGER_SPI_BINB_DELAYGEN_POS2 = epwire_15[13:7];
assign SPCIMAGER_SPI_BINB_DELAYGEN_DAC = epwire_14[7:4];
assign SPCIMAGER_SPI_BINB_DELAYGEN_LT_SEL = epwire_15[14:14];
assign SPCIMAGER_SPI_BINB_DELAYGEN_OFFSET_SEL = epwire_15[15:15];
assign SPCIMAGER_SPI_BINA_OUT_ENABLE = epwire_14[8:8];
assign SPCIMAGER_SPI_BINB_OUT_ENABLE = epwire_14[9:9];
assign SPCIMAGER_SPI_BINA_INPUTSEL = epwire_14[10:10];
assign SPCIMAGER_SPI_BINB_INPUTSEL = epwire_14[11:11];
assign ROI_FIRST_ROW = epwire_16[7:0];
assign ROI_LAST_ROW = epwire_16[15:8];
assign ROI_FIRST_COL = epwire_17[8:0];
assign ROI_LAST_COL = epwire_18[8:0];
assign EXPOSURE_START_TRIGGER = epwire_44[0:0];
assign RST_CTRL_SR = epwire_41[0:0];
assign PROG_CTRL_SR = epwire_42[0:0];
assign epwire_60[0:0] = PROG_COMPLETE;
assign epwire_A2[15:0] = ADC_FIFO_OUT;
assign ADC_FIFO_RST = epwire_43[0:0];
assign SPCIMAGER_CHIP_RESET = epwire_14[12:12];
assign EXPOSURE_TIME_LSB = epwire_1A[15:0];
assign EXPOSURE_TIME_MSB = epwire_1B[15:0];
assign EXPOSURE_MODE = epwire_17[14:10];
assign epwire_24[15:0] = EXPOSURE_TIME_LSB_RET;
assign epwire_25[15:0] = EXPOSURE_TIME_MSB_RET;
assign epwire_22[15:0] = FIFO_WR_COUNT;
assign epwire_23[15:0] = FIFO_WR_LIMIT;
assign DEBUG_PULSERESET = epwire_45[0:0];
assign CDSBLK_DISABLE = epwire_14[13:13];
assign CDSSIG_DISABLE = epwire_14[14:14];
assign CDS_CROWBAR_DISABLE = epwire_14[15:15];
assign NO_OF_EXPOSURES = epwire_19[31:0];
assign DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE = epwire_18[11:11];
assign epwire_3f[15:0] = FIRMWARE_REVISION;
assign DIGITAL_READOUT_PIXEL_BIT = epwire_18[10:10];
assign ROLLING_RESET_CYCLES = epwire_1c[7:0];
assign GLOBAL_RESET_CYCLES = epwire_1d[15:0];
assign COLUMN_CYCLES_CROWBAR = epwire_1e[7:0];
assign ADC_SIGNALS_START = epwire_1e[15:8];
assign ADC_CROWBAR_SAMPLE_START = epwire_1f[7:0];
assign CDS_BLK_AND_SIG_CYCLES = epwire_1f[15:8];
assign SPCIMAGER_AA_TRUE_FALSE = epwire_01[15:15];
assign epwire_A3[31:0] = SINGLE_BIT_FIFO_OUT;
assign DIGITAL_TOF_AMBIENT_REJECTION_ENABLE = epwire_01[14:14];
assign VHV_DATA = (VHV >= 2500) ? 12'd2500 : VHV;
assign VHV2_DATA = (VHV2 >= 2500) ? 12'd2500 : VHV2;
assign DAC1_A_DATA = (VS >= 3300) ? 12'd3300 : VS;
assign DAC1_B_DATA = (VG >= 3650) ? 12'd3650 : VG;
assign DAC2_A_DATA = (VQ >= 3300) ? 12'd3300 : VQ;
assign DAC2_B_DATA = (VREF >= 3300) ? 12'd3300 : VREF;
assign V1_SET_DATA = (V3V3 >= 3650) ? 12'd3650 : V3V3;
assign V2_SET_DATA = (V2V7 >= 3650) ? 12'd3650 : V2V7;
assign V3_SET_DATA = (IBIAS1 >= 3300) ? 12'd3300 : IBIAS1;
assign DAC4_B_DATA = (IBIAS2 >= 3300) ? 12'd3300 : IBIAS2;
assign VEB_SET_DATA = (V3V6 >= 3650) ? 12'd3650 : V3V6;
assign VDD_RAMP_SET_DATA = (VDDOPAMP >= 3650) ? 12'd3650 : VDDOPAMP;
assign VDDE_SET_DATA = (VDDE >= 3300) ? 12'd3300 : VDDE;
assign AVDD_SET_DATA = (V5_SET >= 3300) ? 12'd3300 : V5_SET;
assign V3V3_SET_DATA = (ADCPWR >= 3300) ? 12'd3300 : ADCPWR;
assign V1V2_SET_DATA = (V1V2 >= 1250) ? 12'd1250 : V1V2;
assign V3V6_SET_DATA = (DAC5 >= 3300) ? 12'd3300 : DAC5;
assign DAC_SPARE_DATA = (DAC6 >= 3300) ? 12'd3300 : DAC6;
assign dac_set_in = ProgResetDAC[0];
assign dac_rst_in = ProgResetDAC[1];
assign ProgResetDAC_Ret[0]= dac_set_ret;
assign ProgResetDAC_Ret[1]= dac_rst_ret;



DAC_control PCB_DAC_control_0 ( // System inputs
          .sys_clk(clk_1M), 

          .reset(dac_rst_in),
          // Input to latch in current endpoint values
          .set(dac_set_in),
          // Regbank direct V inputs
          .DAC_VHV(VHV_DATA),
          .DAC_VHV2(VHV2_DATA),
          .DAC1_A(DAC1_A_DATA),
          .DAC1_B(DAC1_B_DATA),
          .DAC2_A(DAC2_A_DATA),
          .DAC2_B(DAC2_B_DATA),
          .V1_SET(V1_SET_DATA),
          .V2_SET(V2_SET_DATA),
          .V3_SET(V3_SET_DATA),
          .DAC4_B(DAC4_B_DATA),
          .VEB_SET(VEB_SET_DATA),
          .VDD_RAMP_SET(VDD_RAMP_SET_DATA),
          .VDDE_SET(VDDE_SET_DATA),
          .AVDD_SET(AVDD_SET_DATA),
          .V3V3_SET(V3V3_SET_DATA),
          .V1V2_SET(V1V2_SET_DATA),
          .V3V6_SET(V3V6_SET_DATA),
          .DAC_SPARE(DAC_SPARE_DATA),
          // DAC control outputs
          .DAC_CLK(DAC_CLK),
          .DAC_DIN(DAC_DIN),
          .DAC_NCS(DAC_NCS),
          .DAC_VHV_out(VHV_ret),
          .DAC_VHV2_out(VHV2_ret),
          .DAC1_A_out(DAC1_A_ret),
          .DAC1_B_out(DAC1_B_ret),
          .DAC2_A_out(DAC2_A_ret),
          .DAC2_B_out(DAC2_B_ret),
          .V1_SET_out(V1_SET_ret),
          .V2_SET_out(V2_SET_ret),
          .V3_SET_out(V3_SET_ret),
          .DAC4_B_out(DAC4_B_ret),
          .VEB_SET_out(VEB_SET_ret),
          .VDD_RAMP_SET_out(VDD_RAMP_SET_ret),
          .VDDE_SET_out(VDDE_SET_ret),
          .AVDD_SET_out(AVDD_SET_ret),
          .V3V3_SET_out(V3V3_SET_ret),
          .V1V2_SET_out(V1V2_SET_ret),
          .V3V6_SET_out(V3V6_SET_ret),
          .DAC_SPARE_out(DAC_SPARE_ret),
          .dac_set(dac_set_ret),
          .dac_rst(dac_rst_ret)
);


okWireIn   wi_OK_LEDs (.okHE(okHE), .ep_addr(8'h00), .ep_dataout(epwire_00));
okWireIn   wi_VHV (.okHE(okHE), .ep_addr(8'h01), .ep_dataout(epwire_01));
okWireIn   wi_VHV2 (.okHE(okHE), .ep_addr(8'h02), .ep_dataout(epwire_02));
okWireIn   wi_VS (.okHE(okHE), .ep_addr(8'h03), .ep_dataout(epwire_03));
okWireIn   wi_VG (.okHE(okHE), .ep_addr(8'h04), .ep_dataout(epwire_04));
okWireIn   wi_VQ (.okHE(okHE), .ep_addr(8'h05), .ep_dataout(epwire_05));
okWireIn   wi_VREF (.okHE(okHE), .ep_addr(8'h06), .ep_dataout(epwire_06));
okWireIn   wi_V3V3 (.okHE(okHE), .ep_addr(8'h07), .ep_dataout(epwire_07));
okWireIn   wi_V2V7 (.okHE(okHE), .ep_addr(8'h08), .ep_dataout(epwire_08));
okWireIn   wi_IBIAS1 (.okHE(okHE), .ep_addr(8'h09), .ep_dataout(epwire_09));
okWireIn   wi_IBIAS2 (.okHE(okHE), .ep_addr(8'h0a), .ep_dataout(epwire_0a));
okWireIn   wi_V3V6 (.okHE(okHE), .ep_addr(8'h0b), .ep_dataout(epwire_0b));
okWireIn   wi_VDDOPAMP (.okHE(okHE), .ep_addr(8'h0c), .ep_dataout(epwire_0c));
okWireIn   wi_VDDE (.okHE(okHE), .ep_addr(8'h0d), .ep_dataout(epwire_0d));
okWireIn   wi_V5_SET (.okHE(okHE), .ep_addr(8'h0e), .ep_dataout(epwire_0e));
okWireIn   wi_ADCPWR (.okHE(okHE), .ep_addr(8'h0f), .ep_dataout(epwire_0f));
okWireIn   wi_V1V2 (.okHE(okHE), .ep_addr(8'h10), .ep_dataout(epwire_10));
okWireIn   wi_DAC5 (.okHE(okHE), .ep_addr(8'h11), .ep_dataout(epwire_11));
okWireIn   wi_DAC6 (.okHE(okHE), .ep_addr(8'h12), .ep_dataout(epwire_12));
okTriggerIn   ti_ProgResetDAC (.okHE(okHE), .ep_addr(8'h40), .ep_clk(clk_1M), .ep_trigger(epwire_40));
okWireOut  wo_ProgResetDAC_Ret (.okHE(okHE), .okEH(okEHx[ 0*65 +: 65 ]), .ep_addr(8'h20), .ep_datain(epwire_20));
okWireIn   wi_SPCIMAGER_SPI_BINA_DELAYGEN_POS1 (.okHE(okHE), .ep_addr(8'h13), .ep_dataout(epwire_13));
okWireIn   wi_SPCIMAGER_SPI_BINA_DELAYGEN_DAC (.okHE(okHE), .ep_addr(8'h14), .ep_dataout(epwire_14));
okWireIn   wi_SPCIMAGER_SPI_BINB_DELAYGEN_POS1 (.okHE(okHE), .ep_addr(8'h15), .ep_dataout(epwire_15));
okWireIn   wi_ROI_FIRST_ROW (.okHE(okHE), .ep_addr(8'h16), .ep_dataout(epwire_16));
okWireIn   wi_ROI_FIRST_COL (.okHE(okHE), .ep_addr(8'h17), .ep_dataout(epwire_17));
okWireIn   wi_ROI_LAST_COL (.okHE(okHE), .ep_addr(8'h18), .ep_dataout(epwire_18));
okTriggerIn   ti_EXPOSURE_START_TRIGGER (.okHE(okHE), .ep_addr(8'h44), .ep_clk(SYS_CLK2), .ep_trigger(epwire_44));
okTriggerIn   ti_RST_CTRL_SR (.okHE(okHE), .ep_addr(8'h41), .ep_clk(SYS_CLK2), .ep_trigger(epwire_41));
okTriggerIn   ti_PROG_CTRL_SR (.okHE(okHE), .ep_addr(8'h42), .ep_clk(SYS_CLK2), .ep_trigger(epwire_42));
okTriggerOut  to_PROG_COMPLETE (.okHE(okHE), .okEH(okEHx[ 1*65 +: 65 ]), .ep_addr(8'h60),.ep_clk(SYS_CLK2), .ep_trigger(epwire_60));
okBTPipeOut  btpo_ADC_FIFO_OUT (.okHE(okHE), .okEH(okEHx[ 2*65 +: 65 ]), .ep_read(ADC_FIFO_OUT_rd), .ep_addr(8'hA2), .ep_datain(epwire_A2), .ep_ready(ADC_FIFO_OUT_ready));
okTriggerIn   ti_ADC_FIFO_RST (.okHE(okHE), .ep_addr(8'h43), .ep_clk(SYS_CLK2), .ep_trigger(epwire_43));
okWireIn   wi_EXPOSURE_TIME_LSB (.okHE(okHE), .ep_addr(8'h1A), .ep_dataout(epwire_1A));
okWireIn   wi_EXPOSURE_TIME_MSB (.okHE(okHE), .ep_addr(8'h1B), .ep_dataout(epwire_1B));
okWireOut  wo_EXPOSURE_TIME_LSB_RET (.okHE(okHE), .okEH(okEHx[ 3*65 +: 65 ]), .ep_addr(8'h24), .ep_datain(epwire_24));
okWireOut  wo_EXPOSURE_TIME_MSB_RET (.okHE(okHE), .okEH(okEHx[ 4*65 +: 65 ]), .ep_addr(8'h25), .ep_datain(epwire_25));
okWireOut  wo_FIFO_WR_COUNT (.okHE(okHE), .okEH(okEHx[ 5*65 +: 65 ]), .ep_addr(8'h22), .ep_datain(epwire_22));
okWireOut  wo_FIFO_WR_LIMIT (.okHE(okHE), .okEH(okEHx[ 6*65 +: 65 ]), .ep_addr(8'h23), .ep_datain(epwire_23));
okTriggerIn   ti_DEBUG_PULSERESET (.okHE(okHE), .ep_addr(8'h45), .ep_clk(SYS_CLK2), .ep_trigger(epwire_45));
okWireIn   wi_NO_OF_EXPOSURES (.okHE(okHE), .ep_addr(8'h19), .ep_dataout(epwire_19));
okWireOut  wo_FIRMWARE_REVISION (.okHE(okHE), .okEH(okEHx[ 7*65 +: 65 ]), .ep_addr(8'h3f), .ep_datain(epwire_3f));
okWireIn   wi_ROLLING_RESET_CYCLES (.okHE(okHE), .ep_addr(8'h1c), .ep_dataout(epwire_1c));
okWireIn   wi_GLOBAL_RESET_CYCLES (.okHE(okHE), .ep_addr(8'h1d), .ep_dataout(epwire_1d));
okWireIn   wi_COLUMN_CYCLES_CROWBAR (.okHE(okHE), .ep_addr(8'h1e), .ep_dataout(epwire_1e));
okWireIn   wi_ADC_CROWBAR_SAMPLE_START (.okHE(okHE), .ep_addr(8'h1f), .ep_dataout(epwire_1f));
okBTPipeOut  btpo_SINGLE_BIT_FIFO_OUT (.okHE(okHE), .okEH(okEHx[ 8*65 +: 65 ]), .ep_read(SINGLE_BIT_FIFO_OUT_rd), .ep_addr(8'hA3), .ep_datain(epwire_A3), .ep_ready(SINGLE_BIT_FIFO_OUT_ready));

endmodule
