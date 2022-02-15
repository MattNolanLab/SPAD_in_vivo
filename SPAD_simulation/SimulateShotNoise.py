import numpy as np 


class SimulateShotNoise():
    def __init__(self):
        
        print('Welcome to Shot Noise Simulation. First choose the waveform which you would like to stimulate the sensor and then run the simulation ')
        
        
    
    def create_wave(self, wave_type, frequency, sampling_frequency, amplitude, offset=10000):

        if wave_type == 'pulse':
            wave = np.tile([1,2],frequency)
            wave = amplitude*np.repeat(wave, (sampling_frequency/frequency)/2)
            return wave
        elif wave_type == 'sine':
            start_time = 0
            end_time = 1
            time = np.arange(start_time, end_time, 1/sampling_frequency)
            theta = 0
            sinewave = (amplitude)* np.sin(2 * np.pi * frequency * time + theta)+offset
            return sinewave
        else:
            print('Please chose either sine or pulse wave')
            
            
            
            
    def simulate_sensor(self,sensor_sampling_rate, stimulation_pattern, waveform_sampling_frequency):

        #sensor_sampling_rate = 100000
        sampling_freq = waveform_sampling_frequency
        sensor_output = np.zeros((sensor_sampling_rate,1))

        step = int(sampling_freq/sensor_sampling_rate)

        for i in range(len(sensor_output)):
            sensor_output[i,0] = np.random.poisson(stimulation_pattern[i*step],1)

        return sensor_output