#ifndef RRDUINO_CLIENT_H
#define RRDUINO_CLIENT_H

#include <Arduino.h>
#include "BaseRRDuinoClient.h"

class RRDuinoClient : protected BaseRRDuinoClient { 
  private:
    Thermistor _thermistor;
    float _temperature_C;

  public:
    RRDuinoClient(String const& id, String const& key);

    // Virtual interfaces
    virtual void update(); //!< Send an "update" command
    virtual boolean tick(); //!< Gather information before sending an "update"
};

#endif
