import numpy as np
from gnuradio import gr
import time

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="peak_reader",
            in_sig=[(np.float32, 4096)],
            out_sig=None
        )

        self.last_print = 0.0

        self.fft_size = 4096
        self.center_freq = 1.42e9
        self.samp_rate = 3e6
        self.decimation = 5
        self.fft_rate = self.samp_rate / self.decimation

    def work(self, input_items, output_items):
        for vec in input_items[0]:
            peak_index = int(np.argmax(vec))
            peak_value_db = float(vec[peak_index])

            bin_width = self.fft_rate / self.fft_size
            peak_freq = self.center_freq + (peak_index - self.fft_size / 2) * bin_width

            now = time.time()
            if now - self.last_print >= 0.2:
                print(
                    f"Peak bin: {peak_index} | "
                    f"Peak value: {peak_value_db:.3f} dB | "
                    f"Peak freq: {peak_freq:.3f} Hz"
                )
                self.last_print = now

        return len(input_items[0])