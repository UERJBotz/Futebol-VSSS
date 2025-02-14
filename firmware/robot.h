void     bipe(int); //millis
void     move(uint8_t, uint8_t); //%, %
uint32_t batt(void); //mV

#ifdef VESPA
    #include <RoboCore_Vespa.h>

    VespaLED     led;
    VespaButton  button;
    VespaBattery vbat;
    VespaMotors  motors;
    
    void move(uint8_t esq, uint8_t dir) {
        motors.turn(esq, dir);
    }
    uint32_t batt() {
        return vbat.readVoltage(); //mV
    }
    void bipe(int dt) {
	move(20, 20);
	delay(dt);
	move(0, 0);
    }
#else
    static_assert(0, "robôs por enquanto só com a vespa");
#endif

