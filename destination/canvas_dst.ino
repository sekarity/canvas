/**
   CANvas Automotive Network Mapper v1.0
   Destination Mapping Component

   Author: Sekar Kulandaivel (github.com/sekarkulandaivel)

   Version Date: August 14, 2019
   Version Updates:
     - Isolates target ECU via "direct injection" bus-off on non-target ECUs
     - Determines the "message-reception" filter for a target ECU

   Copyright (c) 2017-2019, Carnegie Mellon University. All rights reserved.
*/

#include <Arduino.h>
#include <due_can.h>
#include "variant.h"

#define CANTX 7
#define CANRX 8
#define BUS_EOF 0b1111111

// define TARGET in binary with bit stuffing
#define TARGET 0b0001001000110001  // 0x123
#define TARGET_ID 0x123
#define TARGET_FILTER 0x7ff
#define BUS_SPEED CAN_BPS_500K

volatile uint16_t counter;
volatile uint16_t identifier;

// ISR for each bit time
void TC2_Handler(void) {

  // ensures proper timing
  TC_GetStatus(TC0, 2);

  identifier = (identifier << 1);
  counter++;

  if (digitalReadDirect(CANRX)) {
    digitalWriteDirect(12, 1);
    identifier++;
  }

  if (identifier == TARGET) {
    pinMode(CANTX, OUTPUT);
    digitalWriteDirect(CANTX, 0);
    delayMicroseconds(1000000 / BUS_SPEED * 6);
    pinMode(CANTX, INPUT);
    TC_Stop(TC0, 2);
  }

  digitalWriteDirect(12, 0);

  if (counter > 20) { // 12 + 2 stuff bits
    TC_Stop(TC0, 2);
  }
}

// user-defined ISR for start-of-frame
void CAN0_Handler(void) {
  if (CAN0->CAN_SR & CAN_SR_TSTP) {
    identifier = digitalReadDirect(CANRX);
    NVIC_EnableIRQ(TC2_IRQn);
    TC_Start(TC0, 2);
    digitalWriteDirect(12, 1);
    digitalWriteDirect(12, 0);
    identifier = (identifier << 1);
    identifier = digitalReadDirect(CANRX);
    counter = 1;
  }
}

void setup() {

  pinMode(12, OUTPUT);
  // bus-off pin -- connect directly to CANTX
  pinMode(CANTX, INPUT);
  // feedback pin -- connect directly to CANRX
  pinMode(CANRX, INPUT);

  // setup timer for bit time
  setup_timer0_ch2();

  Can0.init(BUS_SPEED);
  // set all mailbox filters to match target
  for (int filter = 0; filter < 7; filter++) {
    Can0.setRXFilter(filter, TARGET_ID, TARGET_FILTER, false);
  }
  // capture timestamp at start-of-frame
  Can0.set_timestamp_capture_point(0);
//  // set CAN0 handler at higher priority
//  NVIC_SetPriority(CAN0_IRQn, 0);
  // enable interrupt at timestamp capture point
  Can0.enable_interrupt(Can0.get_status() & CAN_IER_TSTP);

}

void loop() {
  ;
}

// timer0_ch2 is first available timer intended for interrupt purposes
void setup_timer0_ch2() {

  // enables clock for timer0-channel2
  pmc_enable_periph_clk(ID_TC2);
  // setup timer0-channel2 to generate waveform, trigger on up, and scaled clock1 (MCK / 2)
  TC_Configure(TC0, 2, TC_CMR_WAVE | TC_CMR_WAVSEL_UP_RC | TC_CMR_TCCLKS_TIMER_CLOCK1);
  // set time to CLOCK1 / CAN_BPS
  TC_SetRC(TC0, 2, VARIANT_MCK / 2 / BUS_SPEED);
  // enable RC compare interrupt
  TC0->TC_CHANNEL[2].TC_IER = TC_IER_CPCS;
  // disable all other interrupts
  TC0->TC_CHANNEL[2].TC_IDR = ~TC_IER_CPCS;

}

/**
   Source: github.com/stimmer/DueVGA
*/
inline void digitalWriteDirect(int pin, boolean val) {
  if (val) g_APinDescription[pin].pPort -> PIO_SODR = g_APinDescription[pin].ulPin;
  else    g_APinDescription[pin].pPort -> PIO_CODR = g_APinDescription[pin].ulPin;
}

/**
   Source: github.com/stimmer/DueVGA
*/
inline int digitalReadDirect(int pin) {
  return !!(g_APinDescription[pin].pPort -> PIO_PDSR & g_APinDescription[pin].ulPin);
}
