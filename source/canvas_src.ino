/**
   CANvas Automotive Network Mapper v1.0
   Source Mapping Component

   Author: Sekar Kulandaivel (github.com/sekarkulandaivel)

   Version Date: August 14, 2019
   Version Updates:
     - Collects hardware-timestamped traffic from bus

   Copyright (c) 2017-2019, Carnegie Mellon University. All rights reserved.
*/

#include <Arduino.h>
#include <due_can.h>
#include "variant.h"

#define CANSOF 9
#define CANRCV 10
#define CANOVR 11

#define BUS_SPEED CAN_BPS_500K

CAN_FRAME incoming;

volatile uint16_t timestamp;
volatile uint16_t identifier;

// user-defined ISR for start-of-frame or message receive
void CAN0_Handler(void) {

  uint32_t ul_status = CAN0->CAN_SR;
  if (ul_status & CAN_SR_TSTP) {
    digitalWriteDirect(CANSOF, 1);
    digitalWriteDirect(CANSOF, 0);
  }
  if (ul_status & CAN_SR_MB0) {
    timestamp = CAN0->CAN_TIMESTP;
    identifier = (CAN0->CAN_MB[0].CAN_MID >> CAN_MID_MIDvA_Pos) & 0x7ffu;
    Can0.mailbox_send_transfer_cmd(0);
    digitalWriteDirect(CANRCV, 1);
    digitalWriteDirect(CANRCV, 0);
    Serial.write(identifier);
    Serial.write(timestamp);
    Serial.write("\n");
    
  }
  if ((ul_status & CAN_MSR_MRDY) && (ul_status & CAN_MSR_MMI)) {
    digitalWriteDirect(CANOVR, 1);
    digitalWriteDirect(CANOVR, 0);
  }
}

void setup() {

  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  
  Can0.init(BUS_SPEED);
  Serial.begin(115200);
  // capture timestamp at start-of-frame
  Can0.set_timestamp_capture_point(0);
  // set mailbox filter to receive all
  Can0.setRXFilter(0, 0x000, 0x000, false);
  // disables all but one mailbox (in RX w/o overwrite)
  Can0.mailbox_set_mode(0, 1);
  for (int mailbox = 1; mailbox < 8; mailbox++) {
    Can0.mailbox_set_mode(mailbox, 0);
  }
  // set CAN0 handler at higher priority
  NVIC_SetPriority(CAN0_IRQn, 0);
  // enable interrupt at timestamp capture point
  Can0.enable_interrupt(Can0.get_interrupt_mask() & CAN_IER_TSTP & CAN_IER_MB0);
}

void loop() {
  
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
