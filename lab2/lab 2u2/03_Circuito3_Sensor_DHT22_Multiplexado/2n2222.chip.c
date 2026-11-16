#include "wokwi-api.h"
#include <stdlib.h>

typedef struct {
  pin_t pin_base;
  pin_t pin_col;
  pin_t pin_emi;
} chip_state_t;

static void on_base_change(void *user_data, pin_t pin, uint32_t level) {
  chip_state_t *chip = (chip_state_t *)user_data;
  
  if (level == HIGH) {
    // Transistor NPN Conduciendo: Conecta el colector a GND digital
    pin_mode(chip->pin_col, OUTPUT);
    pin_write(chip->pin_col, LOW); 
  } else {
    // Transistor NPN en Corte: Colector en alta impedancia (circuito abierto)
    pin_mode(chip->pin_col, INPUT); 
  }
}

void chip_init() {
  chip_state_t *chip = malloc(sizeof(chip_state_t));

  chip->pin_base = pin_init("BASE", INPUT);
  chip->pin_col = pin_init("COL", INPUT); // Inicia abierto
  chip->pin_emi = pin_init("EMI", INPUT);

  const pin_watch_config_t watch_config = {
    .edge = BOTH,
    .pin_change = on_base_change,
    .user_data = chip,
  };
  pin_watch(chip->pin_base, &watch_config);
}